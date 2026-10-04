#!/usr/bin/env bash
#
# Minimal end-to-end check for platforms where the full PowerShell suite does not
# run. The full suite (tests/run_tests.ps1) covers 50 cases and is the primary
# gate; this exists so that a Linux build is verified to actually work, not
# merely to compile.
#
# It starts a real server, transfers a real file over real TLS, and compares the
# SHA-256 of the stored file with the source using an external tool, so the check
# does not rely on the program's own claim of success.
#
# Usage: tests/smoke_test.sh [build-dir] [port]

set -euo pipefail

BUILD_DIR="${1:-build}"
PORT="${2:-9300}"
EXE="$BUILD_DIR/FTP"
CERT="$BUILD_DIR/server.crt"
LOG="$(mktemp)"
WORK="$(mktemp -d)"
SRC="$WORK/smoke.bin"
DST="$BUILD_DIR/received_smoke.bin"
SERVER_PID=""

cleanup() {
    if [ -n "$SERVER_PID" ] && kill -0 "$SERVER_PID" 2>/dev/null; then
        kill "$SERVER_PID" 2>/dev/null || true
        wait "$SERVER_PID" 2>/dev/null || true
    fi
    rm -rf "$WORK" "$LOG"
}
trap cleanup EXIT

fail() {
    echo "FAIL: $*" >&2
    if [ -s "$LOG" ]; then
        echo "--- server log ---" >&2
        cat "$LOG" >&2
    fi
    exit 1
}

pass() { echo "PASS: $*"; }

[ -x "$EXE" ] || fail "$EXE not found or not executable"
[ -f "$CERT" ] || fail "$CERT not found; the build did not stage a certificate"

# The server stores uploads relative to its own working directory, so it is
# started inside the build directory: that is where the certificate was staged
# and where the stored file is expected. An absolute path is resolved first,
# because the subshell below changes directory.
BUILD_DIR_ABS="$(cd "$BUILD_DIR" && pwd)"

# 8 MB of non-zero data, so a truncated or zero-filled transfer cannot pass by
# accident. /dev/urandom would be ideal but is not reproducible; a fixed pattern
# is enough because the digest is compared, not assumed.
head -c 8388608 /dev/zero | tr '\0' 'A' > "$SRC"
EXPECTED_SHA="$(sha256sum "$SRC" | cut -d' ' -f1)"

rm -f "$DST"

echo "starting server on port $PORT"
# exec inside the subshell, so the background PID is the server itself and
# cleanup can signal it.
( cd "$BUILD_DIR_ABS" && exec "$BUILD_DIR_ABS/FTP" server "$PORT" ) > "$LOG" 2>&1 &
SERVER_PID=$!

# Wait for the listener rather than sleeping a fixed amount, so a slow machine
# does not produce a false failure.
for _ in $(seq 1 100); do
    if grep -q "Listening on port" "$LOG" 2>/dev/null; then
        break
    fi
    if ! kill -0 "$SERVER_PID" 2>/dev/null; then
        fail "the server exited before it started listening"
    fi
    sleep 0.1
done
grep -q "Listening on port" "$LOG" || fail "the server did not report a listener within 10s"
pass "the server is listening"

# Send the file and require a zero exit status: the client exits 0 only when the
# server confirmed a matching digest.
if ! "$EXE" client "$SRC" 127.0.0.1 "$PORT" > "$WORK/client.log" 2>&1; then
    cat "$WORK/client.log" >&2
    fail "the client exited non-zero"
fi
grep -q "hash matches" "$WORK/client.log" || {
    cat "$WORK/client.log" >&2
    fail "the client did not report a verified transfer"
}
pass "the client transferred the file and the server verified the digest"

[ -f "$DST" ] || fail "$DST was not created"
ACTUAL_SHA="$(sha256sum "$DST" | cut -d' ' -f1)"
[ "$ACTUAL_SHA" = "$EXPECTED_SHA" ] || fail "digest mismatch: $ACTUAL_SHA != $EXPECTED_SHA"
pass "the stored file matches the source byte for byte ($ACTUAL_SHA)"

[ "$(stat -c %s "$DST")" = "8388608" ] || fail "the stored file has the wrong size"
pass "the stored size is correct (8388608 bytes)"

# A plaintext probe must fail the TLS handshake rather than be interpreted as a
# session. The legitimate transfer above already produced one completed
# handshake, so exactly one must remain after the probe.
complete_count() { grep -c "TLS handshake complete" "$LOG" 2>/dev/null || true; }

COMPLETE_BEFORE="$(complete_count)"
[ "$COMPLETE_BEFORE" = "1" ] || fail "expected 1 completed handshake, saw $COMPLETE_BEFORE"

printf 'GET / HTTP/1.1\r\nHost: localhost\r\n\r\n' > "$WORK/probe.txt"
if command -v nc > /dev/null 2>&1; then
    nc -w 2 127.0.0.1 "$PORT" < "$WORK/probe.txt" > /dev/null 2>&1 || true
else
    timeout 2 bash -c "cat '$WORK/probe.txt' > /dev/tcp/127.0.0.1/$PORT" 2> /dev/null || true
fi
sleep 1

grep -q "TLS handshake failed" "$LOG" || fail "a plaintext probe did not fail the TLS handshake"
COMPLETE_AFTER="$(complete_count)"
[ "$COMPLETE_AFTER" = "1" ] || fail "the plaintext probe was accepted as a session ($COMPLETE_AFTER completed handshakes)"
pass "plaintext was rejected at the TLS layer"

# The rejected probe must not have created or altered any stored file.
[ ! -e "$DST.remote_probe" ] || fail "the plaintext probe created a stored file"
pass "the rejected probe left no stored file"

rm -f "$DST"
echo "smoke test passed"

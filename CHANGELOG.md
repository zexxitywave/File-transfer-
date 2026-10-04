# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
The version is declared once, as `project(FTP VERSION ...)` in `CMakeLists.txt`,
and is reported by `FTP --version`.

## [Unreleased]

Nothing yet. Changes land here first and are grouped into a release at tag time;
see [CONTRIBUTING.md](CONTRIBUTING.md#releases).

## [1.0.0] - 2026-09-30

First public release. Upload-only, TLS-encrypted, resumable transfer with
SHA-256 verification of every stored file.

### Added

- TLS 1.2+ transport for every connection, with OpenSSL SNI so the server is
  asked for by name.
- Certificate verification on the client, on by default: the chain *and* the
  host name are checked, including IP literals such as `127.0.0.1`.
  `--ca <file>` verifies against a different authority; `--insecure` disables
  verification and prints a warning.
- Resumable uploads. The server reports how many bytes it already holds and the
  client continues from that offset, so an interrupted transfer does not
  restart from zero. A stored copy larger than the source is treated as stale
  and restarted.
- SHA-256 integrity verification after every transfer, computed incrementally
  with OpenSSL's `EVP` interface. A file whose digest does not match the
  sender's is deleted and the client exits non-zero.
- Concurrent sessions: one `io_context` pool of 2-4 threads, at most one
  operation in flight per session, so several clients transfer at once without
  occupying a worker thread.
- Per-destination exclusion, so two clients can never write the same
  `received_<name>`; the second one is refused as *busy*.
- Strict file name validation, rejecting path separators, `..`, control
  characters, reserved device names and over-long names.
- `--version` and `--help`.
- End-to-end test suite (`tests/run_tests.ps1`, registered with CTest) covering
  clean transfers, resumption after a kill, tampered-file rejection, four
  concurrent clients, destination contention and the certificate failure cases.
  `tests/smoke_test.sh` provides the same single-transfer check for Linux CI.
- Continuous integration on Linux and Windows (`.github/workflows/ci.yml`).
- Project documentation: `docs/PRD.md`, `docs/ARCHITECTURE.md`, `docs/UML.md`,
  `docs/DEVELOPMENT_PLAN.md`, `docs/TEST_PLAN.md`.

### Changed

- The stored-file transfer rate is printed with two decimals.
- The client looks for `server.crt` next to the executable first and then in
  `./tls_key`, and prints the resolved path before connecting, so a certificate
  mismatch no longer surfaces only as `certificate verify failed`.
- Progress bars are drawn only when the output is a terminal; redirected output
  contains log lines only.

### Fixed

- MinGW builds no longer fail to launch on Windows: the required runtime DLLs
  (`libstdc++-6`, `libgcc_s_seh-1`, `libwinpthread-1`, `libssl-*`, `libcrypto-*`)
  are copied next to the executable at configure time.
- `FindOpenSSL` misses MinGW's `libssl.a` / `libcrypto.a`, so the build falls
  back to a header/library search driven by `OPENSSL_ROOT_DIR`.

### Security

- Verification is on by default; the client refuses to start when it has no CA
  to verify against rather than accepting whatever the server presents.
- A failed chain validation is never overridden by the host name check.
- A host name check failure cannot be bypassed by returning `true` for a
  certificate that failed pre-verification.

### Known limitations

- Upload only: there is no download path.
- No authentication; any client that can reach the port may upload.
- The bundled certificate is self-signed and for development only. Replace it
  with a certificate issued for the host the server runs on.
- No per-user storage: every upload is stored as `received_<name>` in the
  server's working directory.
- The digest of a finished transfer is computed inline, so hashing a very large
  file occupies one thread of the pool.
- The wire protocol is not versioned: client and server must be the same build.

[Unreleased]: https://github.com/zexxitywave/File-transfer-/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/zexxitywave/File-transfer-/releases/tag/v1.0.0

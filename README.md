# Secure FTP Server

**TLS-encrypted, resumable file transfer in C++20 — with SHA-256 verification of
every file it stores.**

[![CI](https://github.com/zexxitywave/File-transfer-/actions/workflows/ci.yml/badge.svg)](https://github.com/zexxitywave/File-transfer-/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/zexxitywave/File-transfer-?label=release&sort=semver)](https://github.com/zexxitywave/File-transfer-/releases/latest)
[![License: MIT](https://img.shields.io/badge/license-MIT-00599C.svg)](LICENSE)
[![C++20](https://img.shields.io/badge/C%2B%2B-20-00599C?logo=c%2B%2B&logoColor=white)](CMakeLists.txt)
[![OpenSSL](https://img.shields.io/badge/TLS-OpenSSL%203.x-00599C?logo=openssl&logoColor=white)](https://www.openssl.org/)
[![Platforms](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey?logo=windows&logoColor=white)](CMakeLists.txt)
[![Tests](https://img.shields.io/badge/tests-50%20checks-00599C)](tests/run_tests.ps1)

---

## Contents

- [About](#about)
- [Quick start](#quick-start)
- [Features](#features)
- [Documentation](#documentation)
- [Tech stack](#tech-stack)
- [How it works](#how-it-works)
- [Protocol](#protocol)
- [Fault tolerance](#fault-tolerance)
- [Security](#security)
- [Building](#building)
- [Running](#running)
- [Testing](#testing)
- [Project layout](#project-layout)
- [Known limitations](#known-limitations)
- [Roadmap](#roadmap)
- [Releases](#releases)
- [Contributing](#contributing)
- [License](#license)
- [Troubleshooting](#troubleshooting)
- [Acknowledgements](#acknowledgements)

---

## About

This project implements a secure client-server file transfer protocol that
recovers from network interruptions without restarting the transfer. Data is
encrypted with TLS, and the receiver proves the delivered file matches the one
that was sent before it is accepted.

It is a single C++20 executable that runs in one of two modes — `server` and
`client` — built with CMake, using Boost.Asio for networking and OpenSSL for
TLS and hashing.

| | |
| --- | --- |
| **Problem** | Transfers either restart from zero or complete with no proof of integrity, and data travels in clear text. |
| **Solution** | A TLS-encrypted, resumable upload that verifies the SHA-256 of the stored file and deletes it on mismatch. |
| **Audience** | A machine that has to *receive* files reliably over an unstable or hostile link. |
| **Scope** | Upload only, no authentication, no per-user storage. See [Known limitations](#known-limitations). |
| **Status** | v1.0.0. Client and server are the same build; the protocol is not versioned. |
| **Platforms** | Windows and Linux, MSVC and MinGW/GCC, built and tested in CI. |

### Design goals

- Secure communication by default, with verification that cannot be silently
  switched off
- High reliability: a dropped connection costs the remaining bytes, not the file
- Provable delivery: the sender's digest is checked, not merely reported
- Modular, extensible code with one component per translation unit
- Fault tolerance that is tested end to end, not asserted

---

## Quick start

```bash
git clone https://github.com/zexxitywave/File-transfer-.git
cd File-transfer-

# 1. Dependencies: CMake 3.15+, a C++20 compiler, OpenSSL, Boost headers
#    Debian/Ubuntu: sudo apt-get install cmake g++ libssl-dev libboost-dev

# 2. A certificate is required and is never committed to the repository
mkdir -p tls_key
openssl req -x509 -newkey rsa:2048 -nodes \
  -keyout tls_key/server.key -out tls_key/server.crt \
  -days 365 -subj "/CN=localhost" \
  -addext "subjectAltName=DNS:localhost,IP:127.0.0.1"

# 3. Build and test
cmake -S . -B build
cmake --build build
ctest --test-dir build --output-on-failure

# 4. Transfer a file. Start the server from the build directory, because that
#    is where the certificate and the uploads live.
cd build
./FTP server 9000          # terminal 1
./FTP client ../note.txt    # terminal 2
```

Uploads arrive as `received_<name>`. Kill the client mid-transfer and run the
same command again: the server reports how many bytes it already holds and the
transfer continues from there.

```text
# [SERVER] Listening on port 9000 (TLS enabled)
# [CLIENT] Resuming at offset 3407872 of 8388608
# [SUCCESS] Server verified the file (hash matches)
```

On Windows use `FTP.exe`, and prefix it with `.\` in PowerShell: a bare
`FTP.exe` resolves to the built-in `C:\Windows\System32\ftp.exe`.

`FTP --version` and `FTP --help` print the version and the usage text without
needing a certificate or a peer.

---

## Features

- **TLS encryption** using OpenSSL, with SNI so the server is asked for by name
- **Certificate verification on by default** — chain *and* host name, including
  IP literals such as `127.0.0.1`
- **Automatic resumption** after connection loss, from the last stored byte
- **Integrity verification** with SHA-256 computed incrementally; a file that
  does not match is deleted
- **Concurrent clients** served from a small thread pool, with at most one
  operation in flight per session
- **One writer per destination** — a second client is refused as *busy* rather
  than overwriting a transfer in progress
- **Strict file name validation** — no path separators, no `..`, no control
  characters, no reserved device names
- **End-to-end test suite** of 50 automated checks over real TLS connections,
  registered with CTest
- **Cross-platform** builds from one CMake project, MSVC and MinGW supported

---

## Documentation

| Document | Contents |
| --- | --- |
| [docs/PRD.md](docs/PRD.md) | Project Requirements Document: problem, scope, 20 functional and 12 non-functional requirements, limitations, deliverables |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Layers, component responsibilities, concurrency model, data structures, wire protocol, design decisions, security design |
| [docs/UML.md](docs/UML.md) | Class diagram, three sequence diagrams, two state machine diagrams |
| [docs/DEVELOPMENT_PLAN.md](docs/DEVELOPMENT_PLAN.md) | The six project stages mapped to the work done, timeline, demonstration script |
| [docs/TEST_PLAN.md](docs/TEST_PLAN.md) | Test strategy, coverage traceability, defects found and fixed, measured results |
| [CHANGELOG.md](CHANGELOG.md) | Every user-visible change, per release |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Local setup, code style, commit conventions, pull request and release process |
| [SECURITY.md](SECURITY.md) | Supported versions, private reporting, threat model, hardening a deployment |
| [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) | Expected behaviour, and how to report a violation |

---

## Tech stack

| | |
| --- | --- |
| **Language** | C++20 |
| **Build system** | CMake 3.15+ |
| **Networking** | Boost.Asio (header only) |
| **Security** | OpenSSL — TLS transport and SHA-256 |
| **Concurrency** | `std::thread` pool driving a shared `io_context` |
| **Sockets** | Boost.Asio over WinSock or BSD sockets |
| **Testing** | PowerShell and Bash end-to-end scripts, driven by CTest |
| **CI** | GitHub Actions, Linux and Windows |

---

## How it works

The code is five layers, with dependencies pointing one way only:

```text
main.cpp        command line, certificate discovery, event loop
   |
server.cpp      acceptor, shared SSL context, destination claim set
client.cpp      connect, send header, honour the resume offset
   |
serverSession.cpp   request validation, chunk loop, integrity verdict
   |
protocol.hpp    wire constants and status codes (shared contract)
checksum.hpp    incremental SHA-256
logging.hpp     progress, warnings and errors
```

- **Server** — accepts connections, creates a session for each client, serves
  them all concurrently, and guarantees that only one client at a time writes a
  given `received_<name>`.
- **Client** — connects securely, verifies the server certificate, uploads the
  file, and resumes an interrupted transfer from the offset the server reports.
- **Server session** — validates the request before anything is stored, receives
  64 KB chunks, tracks transfer state, recovers interrupted transfers, and
  verifies the digest before declaring success.
- **Checksum** — SHA-256 via OpenSSL's `EVP` interface, computed incrementally so
  memory use does not depend on file size.

Every step of a session is asynchronous and keeps at most one operation in
flight, so a transfer never occupies a worker thread. The server runs its
`io_context` on a small pool of two to four threads, which is what allows
several clients to transfer at the same time.

---

## Protocol

```text
client                                   server
  |---- uint32 name_len -------------------->|
  |---- name_len bytes filename ------------>|
  |---- 64 bytes hex SHA-256 --------------->|
  |---- uint64 file_size -------------------->|
  |                                          |  the whole request is validated
  |                                          |  before anything is stored
  |<--- 1 byte status (proceed / refused) ---|
  |<--- uint64 resume_offset ----------------|  only when proceeding
  |---- payload, 64 KB chunks --------------->|
  |<--- 1 byte status (verified / failed) ---|
```

All scalars are host byte order and each is sent as a single write, so the
header never needs packing. Uploads are stored as `received_<name>`, which is
what makes resumption possible: the stored file length is the resume offset.

Because the request is validated up front, a refusal is reported as a status
byte instead of a misleading resume offset. A client whose file is already being
uploaded by somebody else is told the destination is **busy** and exits, rather
than writing over the other transfer.

The protocol is not versioned, so a client and a server must be the same build.

---

## Fault tolerance

```text
Client
    │
 Upload File
    │
 Connection Lost
    │
 Reconnect
    │
 Resume From Last Received Byte
    │
 Transfer Complete
```

Instead of retransmitting the entire file, the client resumes from the last
offset the server has on disk, which reduces bandwidth usage and improves
reliability. Because that offset *is* the size of the partially stored file, a
file whose stored copy is larger than the source is treated as stale and
restarted from zero.

This behaviour is exercised by the test suite, which kills a client mid-transfer
and then resumes it: see the *resumption* group in `docs/TEST_PLAN.md`.

---

## Security

All communication is encrypted with **TLS**, and the client verifies the server
by default.

| Measure | Detail |
| --- | --- |
| Encrypted transport | TLS 1.2 or newer via OpenSSL, with SNI |
| Certificate verification | Chain **and** host name checked by default, IP literals included |
| No silent downgrade | `--insecure` exists for troubleshooting, prints a warning |
| Fail closed | The client refuses to start when it has no CA to verify against |
| Strict validation | File names are rejected before anything is written |
| Integrity | SHA-256 compared after every transfer; a mismatch deletes the file |
| Exclusive writes | One writer per destination; contention is refused as *busy* |

The client looks for `server.crt` next to the executable, then in `./tls_key`,
which is where the build copies the development certificate. The resolved path
is printed before connecting, because a mismatch otherwise surfaces only as
`certificate verify failed`. Use `--ca <file>` to verify against a different
authority.

The bundled certificate is self-signed and intended for development. A trusted
deployment should replace it with a certificate issued for the host it runs on.

**The server authenticates nobody.** Any client that can reach the port may
upload. Do not expose it to an untrusted network, and read
[SECURITY.md](SECURITY.md) before deploying it.

---

## Building

### Requirements

- CMake 3.15+
- A C++20 compiler (MSVC 2019+, GCC 10+, Clang 10+)
- Boost 1.70+ (**headers only**, used by Boost.Asio)
- OpenSSL 1.1.1+ development libraries
- PowerShell 5.1+ on Windows, to run the end-to-end suite

CMake never links Boost libraries, because Asio is header only. OpenSSL *is*
linked, so both its headers and its import/static libraries are required.

> **Note for MinGW (including the toolchain bundled with CLion):** the bundled
> GCC does not ship OpenSSL or Boost, so install both yourself. `FindOpenSSL` on
> Windows also ignores MinGW's `libssl.a` / `libcrypto.a` archives, so
> `CMakeLists.txt` falls back to a plain header/library search driven by
> `OPENSSL_ROOT_DIR`. When configuring from a plain `cmd`/`PowerShell` window,
> also put the compiler's `bin\mingw\bin` on `PATH`, otherwise CMake cannot find
> `mingw32-make.exe` for the generator and reports the compiler as broken.

### Clone

```bash
git clone https://github.com/zexxitywave/File-transfer-.git
cd File-transfer-
```

The repository deliberately contains no certificate or private key, so the next
step is required before the server will start.

### Generate the TLS certificate

The server refuses to start without a certificate. Create a self-signed pair
once (they are intentionally kept out of version control). The subject
alternative names let the client verify the host by name, including `127.0.0.1`:

```bash
openssl req -x509 -newkey rsa:2048 -nodes \
  -keyout tls_key/server.key -out tls_key/server.crt \
  -days 365 -subj "/CN=localhost" \
  -addext "subjectAltName=DNS:localhost,IP:127.0.0.1"
```

### Build

```bash
cmake -S . -B build
cmake --build build
```

If the dependencies are not on a default search path, point CMake at them:

```bash
cmake -S . -B build \
  -DBOOST_ROOT=C:/path/to/boost_1_88_0 \
  -DOPENSSL_ROOT_DIR=C:/path/to/openssl
```

Both variables are optional; drop whichever one resolves automatically. Setting
`OPENSSL_ROOT_DIR` in the environment works too, and on Windows it must point at
the prefix that contains `include/openssl/ssl.h` and `lib/ssl.lib` (MSVC) or
`lib/libssl.a` (MinGW).

On Windows the compiler also needs `ws2_32` and `mswsock`, which `CMakeLists.txt`
adds automatically. If `CMakeLists.txt` changed, re-run the `cmake -S . -B build`
step so the TLS assets are copied next to the new executable.

### Test

```bash
ctest --test-dir build --output-on-failure
```

Or run the script directly, optionally keeping the files it creates:

```bash
powershell -NoProfile -ExecutionPolicy Bypass -File tests/run_tests.ps1 -BuildDir build
powershell -NoProfile -ExecutionPolicy Bypass -File tests/run_tests.ps1 -BuildDir build -KeepArtifacts
```

It exits non-zero if any check fails, and the suite transfers several hundred
megabytes, so it takes roughly a minute.

---

## Running

Start the server (defaults to port 9000). It must be started from the build
directory, because that is where `tls_key/server.crt` and `tls_key/server.key`
are copied and where uploads are written:

```bash
cd build
./FTP server [port]
```

Send a file to it (defaults to 127.0.0.1:9000):

```bash
./FTP client <path/to/file> [host] [port] [--ca <file> | --insecure]
./FTP --help
./FTP --version
```

On Windows use `FTP.exe` instead of `./FTP`, for example `.\FTP.exe server`.

Always prefix the executable with `.\` in PowerShell. A bare `FTP.exe` does not
run this program: PowerShell resolves names through `PATH` and finds the
built-in `C:\Windows\System32\ftp.exe` client instead, which prints Microsoft's
FTP help text. `.\FTP.exe` runs the one in the current directory.

A complete session looks like this:

```bash
# terminal 1
cd build
./FTP server 9000
# [SERVER] Listening on port 9000 (TLS enabled)

# terminal 2
echo hello > note.txt
./FTP client ../note.txt 127.0.0.1 9000
# [SUCCESS] Server verified the file (hash matches)
```

Uploads land in the server's working directory as `received_<name>`. If the
connection drops, run the same client command again: the server reports how many
bytes it already holds and the transfer continues from there. Once a transfer
completes the server recomputes the SHA-256 of the stored file, deletes it if it
does not match, and tells the client the outcome. The client exits with `0` only
when the server confirmed a matching hash.

Two clients may transfer at the same time, but only one client at a time may
write a given name: a second client asking for a destination that is already in
use is refused as **busy** and exits non-zero, rather than writing over the
transfer in progress.

Progress bars are drawn only when the output is a terminal. With the output
redirected to a file, each session's progress is dropped so the log stays
readable, and only real log lines are written.

---

## Testing

There are no mocks and no unit-test framework: the suite starts a real server and
drives real clients over real TLS, then checks the outcome from the outside.

| Suite | Platform | What it covers |
| --- | --- | --- |
| `tests/run_tests.ps1` (registered with CTest) | Windows | 50 checks: clean transfers, resumption after a kill, tampered-file rejection, four concurrent clients, destination contention, certificate failure cases, name validation |
| `tests/smoke_test.sh` | Linux | One real transfer, with the stored file's SHA-256 compared against the source by an external tool |

```bash
ctest --test-dir build --output-on-failure     # Windows: full suite
bash tests/smoke_test.sh build 9300             # Linux: smoke check
```

`docs/TEST_PLAN.md` traces every functional requirement to the check that covers
it, and lists the defects the suite found and how they were fixed.

---

## Project layout

```text
.
├── .github/
│   ├── ISSUE_TEMPLATE/          bug report, feature request, contact links
│   ├── workflows/
│   │   ├── ci.yml               build + test on Linux and Windows
│   │   └── release.yml          tagged releases: build, package, publish
│   ├── dependabot.yml
│   └── PULL_REQUEST_TEMPLATE.md
├── include/
│   ├── checksum.hpp             incremental SHA-256
│   ├── client.hpp
│   ├── logging.hpp
│   ├── protocol.hpp             wire constants and status codes
│   ├── server.hpp
│   └── serverSession.hpp
├── src/
│   ├── main.cpp                 CLI, certificate discovery, event loop
│   ├── client.cpp
│   ├── server.cpp
│   ├── serverSession.cpp
│   └── checksum.cpp
├── tests/
│   ├── run_tests.ps1            end-to-end suite (CTest target end_to_end)
│   └── smoke_test.sh            single-transfer check for Linux CI
├── docs/                        PRD, architecture, UML, plans, test plan
├── .clang-format                formatting rules for the C++ sources
├── .editorconfig                line endings and indentation
├── CHANGELOG.md                 release history
├── CMakeLists.txt               the build, and the single declared version
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── LICENSE                      MIT
├── README.md
├── SECURITY.md
└── tls_key/                     generated locally; never committed
```

---

## Known limitations

- **Upload only.** There is no download path yet, despite the original design
  notes. It is the highest-value addition; see [Roadmap](#roadmap).
- **No authentication.** Any client that can reach the port may upload. The
  bundled certificate is self-signed and intended for development, so a real
  deployment also needs a certificate issued for the host it runs on.
- **No per-user storage.** Every upload is stored as `received_<name>` in the
  server's working directory, so a name is shared by everyone. A client that
  finds the name already in use is refused as *busy* rather than being allowed
  to write over it.
- **Hashing occupies a worker thread.** The digest of a finished transfer is
  computed inline, so a very large file keeps one of the pool's threads busy
  while it hashes.
- **No transfer encryption beyond TLS.** Payloads are not encrypted a second
  time and there is no signing; integrity relies on the SHA-256 comparison.
- **The protocol is not versioned.** Client and server have to be the same
  build.

---

## Roadmap

Planned, roughly in the order it would be worth doing. Contributions welcome;
open an issue first so the approach can be agreed (see
[CONTRIBUTING.md](CONTRIBUTING.md)).

- [ ] Download support, so files can be sent back to a client
- [ ] User authentication, and per-user storage so two users can use the same
      file name
- [ ] Upload/download queue, with a visible transfer list
- [ ] Recursive folder transfer
- [ ] Transfer cancellation
- [ ] Persistent transfer metadata, so resume state survives a server restart
- [ ] Structured logging and monitoring
- [ ] IPv6 support
- [ ] Cross-platform GUI client
- [ ] File compression
- [ ] Directory browsing

---

## Releases

Releases are published from tags: pushing `v<major>.<minor>.<patch>` runs the
release workflow, which rebuilds both platforms, re-runs the tests, and attaches:

| Artifact | Contents |
| --- | --- |
| `ftp-server-<version>-linux-x86_64.tar.gz` | `FTP` binary, `LICENSE`, `README.md`, `CHANGELOG.md`, `docs/` |
| `ftp-server-<version>-windows-x86_64.zip` | `FTP.exe` plus the runtime DLLs it needs, and the same documents |
| `SHA256SUMS.txt` | Checksums for both archives |

Download the latest release from
[GitHub Releases](https://github.com/zexxitywave/File-transfer-/releases/latest),
or clone and build from source — the build is two commands and needs no
installer.

| Version | Supported | Notes |
| --- | --- | --- |
| 1.0.x | Yes | Current. Client and server must be the same build. |

The version is declared once, as `project(FTP VERSION ...)` in
`CMakeLists.txt`, and reported by `FTP --version`. Every user-visible change is
recorded in [CHANGELOG.md](CHANGELOG.md), which follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## Contributing

Bug reports, questions and pull requests are welcome. Please read
[CONTRIBUTING.md](CONTRIBUTING.md) first — it covers the local setup, the
formatting rules enforced by `.clang-format` and `.editorconfig`, the commit
convention, what CI checks on each platform, and how a change is documented.

- [CONTRIBUTING.md](CONTRIBUTING.md) — how to build, test and propose a change
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) — expected behaviour, and how to
  report a violation
- [SECURITY.md](SECURITY.md) — how to report a vulnerability privately

Issue templates are provided for bug reports and feature requests; for anything
security-sensitive, use the private advisory channel rather than an issue.

---

## License

Released under the [MIT License](LICENSE).

```text
MIT License

Copyright (c) 2026 zexxitywave
```

The bundled third-party components keep their own licences: OpenSSL (Apache
License 2.0) and Boost.Asio (Boost Software License 1.0). Neither is vendored
into this repository.

---

## Troubleshooting

**The program prints nothing and returns to the prompt instantly.** This is a
DLL failure, not a program bug. Windows rejects the launch with
`0xC0000135` (`STATUS_DLL_NOT_FOUND`) before `main()` runs, so there is no
output and no error message. Check it with:

```powershell
$LASTEXITCODE    # -1073741515 means 0xC0000135, a missing DLL
```

A MinGW build links its runtime and OpenSSL dynamically, so `libstdc++-6.dll`,
`libgcc_s_seh-1.dll`, `libwinpthread-1.dll`, `libssl-*.dll` and `libcrypto-*.dll`
must be reachable. The build copies them next to the executable
(`Runtime DLLs copied next to the executable` appears in the CMake output), so
if they are missing, point CMake at a real toolchain:

```bash
cmake -S . -B build -DOPENSSL_ROOT_DIR=/path/to/openssl
```

On MSVC the runtime is static and this cannot happen.

**`Address already in use`.** A previous server is still listening. End
`FTP.exe` in Task Manager, or pick another port.

**`certificate verify failed`.** The client trusts a different certificate from
the one the server holds. The path it verified against is printed as
`[INFO] Verifying the server certificate against ...`; check that it is the
`server.crt` belonging to the running server's `server.key`.

**The server logs `handshake error ... http request`.** Something sent plain
HTTP to the TLS port, usually a browser opening `http://localhost:9000`. There
is no web interface; ignore those entries.

---

## Acknowledgements

- **OpenSSL** — TLS transport and SHA-256
- **Boost.Asio** — the asynchronous networking and TLS stream layer
- **CMake** — the build, including the automatic copy of TLS assets and Windows
  runtime DLLs
- **GitHub Actions** — continuous integration on Linux and Windows

This project also stands on the [principles behind TLS](https://tls13.xargs.org/)
and on the well-documented behaviour of the SHA-256 digest, which make a
transfer verifiable rather than merely completed.

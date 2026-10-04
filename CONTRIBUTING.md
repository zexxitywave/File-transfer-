# Contributing to Secure FTP Server

Thanks for taking the time to help. This document explains how to build the
project locally, what the code is expected to look like, how a change is
reviewed and released, and where to ask questions.

By participating you agree to the [Code of Conduct](CODE_OF_CONDUCT.md).

## Table of contents

- [Quick start](#quick-start)
- [Development environment](#development-environment)
- [Running the tests](#running-the-tests)
- [Code style](#code-style)
- [Commit messages](#commit-messages)
- [Opening a pull request](#opening-a-pull-request)
- [Documentation](#documentation)
- [Releases](#releases)
- [Reporting a security issue](#reporting-a-security-issue)

## Quick start

```bash
git clone https://github.com/zexxitywave/File-transfer-.git
cd File-transfer-

# Dependencies: CMake 3.15+, a C++20 compiler, OpenSSL 1.1.1+ and Boost 1.70+
# headers. On Debian/Ubuntu: sudo apt-get install cmake g++ libssl-dev libboost-dev

# The server refuses to start without a certificate. It is never committed.
openssl req -x509 -newkey rsa:2048 -nodes \
  -keyout tls_key/server.key -out tls_key/server.crt \
  -days 365 -subj "/CN=localhost" \
  -addext "subjectAltName=DNS:localhost,IP:127.0.0.1"

cmake -S . -B build
cmake --build build
ctest --test-dir build --output-on-failure
```

On Windows use `FTP.exe` and prefix it with `.\` in PowerShell, otherwise
PowerShell resolves the name to the built-in `C:\Windows\System32\ftp.exe`.
On MinGW, also put the compiler's `bin` directory on `PATH` so CMake can find
`mingw32-make.exe`.

## Development environment

| Dependency | Version | Notes |
| --- | --- | --- |
| CMake | 3.15 or newer | Also provides the `ctest` entry point used by CI. |
| C++20 compiler | MSVC 2019+, GCC 10+, Clang 10+ | Built and tested with GCC 15/16 (MinGW and Linux). |
| OpenSSL | 1.1.1 or newer | Headers **and** libraries: TLS and the SHA-256 digest. |
| Boost | 1.70 or newer | Headers only, used by Boost.Asio. No Boost library is linked. |
| PowerShell 5.1+ | Windows only | Runs the end-to-end suite. |

If a dependency is not on a default search path, pass it explicitly:

```bash
cmake -S . -B build -DBOOST_ROOT=/path/to/boost_1_88_0 -DOPENSSL_ROOT_DIR=/path/to/openssl
```

`OPENSSL_ROOT_DIR` must point at the prefix that contains
`include/openssl/ssl.h` and `lib/ssl.lib` (MSVC) or `lib/libssl.a` (MinGW).
Re-run the configure step after editing `CMakeLists.txt`, because that is the
step that copies the TLS assets and the Windows runtime DLLs next to the
executable.

## Running the tests

There are no mocks and no unit-test framework: the suite starts a real server
and drives real clients over real TLS connections, then checks the outcome from
the outside.

```bash
# Windows: the full end-to-end suite, registered with CTest
ctest --test-dir build --output-on-failure

# Windows: the same suite directly, keeping the files it creates
powershell -NoProfile -ExecutionPolicy Bypass -File tests/run_tests.ps1 -BuildDir build -KeepArtifacts

# Linux: the single-transfer smoke check
bash tests/smoke_test.sh build 9300
```

The end-to-end suite transfers several hundred megabytes and takes roughly a
minute. `docs/TEST_PLAN.md` lists every group it covers and how each functional
requirement is traced to a check.

Guidelines for a change:

1. Add or extend a case in `tests/run_tests.ps1` for any behaviour you add. A
   new feature without a check will be asked for one in review.
2. Keep a change to one concern. A fix, a refactor and a format pass in the same
   commit make the history harder to read than it needs to be.
3. Say in the pull request which manual checks you ran, if any.

## Code style

The rules are enforced by the committed configuration, not by memory:

- `.clang-format` — Google base, C++20, 120 columns, 4-space indent. Run
  `clang-format -i src/*.cpp include/*.hpp` before committing.
- `.editorconfig` — LF endings, UTF-8, no trailing whitespace, final newline.
  This matters on Windows, where Git would otherwise rewrite line endings.

Beyond what the tools enforce:

- Comments explain **why**, not what. A comment restating the code is noise; a
  comment explaining a non-obvious constraint or a rejected alternative is
  valuable.
- One translation unit per component, declared in `include/` and defined in
  `src/`. Headers describe the contract; the `.cpp` carries the reasoning.
- Keep the layer dependency rule: `main` → `server`/`client` → `session` →
  `protocol`/`checksum`/`logging`. Nothing may depend upwards.
- No secret, key or certificate is ever committed. `tls_key/`, `*.key`,
  `*.crt` and `*.pem` are ignored; the certificate is generated locally and by
  CI.

## Commit messages

Use the imperative mood and explain the motivation, in the style the existing
history uses:

```text
Fix Windows launch failures: copy MinGW runtime DLLs, find the CA next to the executable
```

A commit that touches one component keeps its subject under about 72
characters and names the component after a colon. Nothing forces a squash
merge, but a reviewer should be able to read the subject lines alone and
understand what changed.

## Opening a pull request

1. Branch from `main`: `git checkout -b fix/resume-offset-after-idle-timeout`.
2. Make the change, format it, and run the suite.
3. Fill in `.github/PULL_REQUEST_TEMPLATE.md`: what changed, why, and how it was
   verified. Screenshots are not applicable, but log output often is.
4. Push and open the pull request against `main`.

Both CI jobs must pass. Linux runs the build and the smoke test; Windows runs
the build and the full end-to-end suite, so a change that works on Linux only
is caught before review.

By contributing you agree that your work is licensed under the
[MIT License](LICENSE).

## Documentation

| Document | Update it when |
| --- | --- |
| `README.md` | Features, build steps, protocol, limitations or usage change. |
| `docs/PRD.md` | A requirement is added, changed or retired. |
| `docs/ARCHITECTURE.md` | A layer, component, data structure or design decision changes. |
| `docs/UML.md` | A class, its interface, or a sequence/state machine changes. |
| `docs/TEST_PLAN.md` | A test group is added, or a defect is found and fixed. |
| `CHANGELOG.md` | Anything a user could notice. Added under `Unreleased`. |

Documentation that contradicts the code is treated as a defect. If a change
makes an existing document wrong, fixing that document is part of the change.

## Releases

The version lives in exactly one place, `project(FTP VERSION ...)` in
`CMakeLists.txt`, and `FTP --version` reports it. `CHANGELOG.md` follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project
follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

To cut a release:

1. Move everything under `## [Unreleased]` in `CHANGELOG.md` into a
   `## [x.y.z] - YYYY-MM-DD` section, add the compare link at the bottom, and
   open a pull request for it.
2. Update `project(FTP VERSION x.y.z ...)` in the same pull request. The release
   workflow refuses to publish a tag that does not match this declaration.
3. Merge, then tag and push:

   ```bash
   git tag -a v1.1.0 -m "Release v1.1.0"
   git push origin v1.1.0
   ```

4. The `Release` workflow builds both platforms, re-runs the tests, packages the
   binary with the Windows runtime DLLs, publishes the archives with SHA-256
   checksums, and attaches the relevant changelog section as the release notes.

Because the wire protocol is not versioned, a client and a server must come
from the same build. A release that changes the protocol is therefore a major
release.

## Reporting a security issue

Do not open a public issue for a vulnerability. Follow
[SECURITY.md](SECURITY.md) instead.

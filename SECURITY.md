# Security Policy

This project handles files that may be confidential and moves them over a
network. Vulnerabilities are taken seriously and are handled privately.

## Supported versions

| Version | Supported | Notes |
| --- | --- | --- |
| 1.0.x | Yes | Current release. Client and server must be the same build. |

Older versions are not patched. There is no long-term-support branch: this is
a single-line project and the upgrade path is a fresh download.

## Reporting a vulnerability

**Do not open a public issue, and do not open a pull request for a
vulnerability.**

Report it privately through GitHub Security Advisories:

1. Go to `https://github.com/zexxitywave/File-transfer-/security/advisories/new`.
2. Describe the problem, the component (`src/serverSession.cpp`,
   `include/protocol.hpp`, the certificate handling in `src/main.cpp`, …) and
   the version or commit you tested.
3. Include the steps to reproduce, ideally as a short transcript of the two
   terminals (server and client) with the log lines and any file names
   involved.
4. Suggest a fix if you have one, but a report without a fix is still welcome.

You can expect an acknowledgement within a few days and an assessment within two
weeks. If a fix is needed, a release will be prepared and you will be credited
in the changelog unless you prefer to stay anonymous. Please allow time for the
release to be published before disclosing the issue publicly.

## Threat model in one paragraph

The protocol is **TLS 1.2 or newer on every connection**, so payloads are
encrypted and cannot be read or modified in transit by a network attacker. What
TLS does not cover is the destination: **the server authenticates nobody.** Any
client that can reach the port may upload, and uploads are written to the
server's working directory as `received_<name>`. This is a deliberate scope
decision, recorded as a limitation in the README and in `docs/PRD.md`, not an
oversight. Do not expose this server to an untrusted network.

## What the implementation does

- Verifies the server certificate **by default**: the chain *and* the host name,
  including IP literals such as `127.0.0.1`.
- Never overrides a chain that failed validation with a host name match.
- Refuses to start when it has no CA to verify against, instead of accepting
  whatever the server presents.
- Validates every file name before anything is stored: no path separators, no
  `..`, no control characters, no reserved Windows device names, and a length
  bound, so a client cannot write outside the target directory.
- Recomputes the SHA-256 of a stored file after every transfer and deletes the
  file if it does not match the digest the client sent.
- Permits only one writer per destination: a second client asking for a name
  already in use is refused as *busy* instead of overwriting the transfer in
  progress.

## Hardening a deployment

Before running this anywhere that matters:

1. **Replace the development certificate.** The bundled one is self-signed and
   intended for local testing. Issue a certificate for the host the server runs
   on and pass it to the client with `--ca <file>`.
2. **Do not use `--insecure`.** It disables certificate verification and prints a
   warning. It exists for troubleshooting.
3. **Put the server behind a port that is not reachable from the internet.**
   There is no authentication, so reachability is the only access control.
4. **Run it as a user with no more privileges than it needs**, because uploads
   are written to its working directory.
5. **Never commit a key.** `tls_key/`, `*.key`, `*.crt` and `*.pem` are ignored
   by Git, but a key that is committed must be treated as compromised and
   rotated, not merely deleted.

## Out of scope

- Findings that require an attacker who is already an authenticated, permitted
  uploader.
- The absence of authentication and of a download path: these are documented
  limitations, tracked as future work, and will not be treated as
  vulnerabilities.
- Weaknesses in OpenSSL or Boost themselves. Report those upstream; please
  still notify us so a dependency bump can be scheduled.

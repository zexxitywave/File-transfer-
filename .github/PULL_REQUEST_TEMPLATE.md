<!--
Keep the pull request short enough to review. Say what changed and why, then
point at the evidence that it works. Delete the guidance in parentheses before
opening the pull request.
-->

## What and why

<!-- What does this change, and what problem does it solve? If it fixes an
     issue, use "Fixes #123" so it is closed automatically. -->

Closes #

## How it was verified

<!-- Tick what you ran, and paste the interesting output. -->

- [ ] `ctest --test-dir build --output-on-failure` (Windows, full suite)
- [ ] `bash tests/smoke_test.sh build` (Linux)
- [ ] Manual: described below

```
```

## Checklist

- [ ] The change is about one concern, and unrelated reformatting is not included.
- [ ] `clang-format -i src/*.cpp include/*.hpp` has been run on the files I touched.
- [ ] New behaviour has a test case in `tests/run_tests.ps1`, or is documented
      as untested here.
- [ ] Documentation that this change makes wrong has been updated in the same
      pull request (`README.md`, `docs/`, or `CHANGELOG.md` under *Unreleased*).
- [ ] No certificate, key or other secret is included.
- [ ] Layer dependencies still point one way: `main` → `server`/`client` →
      `session` → `protocol`/`checksum`/`logging`.

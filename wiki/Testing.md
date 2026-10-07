# Testing

## Automated tests

Run:

```bash
python -m pytest -v
```

Current validated feature-branch result: **123 passed**.

The suite covers authorization, connectivity fail-closed behavior, discovery, evidence collision safety, credential auditing, wireless capability detection, wireless operation planning, reporting, and existing assessment behavior.

## Python compilation

```bash
python -m compileall -q .
```

Current result: PASS.

## Shell validation

```bash
for f in *.sh; do bash -n "$f"; done
```

All repository shell scripts pass syntax validation.

## Git hygiene

```bash
git diff --check
```

## CI

GitHub Actions executes the automated suite on repository changes. Tests do not require physical wireless hardware or live packet transmission.

## Safety test boundary

Credential tests use mocks/dry-run behavior. Wireless operation tests verify authorization, capability gates, evidence, and the absence of transmission; they do not send deauthentication, handshake-capture, or frame-injection traffic.

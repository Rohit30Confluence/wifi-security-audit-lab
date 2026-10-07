# Wireless Red-Team Operations

The feature branch contains a fail-closed planning layer for authorized wireless assessment workflows.

## Supported operation types

- `deauth`
- `handshake_capture`
- `frame_injection`

These are workflow identifiers, not permission to transmit. The current implementation does not transmit packets.

## Required scope

Every operation requires:

- explicit SSID;
- explicit BSSID;
- authorization reference;
- wireless interface;
- matching authorization record;
- capability result advertising the required monitor-mode state.

Automatic target selection is disabled. Unrestricted frame-injection policy is disabled.

## Evidence

`record_operation_evidence()` stores collision-safe JSON records containing:

- assessment ID;
- timestamp;
- exact target;
- authorization reference;
- interface;
- requested operation;
- execution intent;
- packet backend state;
- transmission state;
- policy/capability details.

## Current stopping point

`packet_backend` is intentionally `NOT_IMPLEMENTED`.

The current evidence state is:

```text
transmission_performed: false
```

A future lab backend must consume the validated plan and independently preserve the same authorization/capability gates. It must not accept arbitrary nearby targets or bypass scope validation.

## Android boundary

Rootless/stock Android cannot be assumed to provide monitor mode or frame injection. Capability detection reports actual host state rather than claiming unsupported features.

## Verification

```bash
python -m pytest -v tests/test_wireless_capability.py tests/test_wireless_operations.py
```

Full branch CI result: **123 passed**.

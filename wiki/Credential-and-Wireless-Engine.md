# Credential and Wireless Assessment Engine

This feature adds guarded credential-audit and wireless-capability infrastructure to the authorized Wi-Fi security assessment framework.

## Credential audit

The credential engine provides:

- Hydra online credential-audit integration.
- John the Ripper offline password-audit integration.
- Authorization validation before subprocess execution.
- Bounded Hydra concurrency from 1–16.
- Dry-run by default.
- Execution timeouts.
- Normalized results suitable for evidence/reporting.

Invalid, missing, empty, malformed, or mismatched authorization blocks execution before the subprocess is started.

## Wireless capability

The capability detector reports:

- available wireless tools;
- detected interfaces;
- supported interface modes;
- monitor-mode readiness;
- discovery-only versus monitor-capable state.

Driver metadata is not treated as proof of frame injection capability.

## Wireless operation planning

The planner accepts explicit:

- SSID
- BSSID
- authorization reference
- interface
- operation type
- capability state

It rejects unauthorized targets, automatic target selection, and unrestricted injection policy.

Supported workflow labels are `deauth`, `handshake_capture`, and `frame_injection`, but the current module only produces validated plans/evidence. It does not transmit those packets.

## Evidence

Operation plans are recorded using collision-safe evidence publication. Records preserve target identity, authorization, operation, execution intent, backend state, and transmission state.

## Android / NetHunter

Stock/rootless Android may expose limited radio capabilities. Monitor mode and injection depend on the hardware, driver, kernel, and permissions. The framework therefore detects actual capabilities at runtime rather than assuming them.

## Verification

The completed branch reports **123 passing tests**. CI does not run live wireless attacks or require physical radios.

## Future work

- [x] Guarded Hydra backend
- [x] Guarded John backend
- [x] Dry-run default
- [x] Wireless capability detection
- [x] Authorization-before-execution tests
- [x] Wireless operation planning
- [x] Collision-safe operation evidence
- [ ] Unified orchestration
- [ ] Evidence adapter for credential results
- [ ] Risk/findings integration
- [ ] External-radio profiles

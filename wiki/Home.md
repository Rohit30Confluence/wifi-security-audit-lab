# Wi-Fi Security Audit Lab — Wiki Home

The project is an authorization-aware Wi-Fi assessment framework for controlled labs, defensive audits, and evidence-backed security testing.

## Current feature state

The project now includes:

- Passive Wi-Fi discovery and security classification
- Explicit BSSID-bound authorization
- Authorized LAN and TCP service assessment
- Collision-safe evidence preservation
- Guarded Hydra and John credential assessment engines
- Wireless radio capability discovery
- Fail-closed wireless operation planning
- Operation evidence recording
- Automated CI validation

The completed credential/wireless feature branch currently reports **123 passing tests**.

## Security boundary

Discovery is observation, not authorization. Active operations must validate the explicit authorization scope before probes or subprocess execution.

Wireless operation types may be represented as assessment plans, but the current implementation does not transmit deauthentication, handshake-capture, or frame-injection traffic. `packet_backend` remains `NOT_IMPLEMENTED`.

## Documentation

- [Architecture](Architecture.md)
- [Methodology](Methodology.md)
- [Credential & Wireless Engine](Credential-and-Wireless-Engine.md)
- [Wireless Red-Team Operations](Wireless-Red-Team-Operations.md)
- [Evidence & Wireless Sessions](Evidence-and-Wireless-Sessions.md)
- [Evidence](Evidence.md)
- [Testing](Testing.md)
- [Status](Status.md)
- [Roadmap](Roadmap.md)
- [Android / Termux Limitations](Android-Termux-Limitations.md)

No synthetic result is presented as live evidence.

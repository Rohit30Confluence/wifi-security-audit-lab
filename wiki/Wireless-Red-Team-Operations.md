# Wireless Red-Team Operations

The branch now has a fail-closed planning layer for authorized wireless assessments.

Supported workflow types are deauth, handshake_capture, and frame_injection. These names describe assessment workflows; the planning module does not transmit packets or perform attacks.

Every request requires an explicit SSID, BSSID, authorization reference, wireless interface, matching authorization record, and a capability result advertising monitor mode.

The planner records target identity, authorization reference, interface, operation, timestamp, execution intent, evidence requirement, and policy state. Automatic target selection and unrestricted frame injection are explicitly disabled.

packet_backend is intentionally NOT_IMPLEMENTED. A future authorized lab backend must consume the validated plan rather than bypass scope validation.

Rootless Android cannot be assumed to provide monitor mode or frame injection. The capability probe reports actual host-advertised capabilities.

Test with: python -m pytest -v tests/test_wireless_capability.py tests/test_wireless_operations.py

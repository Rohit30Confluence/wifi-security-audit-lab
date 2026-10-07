# Architecture

```text
                    ┌─────────────────────────┐
                    │ Android / Linux / Lab   │
                    └────────────┬────────────┘
                                 │
                  ┌──────────────▼──────────────┐
                  │ Discovery & Capability      │
                  │ Wi-Fi / radio / host tools  │
                  └──────────────┬──────────────┘
                                 │
                  ┌──────────────▼──────────────┐
                  │ Authorization / Session      │
                  │ BSSID + authorization_ref    │
                  └──────────────┬──────────────┘
                                 │
          ┌──────────────────────┼──────────────────────┐
          ▼                      ▼                      ▼
   Connectivity          Credential Audit       Wireless Planning
   LAN / TCP              Hydra / John          Guarded operation plan
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 ▼
                    ┌─────────────────────────┐
                    │ Evidence Lifecycle      │
                    │ collision-safe records  │
                    └────────────┬────────────┘
                                 ▼
                    ┌─────────────────────────┐
                    │ Findings / Reports / UI  │
                    └─────────────────────────┘
```

## Core design rules

1. Authorization is validated before active probes or credential subprocesses.
2. SSID discovery never grants authorization.
3. Evidence writes are collision-safe and non-overwriting.
4. Credential execution is bounded and dry-run by default.
5. Wireless capability detection does not imply injection capability.
6. Wireless operation planning is explicit-target and fail-closed.
7. The current wireless planner has no packet-transmission backend.
8. CI uses mocks and does not require live radios.

This separation allows the same framework to operate on Android/Termux while keeping platform limitations explicit.

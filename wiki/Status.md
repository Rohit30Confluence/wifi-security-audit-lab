# Project Status

## Feature branch: credential-and-wireless-assessment-engine

| Capability | Status |
|---|---|
| Passive Wi-Fi discovery | Validated |
| SSID / BSSID / RSSI / frequency | Validated |
| Security classification | Validated |
| Explicit BSSID authorization | Validated |
| Fail-closed active assessment | Validated |
| Authorized LAN discovery | Validated |
| TCP service inventory | Validated |
| Collision-safe evidence | Validated |
| Guarded Hydra credential engine | Validated |
| Guarded John credential engine | Validated |
| Wireless capability detection | Validated |
| Wireless operation planning | Validated |
| Wireless operation evidence | Validated |
| Automated regression suite | **123 passing** |
| Python compilation | Passing |
| Shell syntax checks | Passing |
| GitHub Actions CI | Passing |

## Real-device / Android status

The project has previously been exercised with real Android/Termux telemetry and authorized LAN inventory. Android restrictions remain runtime-dependent; unavailable telemetry is recorded honestly rather than replaced with synthetic results.

## Wireless boundary

The current branch does not include an unrestricted packet backend. `packet_backend=NOT_IMPLEMENTED` and `transmission_performed=false` are intentional safety and audit-state guarantees.

## Next stage

The next engineering stage is orchestration/reporting: one auditable workflow should correlate authorization, capabilities, connectivity, credential assessment, wireless planning, evidence, findings, and final reports.

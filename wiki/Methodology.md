# Assessment Methodology

## Phase 1 — Wireless discovery

Collect observable AP metadata:

- SSID
- BSSID
- RSSI
- frequency/band
- channel information
- security capabilities
- WPS advertisement when exposed

Observation does not authorize active testing.

## Phase 2 — Authorization and session

Before active assessment, validate the explicit BSSID and authorization reference against `authorized_networks.csv`.

Missing, malformed, empty, placeholder, or mismatched authorization fails closed.

## Phase 3 — Connectivity and LAN assessment

For an authorized connected network, collect connection state and derive the available IPv4 scope where platform permissions allow it. Run bounded host and TCP service discovery only inside that scope.

## Phase 4 — Credential assessment

Credential auditing can use guarded Hydra online checks or John offline hash auditing. Authorization is checked before execution, concurrency/timeouts are bounded, and dry-run is the default.

## Phase 5 — Wireless capability and operation planning

Detect wireless interfaces and supported modes. A requested wireless operation must provide explicit SSID, BSSID, interface, authorization reference, and capability evidence.

The current implementation produces a validated operation plan and evidence record only. It does not transmit attack traffic.

## Phase 6 — Evidence

All assessment stages write structured evidence using collision-safe publication. Existing artifacts are never overwritten.

## Phase 7 — Findings and reporting

Evidence is normalized into findings, summaries, dashboards, and future reproducible assessment packages.

## Important distinction

Wireless visibility, network membership, capability, authorization, and execution are separate concepts. The framework keeps those boundaries explicit.

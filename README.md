# Wi-Fi Security Assessment Lab

A defensive, authorization-aware Wi-Fi assessment and audit framework designed for controlled security testing, passive discovery, evidence-backed reporting, and guarded credential/wireless assessment workflows.

Built for defensive security engineers, auditors, red-team practitioners, and students operating in controlled laboratory environments and mobile assessment scenarios (including Termux on Android).

---

## Purpose & Scope

The Wi-Fi Security Assessment Lab demonstrates an evidence-based security auditing workflow:

```text
Discover → Classify → Verify Authorization → Assess → Preserve Evidence → Report
```

### Defensive Boundaries & Authorization Principle

- **Passive observation is not authorization:** Seeing an SSID/BSSID never authorizes probing, association, authentication, credential testing, or packet transmission.
- **Fail-closed authorization:** Active operations require explicit documented authorization. Missing, empty, malformed, invalid, or mismatched authorization fails closed before active probes.
- **BSSID-specific scope binding:** Authorization is bound to the target BSSID. An SSID match alone is only an `SSID_HINT` and never grants permission.
- **Credential testing is guarded:** Hydra online audits and John offline audits validate scope first, use bounded execution, and default to dry-run behavior.
- **Wireless operations are planning-only:** Deauthentication, handshake capture, and frame-injection workflows are represented as guarded operation plans. No unrestricted packet backend is included.
- **Evidence is append-only/collision-safe:** Existing evidence is preserved; concurrent writes receive unique filenames.
- **No real private credentials or private assessment evidence belong in version control.**

---

## Features & Capabilities

- **Passive Wi-Fi Discovery:** Termux:API wireless observation without active probes.
- **Security Classification:** WPA3-SAE, WPA2-PSK, WPA, WEP, and OPEN classification plus band/frequency information.
- **Strict Scope Verification:** Explicit `authorized_networks.csv` validation with no fallback to the example authorization file.
- **Authorized LAN Inventory:** Bounded host and TCP service discovery inside explicitly authorized scope.
- **Credential Assessment Engine:** Guarded Hydra and John integrations with authorization checks, bounded concurrency/timeouts, and dry-run defaults.
- **Wireless Capability Engine:** Detects wireless tools, interfaces, supported modes, and monitor-mode readiness without attack traffic.
- **Wireless Operation Planner:** Explicit SSID/BSSID/interface targeting, authorization gates, capability gates, and collision-safe operation evidence.
- **Evidence Preservation:** Collision-safe, non-overwriting JSON/TXT evidence records with atomic publication.
- **Interactive Dashboards:** Static web consoles for assessment findings, telemetry, and audit metrics.
- **Automated Regression Testing:** **123 tests passing** on the completed feature branch with no physical radio or live-network dependency in CI.

---

## Architecture & Repository Structure

```text
├── .github/workflows/python-tests.yml
├── assessment/
│   ├── authorized_inventory.py
│   ├── authorized_scan.py
│   ├── cli.py
│   ├── connectivity.py
│   ├── credential_audit.py       # Guarded Hydra/John credential auditing
│   ├── discovery.py
│   ├── engine.py
│   ├── evidence.py               # Collision-safe evidence writer
│   ├── executive.py
│   ├── findings.py
│   ├── live.py
│   ├── live_assessment.py
│   ├── live_inventory.py
│   ├── phase6.py
│   ├── presentation.py
│   ├── report.py
│   ├── runner.py
│   ├── services.py
│   ├── session.py                # Authorization/scope lifecycle
│   ├── wireless_capability.py    # Radio capability discovery
│   └── wireless_operations.py    # Guarded wireless operation planning
├── assessment-report/
├── authorized_networks.example.csv
├── index.html
├── public-data/
├── requirements.txt
├── tests/
├── wifi_scan.py
├── wifi_scan.sh
├── wifi-assess.sh
├── wifi-authorized-lan.sh
├── wifi-authorized.sh
├── wifi-live.sh
└── wiki/
```

---

## Supported Platforms & Prerequisites

| Environment | Supported Features | Prerequisites |
| :--- | :--- | :--- |
| **Android / Termux** | Passive Wi-Fi discovery, authorized LAN inventory, capability discovery | Termux, Termux:API, Location enabled for Wi-Fi scans, Python, Nmap where available |
| **Linux / macOS / Windows** | Development, offline assessment engines, tests, reporting, parsing | Python 3.9+, Git, Bash for shell checks |
| **External Wi-Fi radio / NetHunter** | Runtime-dependent wireless capability discovery | Compatible adapter, driver/kernel support, explicit authorized lab scope |

---

## Authorization Configuration

Create the real authorization file locally:

```bash
cp authorized_networks.example.csv authorized_networks.csv
```

The file must contain:

```csv
ssid,bssid,authorization_ref,scope
LAB-NET,02:00:00:00:00:01,AUTH-2026-LAB01,Controlled laboratory assessment
CORP-WIFI,02:00:00:00:00:02,AUTH-2026-CORP02,Authorized internal audit
```

### Scope Rules

- `bssid` must match the target radio.
- SSID-only matches are non-authorizing hints.
- Placeholder references such as `default`, `test`, `none`, `null`, and `authorized-lab` are rejected.
- Missing/empty/malformed authorization fails closed.
- The tool never falls back to `authorized_networks.example.csv`.

---

## Usage

### Passive Wi-Fi Scan

```bash
python3 wifi_scan.py
# or
./wifi_scan.sh
```

Observation only. No active network probing is implied.

### Live Target Assessment

```bash
./wifi-assess.sh --ssid 'LAB-NET' --authorization-ref 'AUTH-2026-LAB01'
```

### Authorized LAN Discovery

```bash
./wifi-authorized-lan.sh AUTH-2026-LAB01
```

### Guarded Credential Assessment

Credential engines require an authorization-validated target. Dry-run is the safe default; execution is bounded and must remain inside the documented assessment scope.

The credential engine supports Hydra online checks for approved protocols and John offline password auditing. Real credentials and private hashes must remain outside version control.

### Wireless Capability / Operation Planning

The wireless capability layer reports actual host capabilities. Wireless operation planning requires explicit SSID, BSSID, interface, authorization reference, and capability validation.

The current branch records plans/evidence only. `packet_backend` is `NOT_IMPLEMENTED` and operation evidence records `transmission_performed: false`.

---

## Automated Testing & Quality Gates

```bash
python3 -m pytest -v
python3 -m compileall -q .
for f in *.sh; do bash -n "$f"; done
git diff --check
```

The completed feature branch currently verifies **123 passing tests**.

---

## CI/CD Pipeline

GitHub Actions runs the Python test workflow on pushes and pull requests. CI installs pytest, runs the complete suite, and keeps wireless/credential tests hardware-independent by using mocks and dry-run behavior.

No live wireless scans or packet-transmission tests are executed in CI.

---

## Documentation Wiki

- [Wiki Home](wiki/Home.md)
- [Architecture](wiki/Architecture.md)
- [Assessment Methodology](wiki/Methodology.md)
- [Testing](wiki/Testing.md)
- [Status](wiki/Status.md)
- [Roadmap](wiki/Roadmap.md)
- [Credential & Wireless Engine](wiki/Credential-and-Wireless-Engine.md)
- [Wireless Red-Team Operations](wiki/Wireless-Red-Team-Operations.md)
- [Evidence & Wireless Sessions](wiki/Evidence-and-Wireless-Sessions.md)
- [Android & Termux Limitations](wiki/Android-Termux-Limitations.md)
- [LAN Inventory](wiki/LAN-Inventory.md)
- [Service Assessment](wiki/Service-Assessment.md)
- [Wi-Fi Discovery](wiki/WiFi-Discovery.md)
- [Evidence](wiki/Evidence.md)

---

## Current Feature-Branch State

The `feature/credential-and-wireless-assessment-engine` branch is complete and CI-verified at **123 tests passed**.

The next planned engineering stage is a unified orchestration/reporting layer that correlates authorization, capability discovery, connectivity, credential assessment, wireless operation planning, evidence, findings, and final reports into one auditable assessment workflow.

The wireless safety boundary remains explicit: no unrestricted deauthentication, arbitrary handshake capture, or unrestricted frame injection backend is included.

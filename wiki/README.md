# Wi-Fi Security Audit Lab — Wiki

## Documentation

- Home
- Status
- Architecture
- Methodology
- Wi-Fi Discovery
- LAN Inventory
- Service Assessment
- Evidence
- Evidence & Wireless Sessions
- Credential & Wireless Engine
- Wireless Red-Team Operations
- Testing
- Android / Termux Limitations
- Roadmap

## Current state

The project has evolved from demonstration reporting into an authorization-aware assessment framework with guarded credential auditing, wireless capability discovery, wireless operation planning, collision-safe evidence, and CI verification.

The completed feature branch currently reports **123 passing tests**.

## Safety boundary

Discovery does not authorize active access. Credential engines validate scope before execution. Wireless operation types are currently planning/evidence workflows only; no unrestricted packet-transmission backend is included.

No synthetic result is presented as live evidence.

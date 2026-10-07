# Android / Termux Limitations

Android exposes a restricted networking environment to unprivileged Termux processes. The assessment framework treats these restrictions as runtime conditions instead of assuming desktop-Linux privileges.

## Observed constraints

- `termux-wifi-scaninfo` provides Wi-Fi scan telemetry when Android permits it.
- `termux-wifi-connectioninfo` provides association information.
- Wi-Fi scanning may require Android Location services to be enabled.
- `ip route`, `ip neigh`, and `/proc/net/*` can be inaccessible.
- Nmap may report limited interfaces/routes when Android does not expose them.
- Rootless Android should not be assumed to provide monitor mode or frame injection.

## Design response

The project:

1. uses Termux:API for Android-specific telemetry;
2. records unavailable data honestly;
3. validates authorization before active assessment;
4. detects wireless capabilities rather than assuming them;
5. keeps wireless operation planning separate from packet transmission.

No synthetic live result is substituted when Android blocks telemetry.

## NetHunter / external radio

Monitor mode and injection are hardware/driver/kernel dependent. Full NetHunter or a compatible external USB radio may expose capabilities unavailable to stock/rootless Android, but the framework still requires explicit authorization and runtime capability validation.

#!/usr/bin/env python3
"""Discover wireless-radio capabilities without transmitting attack traffic."""

from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass
class WirelessInterface:
    name: str
    kind: str
    up: bool
    driver: str | None = None
    chipset: str | None = None


def _run(command: list[str], timeout: int = 5) -> tuple[int, str, str]:
    try:
        p = subprocess.run(
            command, capture_output=True, text=True,
            timeout=timeout, check=False,
        )
        return p.returncode, p.stdout, p.stderr
    except (OSError, subprocess.TimeoutExpired) as exc:
        return -1, "", str(exc)


def _tool(name: str) -> bool:
    return shutil.which(name) is not None


def _interfaces() -> list[WirelessInterface]:
    if not _tool("iw"):
        return []
    rc, out, _ = _run(["iw", "dev"])
    if rc != 0:
        return []

    result: list[WirelessInterface] = []
    current: WirelessInterface | None = None
    for raw in out.splitlines():
        line = raw.strip()
        if line.startswith("Interface "):
            if current:
                result.append(current)
            current = WirelessInterface(
                name=line.split(None, 1)[1], kind="unknown", up=False,
            )
        elif current and line.startswith("type "):
            current.kind = line.split(None, 1)[1]
    if current:
        result.append(current)

    if _tool("ip"):
        for item in result:
            rc, out, _ = _run(["ip", "-o", "link", "show", item.name])
            item.up = rc == 0 and " UP " in f" {out} "
    return result


def _supported_modes() -> list[str]:
    if not _tool("iw"):
        return []
    rc, out, _ = _run(["iw", "list"], timeout=8)
    if rc != 0:
        return []

    modes: list[str] = []
    for line in out.splitlines():
        stripped = line.strip()
        if stripped.startswith("* "):
            value = stripped[2:].strip()
            if value in {
                "managed", "monitor", "AP", "AP/VLAN",
                "P2P-client", "P2P-GO", "P2P-device",
            }:
                modes.append(value)
    return sorted(set(modes))


def collect_capabilities() -> dict[str, Any]:
    interfaces = _interfaces()
    modes = _supported_modes()
    monitor = "monitor" in modes

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "tools": {
            "iw": _tool("iw"),
            "ip": _tool("ip"),
            "lsusb": _tool("lsusb"),
        },
        "interfaces": [asdict(item) for item in interfaces],
        "supported_interface_modes": modes,
        "capabilities": {
            "wireless_discovery": bool(interfaces),
            "monitor_mode": monitor,
            "frame_injection": "unknown",
        },
        "assessment_state": (
            "RADIO_READY_FOR_MONITOR_BACKEND"
            if monitor else "DISCOVERY_ONLY_OR_UNAVAILABLE"
        ),
        "limitations": [
            "Monitor support is inferred from advertised interface modes.",
            "Frame injection is reported as unknown until a backend-specific self-test exists.",
            "No deauthentication, handshake capture, or injection traffic is generated.",
        ],
    }


def main() -> int:
    print(json.dumps(collect_capabilities(), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

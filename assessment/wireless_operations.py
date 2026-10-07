#!/usr/bin/env python3
"""Fail-closed planning for authorized wireless red-team operations."""
from __future__ import annotations
import json, re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any
from assessment.session import validate_scope

_BSSID = re.compile(r"^(?:[0-9a-f]{2}:){5}[0-9a-f]{2}$", re.I)
_ALLOWED = {"deauth", "handshake_capture", "frame_injection"}

@dataclass(frozen=True)
class WirelessOperationPlan:
    operation: str
    ssid: str
    bssid: str
    authorization_ref: str
    interface: str
    execute: bool = False
    status: str = "PLANNED"
    reason: str = ""
    created_at: str = ""

def _validate_request(operation, ssid, bssid, authorization_ref, interface, auth_file, capability):
    if operation not in _ALLOWED: return False, f"Unsupported operation: {operation}"
    if not ssid.strip(): return False, "SSID is required"
    if not _BSSID.fullmatch(bssid.strip()): return False, "A valid target BSSID is required"
    if not interface.strip(): return False, "Wireless interface is required"
    ok, reason = validate_scope(ssid=ssid, bssid=bssid, authorization_ref=authorization_ref, auth_file=auth_file)
    if not ok: return False, reason
    matching = next((x for x in capability.get("interfaces", []) if x.get("name") == interface), None)
    if not matching: return False, f"Interface '{interface}' was not reported by capability discovery"
    if not capability.get("capabilities", {}).get("monitor_mode", False):
        return False, "Monitor mode is not advertised by the wireless capability probe"
    return True, "Authorized target and monitor-capable interface validated"

def plan_operation(*, operation, ssid, bssid, authorization_ref, interface, capability, auth_file=None, execute=False):
    ok, reason = _validate_request(operation, ssid, bssid, authorization_ref, interface, auth_file, capability)
    plan = WirelessOperationPlan(operation, ssid, bssid.lower(), authorization_ref, interface, bool(execute),
        "AUTHORIZED_PLAN" if ok else "BLOCKED", reason, datetime.now(timezone.utc).isoformat())
    result = asdict(plan)
    result.update({
        "packet_backend": "NOT_IMPLEMENTED",
        "transmission_performed": False,
        "evidence_required": True,
        "policy": {
            "authorization_before_active_operation": True,
            "explicit_target_required": True,
            "automatic_target_selection": False,
            "unrestricted_frame_injection": False,
        },
    })
    return result

def main():
    print(json.dumps({"module":"wireless_operations","status":"planning_only",
                      "message":"No wireless packet transmission is implemented by this module."}, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

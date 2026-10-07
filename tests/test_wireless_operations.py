import csv
from assessment.wireless_operations import plan_operation

def _auth_file(tmp_path):
    path = tmp_path / "authorized_networks.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["ssid","bssid","authorization_ref","scope"])
        writer.writeheader()
        writer.writerow({"ssid":"LabAP","bssid":"aa:bb:cc:dd:ee:ff","authorization_ref":"ROE-2026-001","scope":"wireless-lab"})
    return str(path)

def _capability():
    return {"interfaces":[{"name":"wlan1","kind":"managed","up":True}],"capabilities":{"monitor_mode":True}}

def test_unauthorized_target_is_blocked(tmp_path):
    r = plan_operation(operation="deauth", ssid="OtherAP", bssid="11:22:33:44:55:66",
        authorization_ref="ROE-2026-001", interface="wlan1", capability=_capability(), auth_file=_auth_file(tmp_path), execute=True)
    assert r["status"] == "BLOCKED"
    assert r["transmission_performed"] is False

def test_authorized_operation_is_only_a_plan(tmp_path):
    r = plan_operation(operation="handshake_capture", ssid="LabAP", bssid="aa:bb:cc:dd:ee:ff",
        authorization_ref="ROE-2026-001", interface="wlan1", capability=_capability(), auth_file=_auth_file(tmp_path), execute=True)
    assert r["status"] == "AUTHORIZED_PLAN"
    assert r["packet_backend"] == "NOT_IMPLEMENTED"
    assert r["transmission_performed"] is False

def test_injection_is_not_unrestricted(tmp_path):
    r = plan_operation(operation="frame_injection", ssid="LabAP", bssid="aa:bb:cc:dd:ee:ff",
        authorization_ref="ROE-2026-001", interface="wlan1", capability=_capability(), auth_file=_auth_file(tmp_path))
    assert r["policy"]["unrestricted_frame_injection"] is False

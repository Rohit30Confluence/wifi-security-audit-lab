from assessment.wireless_capability import collect_capabilities


def test_wireless_capability_schema(monkeypatch):
    monkeypatch.setattr(
        "assessment.wireless_capability._tool",
        lambda name: name in {"iw", "ip"},
    )
    monkeypatch.setattr(
        "assessment.wireless_capability._interfaces",
        lambda: [],
    )
    monkeypatch.setattr(
        "assessment.wireless_capability._supported_modes",
        lambda: ["managed", "monitor"],
    )
    result = collect_capabilities()
    assert result["capabilities"]["wireless_discovery"] is False
    assert result["capabilities"]["monitor_mode"] is True
    assert result["capabilities"]["frame_injection"] == "unknown"
    assert result["assessment_state"] == "RADIO_READY_FOR_MONITOR_BACKEND"


def test_wireless_capability_does_not_claim_injection(monkeypatch):
    monkeypatch.setattr(
        "assessment.wireless_capability._interfaces", lambda: []
    )
    monkeypatch.setattr(
        "assessment.wireless_capability._supported_modes", lambda: []
    )
    result = collect_capabilities()
    assert result["capabilities"]["frame_injection"] == "unknown"
    assert result["assessment_state"] == "DISCOVERY_ONLY_OR_UNAVAILABLE"

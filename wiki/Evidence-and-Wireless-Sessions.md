# Evidence and Wireless Session Recording

The assessment framework uses collision-safe evidence publication across connectivity, credential, and wireless workflows.

## Guarantees

- assessment and operation identifiers are retained;
- authorization references are recorded;
- repeated writes receive unique filenames;
- existing evidence is never overwritten;
- publication is atomic and flushed before completion;
- operation records include exact SSID/BSSID/interface where applicable;
- wireless operation evidence records `transmission_performed=false` on the current branch;
- no packet capture or credential collection is performed by the evidence writer.

The evidence writer records results; authorization remains the responsibility of the scope/session layer.

## Wireless operation lifecycle

```text
Request
  ↓
Validate scope
  ↓
Check capability
  ↓
Build operation plan
  ↓
Persist collision-safe evidence
  ↓
Report state
```

The current branch stops before packet transmission.

## Verification

```bash
python -m pytest -v tests/test_evidence.py tests/test_wireless_operations.py
```

The full feature branch currently reports **123 tests passed**.

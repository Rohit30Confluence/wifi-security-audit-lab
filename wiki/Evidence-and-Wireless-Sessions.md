# Evidence and Wireless Session Recording

The wireless engine now has a collision-safe metadata evidence writer.

## Guarantees

- required assessment ID, operation, status, and authorization reference
- unique filenames even when multiple records are created within one second
- existing evidence is never overwritten
- atomic file publication
- durable flush before publication
- no packet capture or credential collection is performed by this module

The writer consumes validated operation/session results. It does not authorize operations itself; authorization remains the responsibility of the scope/session layer.

## Test

`python -m pytest -v tests/test_evidence.py tests/test_wireless_operations.py`

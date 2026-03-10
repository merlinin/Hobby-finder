# qualification

Phase 1 / Slice 1 scaffold package.

Purpose: establish architecture shape without changing runtime behavior.

## Slice 5 status
- `port.py` defines the future qualification contract (`QualificationPort`) and a minimal result DTO (`QualificationResult`).
- `stub.py` provides a deterministic placeholder implementation for import/type consistency only.

## Role in Phase 2
In Phase 2, hobby-status decision logic can be implemented behind `QualificationPort` and connected after matching, while keeping the app layer and public API stable.

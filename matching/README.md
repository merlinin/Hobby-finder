# matching

Phase 1 / Slice 1 scaffold package.

Purpose: establish architecture shape without changing runtime behavior.

## Slice 5 status
- `port.py` defines the future matching contract (`MatchingPort`) and a minimal result DTO (`MatchResult`).
- `stub.py` provides a deterministic placeholder implementation for import/type consistency only.

## Role in Phase 2
In Phase 2, production matching logic can be implemented behind `MatchingPort` (normalization, alias lookup, confidence scoring) and then wired through orchestration without changing endpoint contracts.

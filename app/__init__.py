"""Application-layer package scaffold.

This package exists to establish the target architecture in Phase 1 / Slice 1.
To preserve existing behavior and imports, `create_app` is delegated to the
legacy top-level `app.py` module implementation.
"""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


_LEGACY_APP_PATH = Path(__file__).resolve().parent.parent / "app.py"
_SPEC = spec_from_file_location("_legacy_app_module", _LEGACY_APP_PATH)
_LEGACY_APP_MODULE = module_from_spec(_SPEC)
_SPEC.loader.exec_module(_LEGACY_APP_MODULE)

create_app = _LEGACY_APP_MODULE.create_app

__all__ = ["create_app"]

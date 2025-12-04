"""Utility modules for the DOCSYNC package providing configuration, filtering,
and registry functionality.
"""

try:
    from .config import load_config
except ImportError:
    def load_config(path=None):
        return {}

try:
    from .logger import setup_logger
except ImportError:
    import logging
    def setup_logger(name="docsync"):
        return logging.getLogger(name)

try:
    from .validation import validate_path
except ImportError:
    from pathlib import Path
    def validate_path(path, create=False):
        p = Path(path)
        if create:
            p.mkdir(parents=True, exist_ok=True)
        return p.exists()

__all__ = [
    "load_config",
    "setup_logger", 
    "validate_path",
]

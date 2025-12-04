"""Path validation utilities."""

from pathlib import Path


def validate_path(path: Path, create: bool = False) -> bool:
    """Validate and optionally create a path.
    
    Args:
        path: Path to validate
        create: Whether to create the path if it doesn't exist
        
    Returns:
        True if path exists or was created successfully
    """
    if not isinstance(path, Path):
        path = Path(path)
    
    if create and not path.exists():
        path.mkdir(parents=True, exist_ok=True)
    
    return path.exists()

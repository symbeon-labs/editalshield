"""EditalShield Documentation Manager - Simplified DocSync Integration.

This module provides documentation management capabilities for EditalShield,
based on the DocSync project but simplified for generic use.
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class DocumentationManager:
    """Manages documentation structure and organization for EditalShield."""

    def __init__(self, base_path: Path):
        """Initialize the documentation manager.
        
        Args:
            base_path: Root directory of the project
        """
        self.base_path = Path(base_path)
        self.docs_dir = self.base_path / "docs"
        self.src_dir = self.base_path / "src"
        
    def validate_structure(self) -> Dict[str, bool]:
        """Validate documentation structure.
        
        Returns:
            Dict with validation results
        """
        results = {}
        
        # Check required directories
        required_dirs = ["docs", "src", "tests", "examples"]
        for dir_name in required_dirs:
            dir_path = self.base_path / dir_name
            results[f"dir_{dir_name}"] = dir_path.exists()
            
        # Check required files
        required_files = ["README.md", "CONTRIBUTING.md", "LICENSE"]
        for file_name in required_files:
            file_path = self.base_path / file_name
            results[f"file_{file_name}"] = file_path.exists()
            
        return results
    
    def list_documentation_files(self) -> List[Path]:
        """List all documentation files.
        
        Returns:
            List of Path objects for documentation files
        """
        if not self.docs_dir.exists():
            return []
            
        return list(self.docs_dir.rglob("*.md"))
    
    def generate_index(self) -> str:
        """Generate documentation index.
        
        Returns:
            Markdown string with documentation index
        """
        files = self.list_documentation_files()
        
        index = "# Índice de Documentação\n\n"
        
        # Group by directory
        by_dir: Dict[str, List[Path]] = {}
        for file in files:
            rel_path = file.relative_to(self.docs_dir)
            dir_name = str(rel_path.parent) if rel_path.parent != Path(".") else "root"
            
            if dir_name not in by_dir:
                by_dir[dir_name] = []
            by_dir[dir_name].append(file)
        
        # Generate index
        for dir_name in sorted(by_dir.keys()):
            index += f"\n## {dir_name}\n\n"
            for file in sorted(by_dir[dir_name]):
                rel_path = file.relative_to(self.docs_dir)
                file_name = file.stem.replace("_", " ").title()
                index += f"- [{file_name}]({rel_path})\n"
        
        return index
    
    def sync(self) -> Dict[str, int]:
        """Synchronize documentation.
        
        Returns:
            Statistics about synchronization
        """
        stats = {
            "files_found": 0,
            "files_validated": 0,
            "errors": 0
        }
        
        files = self.list_documentation_files()
        stats["files_found"] = len(files)
        
        for file in files:
            try:
                # Validate file can be read
                content = file.read_text(encoding="utf-8")
                if content:
                    stats["files_validated"] += 1
            except Exception as e:
                logger.error(f"Error validating {file}: {e}")
                stats["errors"] += 1
        
        return stats


def sync_documentation(base_path: Optional[Path] = None) -> Dict[str, int]:
    """Sync documentation for EditalShield.
    
    Args:
        base_path: Base path of the project (defaults to current directory)
        
    Returns:
        Synchronization statistics
    """
    if base_path is None:
        base_path = Path.cwd()
    
    manager = DocumentationManager(base_path)
    return manager.sync()


def validate_documentation(base_path: Optional[Path] = None) -> Dict[str, bool]:
    """Validate documentation structure.
    
    Args:
        base_path: Base path of the project (defaults to current directory)
        
    Returns:
        Validation results
    """
    if base_path is None:
        base_path = Path.cwd()
    
    manager = DocumentationManager(base_path)
    return manager.validate_structure()


def generate_documentation_index(base_path: Optional[Path] = None) -> str:
    """Generate documentation index.
    
    Args:
        base_path: Base path of the project (defaults to current directory)
        
    Returns:
        Markdown index
    """
    if base_path is None:
        base_path = Path.cwd()
    
    manager = DocumentationManager(base_path)
    return manager.generate_index()

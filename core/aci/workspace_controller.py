"""
Agent-Computer Interface (ACI) Workspace Controller (Chapter 15)
Provides deterministic, bounded file-system manipulation and workspace navigation.
"""

from __future__ import annotations

from pathlib import Path
from pydantic import BaseModel


class FileStats(BaseModel):
    path: str
    size_bytes: int
    is_directory: bool


class WorkspaceController:
    """
    Safely sandboxes workspace modifications to prevent directory traversal escapes.
    """

    def __init__(self, root_dir: str | Path):
        self.root = Path(root_dir).resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def _resolve_safe(self, rel_path: str) -> Path:
        target = (self.root / rel_path).resolve()
        if not str(target).startswith(str(self.root)):
            raise PermissionError(f"Directory traversal escape detected for path '{rel_path}'")
        return target

    def list_files(self, sub_path: str = "") -> list[FileStats]:
        target = self._resolve_safe(sub_path)
        if not target.exists():
            return []
        items = []
        for p in target.iterdir():
            items.append(FileStats(
                path=str(p.relative_to(self.root)),
                size_bytes=p.stat().st_size if p.is_file() else 0,
                is_directory=p.is_dir(),
            ))
        return items

    def write_file(self, rel_path: str, content: str) -> None:
        target = self._resolve_safe(rel_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    def read_file(self, rel_path: str) -> str:
        target = self._resolve_safe(rel_path)
        if not target.exists() or not target.is_file():
            raise FileNotFoundError(f"File '{rel_path}' not found")
        return target.read_text(encoding="utf-8")

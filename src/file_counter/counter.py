"""Core file counting logic."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class FileStats:
    """File counting statistics.

    Attributes:
        total: Total number of files counted
        by_extension: Dictionary mapping file extension to count
    """

    total: int
    by_extension: dict[str, int]


class FileCounter:
    """Count files in a directory, grouped by extension.

    Attributes:
        directory: Path to the directory to count files in
        recursive: Whether to recursively scan subdirectories
        include_hidden: Whether to include hidden files (starting with .)
    """

    def __init__(self, directory: Path, recursive: bool, include_hidden: bool) -> None:
        """Initialize the FileCounter.

        Args:
            directory: Path to the directory to count files in
            recursive: Whether to recursively scan subdirectories
            include_hidden: Whether to include hidden files
        """
        self.directory = directory
        self.recursive = recursive
        self.include_hidden = include_hidden

    def count(self) -> FileStats:
        """Count files in the directory.

        Returns:
            FileStats containing total count and extension breakdown

        Raises:
            FileNotFoundError: If directory does not exist
            NotADirectoryError: If path is not a directory
        """
        if not self.directory.exists():
            raise FileNotFoundError(f"Directory not found: {self.directory}")

        if not self.directory.is_dir():
            raise NotADirectoryError(f"Path is not a directory: {self.directory}")

        by_extension: dict[str, int] = {}
        total = 0

        # Get all files based on recursive flag
        if self.recursive:
            files = self.directory.rglob("*")
        else:
            files = self.directory.iterdir()

        for file_path in files:
            # Skip directories
            if file_path.is_dir():
                continue

            # Skip hidden files if not included
            if not self.include_hidden and file_path.name.startswith("."):
                continue

            # Get file extension
            extension = file_path.suffix

            # Count files
            by_extension[extension] = by_extension.get(extension, 0) + 1
            total += 1

        return FileStats(total=total, by_extension=by_extension)

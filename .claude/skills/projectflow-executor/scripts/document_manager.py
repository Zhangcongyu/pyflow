"""
Document Manager

Manages versioned requirements documents for ProjectFlow.
"""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Literal


class DocumentManager:
    """
    Manages versioned requirements and constitution documents.

    This class handles:
    - Creating versioned requirements documents
    - Reading versioned documents
    - Migrating from old shared structure
    """

    def __init__(self, pjflow_root: Path):
        """
        Initialize the document manager.

        Args:
            pjflow_root: Path to the pjflow directory
        """
        self.pjflow_root = Path(pjflow_root)
        self.pjflow_root.mkdir(parents=True, exist_ok=True)

    @property
    def constitution_path(self) -> Path:
        """Path to the shared constitution document."""
        return self.pjflow_root / "constitution.md"

    def get_version_dir(self, version_name: str) -> Path:
        """
        Get the path to a version directory.

        Args:
            version_name: Name of the version (e.g., "v0_initial", "v1_add_feature")

        Returns:
            Path to the version directory
        """
        version_dir = self.pjflow_root / version_name
        version_dir.mkdir(parents=True, exist_ok=True)
        return version_dir

    def get_requirements_path(self, version_name: str) -> Path:
        """
        Get the path to a versioned requirements document.

        Args:
            version_name: Name of the version

        Returns:
            Path to the requirements document
        """
        return self.get_version_dir(version_name) / "requirements.md"

    def get_compliance_report_path(self, version_name: str) -> Path:
        """
        Get the path to a versioned compliance report.

        Args:
            version_name: Name of the version

        Returns:
            Path to the compliance report
        """
        return self.get_version_dir(version_name) / "compliance_report.md"

    def create_versioned_requirements(
        self,
        version_name: str,
        content: str,
        overwrite: bool = False,
    ) -> Path:
        """
        Create a versioned requirements document.

        Args:
            version_name: Name of the version
            content: Content of the requirements document
            overwrite: Whether to overwrite if exists

        Returns:
            Path to the created document

        Raises:
            FileExistsError: If file exists and overwrite is False
        """
        requirements_path = self.get_requirements_path(version_name)

        if requirements_path.exists() and not overwrite:
            raise FileExistsError(
                f"Requirements document already exists: {requirements_path}"
            )

        requirements_path.parent.mkdir(parents=True, exist_ok=True)
        requirements_path.write_text(content, encoding="utf-8")

        return requirements_path

    def read_requirements(self, version_name: str) -> str | None:
        """
        Read a versioned requirements document.

        Args:
            version_name: Name of the version

        Returns:
            Content of the requirements document, or None if not found
        """
        requirements_path = self.get_requirements_path(version_name)

        if not requirements_path.exists():
            return None

        return requirements_path.read_text(encoding="utf-8")

    def read_constitution(self) -> str | None:
        """
        Read the shared constitution document.

        Returns:
            Content of the constitution document, or None if not found
        """
        if not self.constitution_path.exists():
            return None

        return self.constitution_path.read_text(encoding="utf-8")

    def list_versions(self) -> list[str]:
        """
        List all version directories.

        Returns:
            List of version names sorted by version number
        """
        versions = []

        for item in self.pjflow_root.iterdir():
            if item.is_dir() and item.name.startswith("v"):
                versions.append(item.name)

        # Sort by version number (v0, v1, v2, etc.)
        versions.sort(key=lambda v: int(v.split("_")[0][1:]) if "_" in v else 0)

        return versions

    def get_latest_version(self) -> str | None:
        """
        Get the latest version directory name.

        Returns:
            Latest version name, or None if no versions exist
        """
        versions = self.list_versions()
        return versions[-1] if versions else None

    def detect_structure_type(self) -> Literal["old", "new", "empty"]:
        """
        Detect whether the project uses old or new structure.

        Returns:
            "old" if using shared requirements.md
            "new" if using versioned structure
            "empty" if pjflow directory doesn't exist or is empty
        """
        if not self.pjflow_root.exists():
            return "empty"

        # Check for old shared requirements.md
        old_requirements = self.pjflow_root / "requirements.md"
        if old_requirements.exists():
            # Check if there are also version directories
            versions = self.list_versions()
            if versions:
                return "new"  # Has both, treat as new
            return "old"

        # Check for version directories
        versions = self.list_versions()
        if versions:
            return "new"

        return "empty"

    def migrate_from_old_structure(self) -> dict[str, str]:
        """
        Migrate from old shared structure to new versioned structure.

        This will:
        1. Copy shared requirements.md to each existing version directory
        2. Rename old requirements.md to requirements.md.bak

        Returns:
            Dictionary mapping version names to migration status

        Raises:
            RuntimeError: If structure is not old
        """
        structure_type = self.detect_structure_type()

        if structure_type != "old":
            raise RuntimeError(
                f"Cannot migrate: current structure is '{structure_type}', not 'old'"
            )

        old_requirements = self.pjflow_root / "requirements.md"

        if not old_requirements.exists():
            raise RuntimeError("Old requirements.md not found")

        requirements_content = old_requirements.read_text(encoding="utf-8")

        results = {}
        versions = self.list_versions()

        if not versions:
            # No versions exist, create v0_initial
            version_dir = self.get_version_dir("v0_initial")
            version_dir.mkdir(parents=True, exist_ok=True)

            requirements_path = version_dir / "requirements.md"
            requirements_path.write_text(requirements_content, encoding="utf-8")

            results["v0_initial"] = "created"

        else:
            # Copy to existing versions
            for version in versions:
                requirements_path = self.get_requirements_path(version)
                requirements_path.write_text(requirements_content, encoding="utf-8")
                results[version] = "migrated"

        # Backup old file
        backup_path = old_requirements.with_suffix(".md.bak")
        shutil.copy2(old_requirements, backup_path)
        old_requirements.unlink()

        results["_backup"] = str(backup_path)

        return results


def create_requirements_template(
    goal: str,
    project_type: Literal["new", "add-feature"],
    complexity: Literal["simple", "medium", "complex"],
) -> str:
    """
    Create a requirements document template.

    Args:
        goal: User's goal for this version
        project_type: Whether this is a new project or adding features
        complexity: Project complexity level

    Returns:
        Markdown formatted requirements template
    """
    md = "# Requirements\n\n"
    md += f"**Project Type**: {project_type}\n\n"
    md += f"**Complexity**: {complexity}\n\n"
    md += f"**Goal**: {goal}\n\n"
    md += "---\n\n"

    if project_type == "new":
        md += "## Project Overview\n\n"
        md += "Describe the overall purpose and scope of this project.\n\n"

        md += "## Core Features\n\n"
        md += "### Feature 1\n"
        md += "- Description:\n"
        md += "- Acceptance Criteria:\n"
        md += "- Priority:\n\n"

        md += "## Technical Requirements\n\n"
        md += "- Performance requirements:\n"
        md += "- Security requirements:\n"
        md += "- Compatibility requirements:\n\n"

        md += "## Success Criteria\n\n"
        md += "1. \n"
        md += "2. \n"
        md += "3. \n\n"

    else:  # add-feature
        md += "## Feature Overview\n\n"
        md += "Describe the new feature(s) being added.\n\n"

        md += "## Changes Required\n\n"
        md += "### New Files\n"
        md += "- \n\n"

        md += "### Modified Files\n"
        md += "- \n\n"

        md += "## Acceptance Criteria\n\n"
        md += "1. \n"
        md += "2. \n"
        md += "3. \n\n"

        md += "## Testing Requirements\n\n"
        md += "- Unit tests:\n"
        md += "- Integration tests:\n\n"

    md += "---\n\n"
    md += f"*Created: {project_type} - {complexity}*\n"

    return md

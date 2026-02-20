"""Tests for document manager."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

# Add parent directory to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.document_manager import (
    DocumentManager,
    create_requirements_template,
)


class TestCreateRequirementsTemplate:
    """Tests for create_requirements_template function."""

    def test_create_new_project_template(self):
        """Test creating template for new project."""
        template = create_requirements_template(
            goal="Create a todo app",
            project_type="new",
            complexity="simple",
        )
        assert "# Requirements" in template
        assert "Create a todo app" in template
        assert "new" in template
        assert "simple" in template

    def test_create_add_feature_template(self):
        """Test creating template for feature addition."""
        template = create_requirements_template(
            goal="Add user authentication",
            project_type="add-feature",
            complexity="medium",
        )
        assert "Add user authentication" in template
        assert "add-feature" in template
        assert "medium" in template


class TestDocumentManager:
    """Tests for DocumentManager class."""

    def test_initialization(self, tmp_path: Path):
        """Test DocumentManager initialization."""
        manager = DocumentManager(tmp_path)
        assert manager.pjflow_root == tmp_path

    def test_create_versioned_requirements_new(self, tmp_path: Path):
        """Test creating new versioned requirements."""
        manager = DocumentManager(tmp_path)
        content = create_requirements_template(
            goal="Test goal",
            project_type="new",
            complexity="simple",
        )

        manager.create_versioned_requirements("v0_initial", content)

        version_dir = tmp_path / "v0_initial"
        assert version_dir.exists()
        req_file = version_dir / "requirements.md"
        assert req_file.exists()
        assert "Test goal" in req_file.read_text()

    def test_create_versioned_requirements_exists_no_overwrite(self, tmp_path: Path):
        """Test that existing requirements are not overwritten by default."""
        manager = DocumentManager(tmp_path)

        # Create initial file
        version_dir = tmp_path / "v0_initial"
        version_dir.mkdir(exist_ok=True)
        req_file = version_dir / "requirements.md"
        req_file.write_text("# Original content")

        # Try to create new content - should raise FileExistsError
        with pytest.raises(FileExistsError):
            manager.create_versioned_requirements(
                "v0_initial", "# New content", overwrite=False
            )

        # Should still have original content
        assert "Original content" in req_file.read_text()
        assert "New content" not in req_file.read_text()

    def test_create_versioned_requirements_overwrite(self, tmp_path: Path):
        """Test overwriting existing requirements."""
        manager = DocumentManager(tmp_path)

        # Create initial file
        version_dir = tmp_path / "v0_initial"
        version_dir.mkdir(exist_ok=True)
        req_file = version_dir / "requirements.md"
        req_file.write_text("# Original content")

        # Overwrite with new content
        manager.create_versioned_requirements(
            "v0_initial", "# New content", overwrite=True
        )

        # Should have new content
        assert "New content" in req_file.read_text()
        assert "Original content" not in req_file.read_text()

    def test_read_versioned_requirements(self, tmp_path: Path):
        """Test reading versioned requirements."""
        manager = DocumentManager(tmp_path)

        # Create requirements file
        version_dir = tmp_path / "v0_initial"
        version_dir.mkdir(exist_ok=True)
        req_file = version_dir / "requirements.md"
        req_file.write_text("# Test content")

        content = manager.read_requirements("v0_initial")
        assert content == "# Test content"

    def test_read_versioned_requirements_missing(self, tmp_path: Path):
        """Test reading missing requirements returns None."""
        manager = DocumentManager(tmp_path)
        content = manager.read_requirements("v0_initial")
        assert content is None

    def test_list_versions(self, tmp_path: Path):
        """Test listing version directories."""
        manager = DocumentManager(tmp_path)

        # Create version directories
        (tmp_path / "v0_initial").mkdir(exist_ok=True)
        (tmp_path / "v1_add_feature").mkdir(exist_ok=True)
        (tmp_path / "other_dir").mkdir(exist_ok=True)

        versions = manager.list_versions()
        assert set(versions) == {"v0_initial", "v1_add_feature"}

    def test_migrate_from_old_structure(self, tmp_path: Path):
        """Test migrating from old shared requirements structure."""
        manager = DocumentManager(tmp_path)

        # Create old structure
        (tmp_path / "requirements.md").write_text("# Old shared requirements")

        # Create some version directories
        (tmp_path / "v0_initial").mkdir(exist_ok=True)
        (tmp_path / "v1_add_feature").mkdir(exist_ok=True)

        # Migrate
        migrated = manager.migrate_from_old_structure()

        assert migrated is True
        # Old file should be removed
        assert not (tmp_path / "requirements.md").exists()
        # Each version should have its own copy
        assert "Old shared requirements" in (
            tmp_path / "v0_initial" / "requirements.md"
        ).read_text()
        assert "Old shared requirements" in (
            tmp_path / "v1_add_feature" / "requirements.md"
        ).read_text()

    def test_migrate_from_old_structure_no_old_file(self, tmp_path: Path):
        """Test migration when no old file exists."""
        manager = DocumentManager(tmp_path)
        migrated = manager.migrate_from_old_structure()
        assert migrated is False


@pytest.fixture
def tmp_path() -> Path:
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmp:
        yield Path(tmp)

"""Tests for file-counter module."""

from __future__ import annotations

from pathlib import Path

import pytest
from click.testing import CliRunner

from file_counter.cli import main
from file_counter.counter import FileCounter, FileStats


class TestFileStats:
    """Test FileStats data class."""

    def test_file_stats_creation(self) -> None:
        """Test creating FileStats instance."""
        stats = FileStats(total=100, by_extension={".py": 10, ".md": 5})
        assert stats.total == 100
        assert stats.by_extension == {".py": 10, ".md": 5}

    def test_file_stats_empty(self) -> None:
        """Test FileStats with empty results."""
        stats = FileStats(total=0, by_extension={})
        assert stats.total == 0
        assert stats.by_extension == {}


class TestFileCounter:
    """Test FileCounter core logic."""

    def test_count_files_in_empty_directory(self, tmp_path: Path) -> None:
        """Test counting files in an empty directory."""
        counter = FileCounter(tmp_path, recursive=False, include_hidden=False)
        stats = counter.count()
        assert stats.total == 0
        assert stats.by_extension == {}

    def test_count_files_single_file(self, tmp_path: Path) -> None:
        """Test counting a single file."""
        test_file = tmp_path / "test.py"
        test_file.write_text("print('hello')")

        counter = FileCounter(tmp_path, recursive=False, include_hidden=False)
        stats = counter.count()
        assert stats.total == 1
        assert stats.by_extension == {".py": 1}

    def test_count_files_multiple_extensions(self, tmp_path: Path) -> None:
        """Test counting files with different extensions."""
        (tmp_path / "test.py").write_text("")
        (tmp_path / "test.md").write_text("")
        (tmp_path / "test.txt").write_text("")
        (tmp_path / "no_extension").write_text("")

        counter = FileCounter(tmp_path, recursive=False, include_hidden=False)
        stats = counter.count()
        assert stats.total == 4
        assert stats.by_extension == {".py": 1, ".md": 1, ".txt": 1, "": 1}

    def test_count_files_recursive(self, tmp_path: Path) -> None:
        """Test recursive file counting."""
        (tmp_path / "root.py").write_text("")
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (subdir / "sub.py").write_text("")
        (subdir / "sub.md").write_text("")

        counter = FileCounter(tmp_path, recursive=True, include_hidden=False)
        stats = counter.count()
        assert stats.total == 3
        assert stats.by_extension == {".py": 2, ".md": 1}

    def test_count_files_non_recursive(self, tmp_path: Path) -> None:
        """Test non-recursive file counting."""
        (tmp_path / "root.py").write_text("")
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (subdir / "sub.py").write_text("")

        counter = FileCounter(tmp_path, recursive=False, include_hidden=False)
        stats = counter.count()
        assert stats.total == 1
        assert stats.by_extension == {".py": 1}

    def test_count_files_exclude_hidden(self, tmp_path: Path) -> None:
        """Test excluding hidden files."""
        (tmp_path / "visible.py").write_text("")
        (tmp_path / ".hidden.py").write_text("")

        counter = FileCounter(tmp_path, recursive=False, include_hidden=False)
        stats = counter.count()
        assert stats.total == 1
        assert stats.by_extension == {".py": 1}

    def test_count_files_include_hidden(self, tmp_path: Path) -> None:
        """Test including hidden files."""
        (tmp_path / "visible.py").write_text("")
        (tmp_path / ".hidden.py").write_text("")

        counter = FileCounter(tmp_path, recursive=False, include_hidden=True)
        stats = counter.count()
        assert stats.total == 2
        assert stats.by_extension == {".py": 2}

    def test_count_files_recursive_with_hidden(self, tmp_path: Path) -> None:
        """Test recursive counting with hidden files."""
        (tmp_path / "root.py").write_text("")
        (tmp_path / ".root_hidden.py").write_text("")

        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (subdir / "sub.py").write_text("")
        (subdir / ".sub_hidden.py").write_text("")

        counter = FileCounter(tmp_path, recursive=True, include_hidden=True)
        stats = counter.count()
        assert stats.total == 4
        assert stats.by_extension == {".py": 4}

    def test_count_files_directory_not_found(self, tmp_path: Path) -> None:
        """Test counting files in non-existent directory."""
        non_existent = tmp_path / "non_existent"
        counter = FileCounter(non_existent, recursive=False, include_hidden=False)

        with pytest.raises(FileNotFoundError):
            counter.count()

    def test_count_files_path_is_file(self, tmp_path: Path) -> None:
        """Test counting when path points to a file, not directory."""
        test_file = tmp_path / "test.py"
        test_file.write_text("")

        counter = FileCounter(test_file, recursive=False, include_hidden=False)
        with pytest.raises(NotADirectoryError):
            counter.count()


class TestCLI:
    """Test CLI interface."""

    def test_cli_help(self) -> None:
        """Test CLI help message."""
        runner = CliRunner()
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "File Counter" in result.output
        assert "--directory" in result.output
        assert "--recursive" in result.output
        assert "--hidden" in result.output

    def test_cli_with_directory(self, tmp_path: Path) -> None:
        """Test CLI with directory argument."""
        (tmp_path / "test.py").write_text("")

        runner = CliRunner()
        result = runner.invoke(main, ["--directory", str(tmp_path)])
        assert result.exit_code == 0
        assert "Total files: 1" in result.output
        assert ".py: 1 files" in result.output

    def test_cli_recursive_flag(self, tmp_path: Path) -> None:
        """Test CLI with recursive flag."""
        (tmp_path / "root.py").write_text("")
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (subdir / "sub.py").write_text("")

        runner = CliRunner()

        # Without recursive
        result = runner.invoke(main, ["--directory", str(tmp_path)])
        assert result.exit_code == 0
        assert "Total files: 1" in result.output

        # With recursive
        result = runner.invoke(main, ["--directory", str(tmp_path), "--recursive"])
        assert result.exit_code == 0
        assert "Total files: 2" in result.output

    def test_cli_hidden_flag(self, tmp_path: Path) -> None:
        """Test CLI with hidden flag."""
        (tmp_path / "visible.py").write_text("")
        (tmp_path / ".hidden.py").write_text("")

        runner = CliRunner()

        # Without hidden
        result = runner.invoke(main, ["--directory", str(tmp_path)])
        assert result.exit_code == 0
        assert "Total files: 1" in result.output

        # With hidden
        result = runner.invoke(main, ["--directory", str(tmp_path), "--hidden"])
        assert result.exit_code == 0
        assert "Total files: 2" in result.output

    def test_cli_non_existent_directory(self, tmp_path: Path) -> None:
        """Test CLI with non-existent directory."""
        non_existent = tmp_path / "non_existent"

        runner = CliRunner()
        result = runner.invoke(main, ["--directory", str(non_existent)])
        assert result.exit_code != 0
        assert "Error" in result.output or "not found" in result.output

    def test_cli_output_format(self, tmp_path: Path) -> None:
        """Test CLI output format."""
        (tmp_path / "test.py").write_text("")
        (tmp_path / "test.md").write_text("")

        runner = CliRunner()
        result = runner.invoke(main, ["--directory", str(tmp_path)])
        assert result.exit_code == 0
        assert "File Counter Results" in result.output
        assert "Total files: 2" in result.output
        assert ".py: 1 files" in result.output
        assert ".md: 1 files" in result.output

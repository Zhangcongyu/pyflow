"""Tests for base compliance checker."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

# Add parent directory to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.base_checker import (
    BaseComplianceChecker,
    ComplianceIssue,
    ComplianceResult,
    SeverityLevel,
)


class DummyComplianceChecker(BaseComplianceChecker):
    """Dummy checker for testing."""

    @property
    def language_name(self) -> str:
        return "dummy"

    @property
    def checker_name(self) -> str:
        return "Dummy Checker"

    def check_code_style(self) -> list[ComplianceIssue]:
        return []

    def check_type_annotations(self) -> list[ComplianceIssue]:
        return []

    def check_test_coverage(self) -> list[ComplianceIssue]:
        return []

    def check_error_handling(self) -> list[ComplianceIssue]:
        return []


class TestComplianceIssue:
    """Tests for ComplianceIssue dataclass."""

    def test_create_minimal_issue(self):
        """Test creating a minimal compliance issue."""
        issue = ComplianceIssue(
            rule_id="TEST001",
            severity=SeverityLevel.MEDIUM,
            category="test",
            message="Test message",
        )
        assert issue.rule_id == "TEST001"
        assert issue.severity == SeverityLevel.MEDIUM
        assert issue.category == "test"
        assert issue.message == "Test message"
        assert issue.file_path is None
        assert issue.line_number is None

    def test_create_full_issue(self):
        """Test creating a full compliance issue with all fields."""
        issue = ComplianceIssue(
            rule_id="TEST002",
            severity=SeverityLevel.HIGH,
            category="code_style",
            message="Test error",
            file_path="src/main.py",
            line_number=42,
            column_number=10,
            context="x = 1",
            fix_suggestion="Change to x = 2",
        )
        assert issue.file_path == "src/main.py"
        assert issue.line_number == 42
        assert issue.column_number == 10
        assert issue.context == "x = 1"
        assert issue.fix_suggestion == "Change to x = 2"


class TestComplianceResult:
    """Tests for ComplianceResult dataclass."""

    def test_create_result(self):
        """Test creating a compliance result."""
        issues = [
            ComplianceIssue(
                rule_id="TEST001",
                severity=SeverityLevel.HIGH,
                category="test",
                message="Issue 1",
            ),
            ComplianceIssue(
                rule_id="TEST002",
                severity=SeverityLevel.MEDIUM,
                category="test",
                message="Issue 2",
            ),
        ]
        result = ComplianceResult(
            checker_name="Test Checker",
            language="python",
            passed=True,
            issues=issues,
        )
        assert result.checker_name == "Test Checker"
        assert result.language == "python"
        assert len(result.issues) == 2
        assert result.total_issues == 2
        assert result.critical_count == 0
        assert result.high_count == 1
        assert result.medium_count == 1
        assert result.low_count == 0
        assert result.has_critical is False
        assert result.has_high is True

    def test_result_with_critical_issue(self):
        """Test result with critical issue."""
        issues = [
            ComplianceIssue(
                rule_id="CRIT001",
                severity=SeverityLevel.CRITICAL,
                category="test",
                message="Critical issue",
            )
        ]
        result = ComplianceResult(
            checker_name="Test Checker",
            language="python",
            passed=False,
            issues=issues,
        )
        assert result.critical_count == 1
        assert result.has_critical is True


class TestBaseComplianceChecker:
    """Tests for BaseComplianceChecker."""

    def test_initialization(self, tmp_path: Path):
        """Test checker initialization."""
        checker = DummyComplianceChecker(tmp_path)
        assert checker.project_root == tmp_path
        assert checker.language_name == "dummy"
        assert checker.checker_name == "Dummy Checker"

    def test_check_constitution_compliance_missing_file(self, tmp_path: Path):
        """Test constitution check with missing file."""
        checker = DummyComplianceChecker(tmp_path)
        issues = checker.check_constitution_compliance()
        assert len(issues) == 1
        assert issues[0].rule_id == "CONSTITUTION_MISSING"
        assert issues[0].severity == SeverityLevel.CRITICAL

    def test_check_constitution_compliance_empty_file(self, tmp_path: Path):
        """Test constitution check with empty file."""
        (tmp_path / "constitution.md").write_text("")
        checker = DummyComplianceChecker(tmp_path)
        issues = checker.check_constitution_compliance()
        assert len(issues) == 1
        assert issues[0].rule_id == "CONSTITUTION_EMPTY"

    def test_check_constitution_compliance_valid(self, tmp_path: Path):
        """Test constitution check with valid file."""
        (tmp_path / "constitution.md").write_text("# Project Constitution\n\n## Rules\n- Rule 1")
        checker = DummyComplianceChecker(tmp_path)
        issues = checker.check_constitution_compliance()
        assert len(issues) == 0

    def test_check_requirements_compliance_missing_version_dir(self, tmp_path: Path):
        """Test requirements check with missing version directory."""
        checker = DummyComplianceChecker(tmp_path)
        issues = checker.check_requirements_compliance("v0_initial")
        assert len(issues) == 1
        assert issues[0].rule_id == "REQUIREMENTS_MISSING"

    def test_check_requirements_compliance_missing_file(self, tmp_path: Path):
        """Test requirements check with missing file."""
        (tmp_path / "v0_initial").mkdir(exist_ok=True)
        checker = DummyComplianceChecker(tmp_path)
        issues = checker.check_requirements_compliance("v0_initial")
        assert len(issues) == 1
        assert issues[0].rule_id == "REQUIREMENTS_FILE_MISSING"

    def test_check_requirements_compliance_valid(self, tmp_path: Path):
        """Test requirements check with valid file."""
        version_dir = tmp_path / "v0_initial"
        version_dir.mkdir(exist_ok=True)
        (version_dir / "requirements.md").write_text("# Requirements\n\n## Feature 1\nDescription")
        checker = DummyComplianceChecker(tmp_path)
        issues = checker.check_requirements_compliance("v0_initial")
        assert len(issues) == 0

    def test_run_all_checks(self, tmp_path: Path):
        """Test running all checks."""
        # Setup
        (tmp_path / "constitution.md").write_text("# Constitution")
        version_dir = tmp_path / "v0_initial"
        version_dir.mkdir(exist_ok=True)
        (version_dir / "requirements.md").write_text("# Requirements")

        checker = DummyComplianceChecker(tmp_path)
        result = checker.run_all_checks("v0_initial")

        assert result.checker_name == "Dummy Checker"
        assert result.language == "dummy"
        assert result.total_issues == 0
        assert result.passed is True


@pytest.fixture
def tmp_path() -> Path:
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmp:
        yield Path(tmp)

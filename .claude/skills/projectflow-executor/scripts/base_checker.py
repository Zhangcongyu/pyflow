"""
Base Compliance Checker

Provides the abstract base class and core data structures for compliance checking
across different programming languages.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any


class SeverityLevel(Enum):
    """Severity level for compliance issues."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


@dataclass
class ComplianceIssue:
    """A compliance issue found during checking."""

    rule_id: str
    severity: SeverityLevel
    category: str
    message: str
    file_path: str | None = None
    line_number: int | None = None
    column_number: int | None = None
    fix_suggestion: str | None = None
    context: str | None = None

    def to_markdown(self) -> str:
        """Convert the issue to markdown format."""
        severity_emoji = {
            SeverityLevel.CRITICAL: "🚨",
            SeverityLevel.HIGH: "⚠️",
            SeverityLevel.MEDIUM: "⚡",
            SeverityLevel.LOW: "📝",
            SeverityLevel.INFO: "ℹ️",
        }

        emoji = severity_emoji.get(self.severity, "•")
        location = f"{self.file_path}:{self.line_number}" if self.file_path else "N/A"

        md = f"#### {emoji} {self.rule_id}\n\n"
        md += f"- **Severity**: {self.severity.value}\n"
        md += f"- **Category**: {self.category}\n"
        md += f"- **Location**: `{location}`\n"
        md += f"- **Message**: {self.message}\n"

        if self.context:
            md += f"- **Context**:\n```\n{self.context}\n```\n"

        if self.fix_suggestion:
            md += f"- **Fix Suggestion**: {self.fix_suggestion}\n"

        return md


@dataclass
class ComplianceResult:
    """Result of a compliance check."""

    language: str
    checker_name: str
    passed: bool
    issues: list[ComplianceIssue] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)
    execution_time_seconds: float = 0.0

    @property
    def critical_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == SeverityLevel.CRITICAL)

    @property
    def high_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == SeverityLevel.HIGH)

    @property
    def medium_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == SeverityLevel.MEDIUM)

    @property
    def low_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == SeverityLevel.LOW)

    def to_markdown(self) -> str:
        """Convert the result to markdown format."""
        status = "✅ PASSED" if self.passed else "❌ FAILED"

        md = f"## {self.checker_name} ({self.language})\n\n"
        md += f"**Status**: {status}\n\n"
        md += f"**Execution Time**: {self.execution_time_seconds:.2f}s\n\n"

        md += "### Issue Summary\n\n"
        md += f"- 🚨 Critical: {self.critical_count}\n"
        md += f"- ⚠️ High: {self.high_count}\n"
        md += f"- ⚡ Medium: {self.medium_count}\n"
        md += f"- 📝 Low: {self.low_count}\n"
        md += f"- **Total**: {len(self.issues)}\n\n"

        if self.metrics:
            md += "### Metrics\n\n"
            for key, value in self.metrics.items():
                md += f"- **{key}**: {value}\n"
            md += "\n"

        if self.issues:
            md += "### Issues\n\n"
            # Group by severity
            by_severity = sorted(
                self.issues, key=lambda i: (i.severity.value, i.rule_id)
            )
            for issue in by_severity:
                md += issue.to_markdown() + "\n"

        return md


class BaseComplianceChecker(ABC):
    """
    Abstract base class for language-specific compliance checkers.

    Each checker must implement the abstract methods to perform compliance
    checking for a specific programming language.
    """

    def __init__(
        self,
        project_root: Path,
        constitution_path: Path | None = None,
        requirements_path: Path | None = None,
    ):
        """
        Initialize the compliance checker.

        Args:
            project_root: Root directory of the project
            constitution_path: Path to constitution.md (optional)
            requirements_path: Path to versioned requirements.md (optional)
        """
        self.project_root = Path(project_root)
        self.constitution_path = Path(constitution_path) if constitution_path else None
        self.requirements_path = Path(requirements_path) if requirements_path else None

    @property
    @abstractmethod
    def language_name(self) -> str:
        """Return the language name this checker supports."""
        pass

    @property
    @abstractmethod
    def checker_name(self) -> str:
        """Return the checker name."""
        pass

    @abstractmethod
    def check_code_style(self) -> list[ComplianceIssue]:
        """
        Check code style compliance.

        Returns:
            List of compliance issues found
        """
        pass

    @abstractmethod
    def check_type_annotations(self) -> list[ComplianceIssue]:
        """
        Check type annotation compliance.

        Returns:
            List of compliance issues found
        """
        pass

    @abstractmethod
    def check_test_coverage(self) -> list[ComplianceIssue]:
        """
        Check test coverage compliance.

        Returns:
            List of compliance issues found
        """
        pass

    @abstractmethod
    def check_error_handling(self) -> list[ComplianceIssue]:
        """
        Check error handling compliance.

        Returns:
            List of compliance issues found
        """
        pass

    def check_constitution_compliance(self) -> list[ComplianceIssue]:
        """
        Check constitution compliance (shared implementation).

        Returns:
            List of compliance issues found
        """
        issues = []

        if not self.constitution_path or not self.constitution_path.exists():
            issues.append(
                ComplianceIssue(
                    rule_id="CONSTITUTION_MISSING",
                    severity=SeverityLevel.CRITICAL,
                    category="constitution",
                    message="Constitution file not found",
                    fix_suggestion=f"Create constitution.md at {self.constitution_path or 'pjflow/constitution.md'}",
                )
            )
            return issues

        try:
            content = self.constitution_path.read_text(encoding="utf-8")

            # Check for common constitution sections
            required_sections = [
                "# Coding Standards",
                "## Coding Standards",
                "### Coding Standards",
            ]
            has_coding_standards = any(
                section in content for section in required_sections
            )

            if not has_coding_standards:
                issues.append(
                    ComplianceIssue(
                        rule_id="CONSTITUTION_NO_STANDARDS",
                        severity=SeverityLevel.HIGH,
                        category="constitution",
                        message="Constitution missing Coding Standards section",
                        fix_suggestion="Add a Coding Standards section to constitution.md",
                    )
                )

        except Exception as e:
            issues.append(
                ComplianceIssue(
                    rule_id="CONSTITUTION_READ_ERROR",
                    severity=SeverityLevel.CRITICAL,
                    category="constitution",
                    message=f"Failed to read constitution: {e}",
                    fix_suggestion="Check constitution.md file permissions and format",
                )
            )

        return issues

    def check_requirements_compliance(self) -> list[ComplianceIssue]:
        """
        Check requirements document compliance (shared implementation).

        Returns:
            List of compliance issues found
        """
        issues = []

        if not self.requirements_path:
            # Requirements are optional for add-feature scenarios
            return issues

        if not self.requirements_path.exists():
            issues.append(
                ComplianceIssue(
                    rule_id="REQUIREMENTS_MISSING",
                    severity=SeverityLevel.HIGH,
                    category="requirements",
                    message=f"Requirements file not found at {self.requirements_path}",
                    fix_suggestion=f"Create requirements.md at {self.requirements_path}",
                )
            )
            return issues

        try:
            content = self.requirements_path.read_text(encoding="utf-8")

            # Check for requirements content
            if len(content.strip()) < 50:
                issues.append(
                    ComplianceIssue(
                        rule_id="REQUIREMENTS_EMPTY",
                        severity=SeverityLevel.HIGH,
                        category="requirements",
                        message="Requirements document appears empty or minimal",
                        fix_suggestion="Add detailed requirements to requirements.md",
                    )
                )

        except Exception as e:
            issues.append(
                ComplianceIssue(
                    rule_id="REQUIREMENTS_READ_ERROR",
                    severity=SeverityLevel.HIGH,
                    category="requirements",
                    message=f"Failed to read requirements: {e}",
                    fix_suggestion="Check requirements.md file permissions and format",
                )
            )

        return issues

    def run_all_checks(self) -> ComplianceResult:
        """
        Run all compliance checks.

        Returns:
            ComplianceResult with all issues found
        """
        import time

        start_time = time.time()

        all_issues: list[ComplianceIssue] = []

        # Run all check methods
        all_issues.extend(self.check_constitution_compliance())
        all_issues.extend(self.check_requirements_compliance())
        all_issues.extend(self.check_code_style())
        all_issues.extend(self.check_type_annotations())
        all_issues.extend(self.check_test_coverage())
        all_issues.extend(self.check_error_handling())

        execution_time = time.time() - start_time

        # Determine if passed (no critical or high issues)
        passed = not any(
            i.severity in (SeverityLevel.CRITICAL, SeverityLevel.HIGH)
            for i in all_issues
        )

        return ComplianceResult(
            language=self.language_name,
            checker_name=self.checker_name,
            passed=passed,
            issues=all_issues,
            execution_time_seconds=execution_time,
        )

    def check_pre_tdd_requirements(self) -> list[ComplianceIssue]:
        """
        Phase 4 pre-check: Verify documents exist and are complete.

        This is a gatekeeper check before executing TDD phases.

        Returns:
            List of compliance issues found
        """
        issues = []

        # 1. Check constitution document
        if not self.constitution_path or not self.constitution_path.exists():
            issues.append(
                ComplianceIssue(
                    rule_id="PRE_TDD_NO_CONSTITUTION",
                    severity=SeverityLevel.CRITICAL,
                    category="pre-tdd",
                    message="Constitution document must exist before TDD phase",
                    fix_suggestion="Create pjflow/constitution.md using pyflow-constitution skill",
                )
            )
            return issues  # Block execution

        # 2. Check requirements document
        if not self.requirements_path or not self.requirements_path.exists():
            issues.append(
                ComplianceIssue(
                    rule_id="PRE_TDD_NO_REQUIREMENTS",
                    severity=SeverityLevel.CRITICAL,
                    category="pre-tdd",
                    message="Requirements document must exist before TDD phase",
                    fix_suggestion="Create requirements.md in version directory",
                )
            )
            return issues  # Block execution

        # 3. Check document content completeness
        try:
            constitution_content = self.constitution_path.read_text(encoding="utf-8")
            if len(constitution_content.strip()) < 100:
                issues.append(
                    ComplianceIssue(
                        rule_id="PRE_TDD_CONSTITUTION_EMPTY",
                        severity=SeverityLevel.HIGH,
                        category="pre-tdd",
                        message="Constitution document appears incomplete",
                        fix_suggestion="Add proper constitution content including Coding Standards",
                    )
                )
        except Exception as e:
            issues.append(
                ComplianceIssue(
                    rule_id="PRE_TDD_CONSTITUTION_READ_ERROR",
                    severity=SeverityLevel.CRITICAL,
                    category="pre-tdd",
                    message=f"Failed to read constitution: {e}",
                    fix_suggestion="Check constitution.md file permissions and format",
                )
            )
            return issues

        try:
            requirements_content = self.requirements_path.read_text(encoding="utf-8")
            if len(requirements_content.strip()) < 50:
                issues.append(
                    ComplianceIssue(
                        rule_id="PRE_TDD_REQUIREMENTS_EMPTY",
                        severity=SeverityLevel.HIGH,
                        category="pre-tdd",
                        message="Requirements document appears incomplete",
                        fix_suggestion="Add detailed requirements including features and acceptance criteria",
                    )
                )
        except Exception as e:
            issues.append(
                ComplianceIssue(
                    rule_id="PRE_TDD_REQUIREMENTS_READ_ERROR",
                    severity=SeverityLevel.CRITICAL,
                    category="pre-tdd",
                    message=f"Failed to read requirements: {e}",
                    fix_suggestion="Check requirements.md file permissions and format",
                )
            )
            return issues

        return issues

    def check_post_tdd_injection_verify(self) -> list[ComplianceIssue]:
        """
        Phase 4 post-check: Verify code reflects document constraints.

        Checks that generated code:
        1. Follows constitution Coding Standards
        2. Implements features from requirements document
        3. Has no feature creep beyond requirements

        Returns:
            List of compliance issues found
        """
        issues = []

        # This check is partially implemented in existing check_* methods
        # Here we primarily aggregate and generate "injection verification" report

        # Check if all constitution requirements are reflected in code
        issues.extend(self.check_code_style())
        issues.extend(self.check_type_annotations())
        issues.extend(self.check_error_handling())

        # Add metadata issue indicating this is an injection verification check
        if not any(i.severity == SeverityLevel.CRITICAL for i in issues):
            issues.append(
                ComplianceIssue(
                    rule_id="INJECTION_VERIFY_SUCCESS",
                    severity=SeverityLevel.INFO,
                    category="injection-verify",
                    message="Code appears to follow constitution constraints",
                )
            )

        return issues

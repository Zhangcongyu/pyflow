"""
Python Compliance Checker

Implements compliance checking for Python projects using ruff, mypy, and pytest.
"""

from __future__ import annotations

import json
import re
import subprocess

from .base_checker import (
    BaseComplianceChecker,
    ComplianceIssue,
    SeverityLevel,
)


class PythonComplianceChecker(BaseComplianceChecker):
    """
    Python-specific compliance checker.

    Uses ruff for linting, mypy for type checking, and pytest for coverage.
    """

    @property
    def language_name(self) -> str:
        return "python"

    @property
    def checker_name(self) -> str:
        return "Python Compliance Checker"

    def check_code_style(self) -> list[ComplianceIssue]:
        """Check code style using ruff."""
        issues = []

        try:
            # Run ruff check
            result = subprocess.run(
                ["ruff", "check", ".", "--output-format=json"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
            )

            if result.stdout:
                try:
                    ruff_output = json.loads(result.stdout)
                    for item in ruff_output:
                        severity = self._map_ruff_severity(item.get("level", "Error"))

                        issues.append(
                            ComplianceIssue(
                                rule_id=item["code"],
                                severity=severity,
                                category="code_style",
                                message=item["message"],
                                file_path=item.get("filename"),
                                line_number=item.get("location", {}).get("row"),
                                column_number=item.get("location", {}).get("column"),
                                fix_suggestion="Run `ruff check --fix .` to auto-fix",
                            )
                        )
                except json.JSONDecodeError:
                    pass

        except FileNotFoundError:
            issues.append(
                ComplianceIssue(
                    rule_id="RUFF_NOT_INSTALLED",
                    severity=SeverityLevel.HIGH,
                    category="code_style",
                    message="ruff is not installed",
                    fix_suggestion="Install ruff: `uv add --dev ruff`",
                )
            )
        except Exception as e:
            issues.append(
                ComplianceIssue(
                    rule_id="RUFF_CHECK_ERROR",
                    severity=SeverityLevel.MEDIUM,
                    category="code_style",
                    message=f"Failed to run ruff: {e}",
                )
            )

        return issues

    def check_type_annotations(self) -> list[ComplianceIssue]:
        """Check type annotations using mypy."""
        issues = []

        try:
            # Run mypy
            result = subprocess.run(
                [
                    "mypy",
                    "src/",
                    "--no-error-summary",
                    "--show-error-codes",
                ],
                cwd=self.project_root,
                capture_output=True,
                text=True,
            )

            if result.stdout:
                for line in result.stdout.splitlines():
                    if line.strip() and not line.startswith("Success:"):
                        issue = self._parse_mypy_line(line)
                        if issue:
                            issues.append(issue)

        except FileNotFoundError:
            issues.append(
                ComplianceIssue(
                    rule_id="MYPY_NOT_INSTALLED",
                    severity=SeverityLevel.HIGH,
                    category="type_annotations",
                    message="mypy is not installed",
                    fix_suggestion="Install mypy: `uv add --dev mypy`",
                )
            )
        except Exception as e:
            issues.append(
                ComplianceIssue(
                    rule_id="MYPY_CHECK_ERROR",
                    severity=SeverityLevel.MEDIUM,
                    category="type_annotations",
                    message=f"Failed to run mypy: {e}",
                )
            )

        # Additional checks for missing type annotations
        issues.extend(self._check_missing_type_hints())

        return issues

    def check_test_coverage(self) -> list[ComplianceIssue]:
        """Check test coverage using pytest."""
        issues = []

        try:
            # Run pytest with coverage
            subprocess.run(
                [
                    "pytest",
                    "--cov=src",
                    "--cov-report=json",
                    "--cov-report=term-missing",
                ],
                cwd=self.project_root,
                capture_output=True,
                text=True,
            )

            # Read coverage report
            coverage_file = self.project_root / "coverage.json"
            if coverage_file.exists():
                try:
                    with open(coverage_file) as f:
                        coverage_data = json.load(f)

                    total_coverage = coverage_data.get("totals", {}).get(
                        "percent_covered", 0
                    )

                    if total_coverage < 80:
                        issues.append(
                            ComplianceIssue(
                                rule_id="COVERAGE_LOW",
                                severity=SeverityLevel.HIGH
                                if total_coverage < 60
                                else SeverityLevel.MEDIUM,
                                category="test_coverage",
                                message=f"Test coverage is {total_coverage:.1f}%, below 80% threshold",
                                fix_suggestion="Add more tests to improve coverage",
                            )
                        )

                    # Check individual files
                    for filename, file_data in coverage_data.get("files", {}).items():
                        file_coverage = file_data.get("summary", {}).get(
                            "percent_covered", 100
                        )
                        if file_coverage < 80:
                            issues.append(
                                ComplianceIssue(
                                    rule_id="FILE_COVERAGE_LOW",
                                    severity=SeverityLevel.MEDIUM,
                                    category="test_coverage",
                                    message=f"File {filename} has {file_coverage:.1f}% coverage",
                                    file_path=filename,
                                    fix_suggestion="Add tests for this file",
                                )
                            )

                except (OSError, json.JSONDecodeError):
                    pass

        except FileNotFoundError:
            issues.append(
                ComplianceIssue(
                    rule_id="PYTEST_NOT_INSTALLED",
                    severity=SeverityLevel.HIGH,
                    category="test_coverage",
                    message="pytest is not installed",
                    fix_suggestion="Install pytest: `uv add --dev pytest pytest-cov`",
                )
            )
        except Exception as e:
            issues.append(
                ComplianceIssue(
                    rule_id="COVERAGE_CHECK_ERROR",
                    severity=SeverityLevel.MEDIUM,
                    category="test_coverage",
                    message=f"Failed to check coverage: {e}",
                )
            )

        return issues

    def check_error_handling(self) -> list[ComplianceIssue]:
        """Check error handling compliance."""
        issues = []

        # Check for bare except clauses
        try:
            for py_file in self.project_root.rglob("*.py"):
                if "venv" in str(py_file) or ".venv" in str(py_file):
                    continue

                try:
                    content = py_file.read_text(encoding="utf-8")
                    lines = content.splitlines()

                    for i, line in enumerate(lines, 1):
                        # Check for bare except
                        if re.search(r"except\s*:", line):
                            issues.append(
                                ComplianceIssue(
                                    rule_id="BARE_EXCEPT",
                                    severity=SeverityLevel.HIGH,
                                    category="error_handling",
                                    message="Bare except clause detected",
                                    file_path=str(
                                        py_file.relative_to(self.project_root)
                                    ),
                                    line_number=i,
                                    context=line.strip(),
                                    fix_suggestion="Specify exception type, e.g., `except Exception as e:`",
                                )
                            )

                        # Check for pass in except
                        if re.search(r"except.*:\s*pass", line):
                            issues.append(
                                ComplianceIssue(
                                    rule_id="EMPTY_EXCEPT",
                                    severity=SeverityLevel.MEDIUM,
                                    category="error_handling",
                                    message="Empty except block with pass",
                                    file_path=str(
                                        py_file.relative_to(self.project_root)
                                    ),
                                    line_number=i,
                                    context=line.strip(),
                                    fix_suggestion="Add proper error handling or logging",
                                )
                            )

                except (OSError, UnicodeDecodeError):
                    continue

        except Exception:
            pass

        return issues

    def _map_ruff_severity(self, level: str) -> SeverityLevel:
        """Map ruff severity level to our SeverityLevel."""
        mapping = {
            "Error": SeverityLevel.HIGH,
            "Warning": SeverityLevel.MEDIUM,
            "Info": SeverityLevel.LOW,
        }
        return mapping.get(level, SeverityLevel.MEDIUM)

    def _parse_mypy_line(self, line: str) -> ComplianceIssue | None:
        """Parse a mypy error line into a ComplianceIssue."""
        # Format: filename:line: severity: message
        match = re.match(r"([^:]+):(\d+): (\w+): (.+)", line)
        if match:
            filename, line_no, severity, message = match.groups()
            return ComplianceIssue(
                rule_id="MYPY_ERROR",
                severity=SeverityLevel.HIGH
                if severity == "error"
                else SeverityLevel.MEDIUM,
                category="type_annotations",
                message=message,
                file_path=filename,
                line_number=int(line_no),
                fix_suggestion="Add type annotations to fix this issue",
            )
        return None

    def _check_missing_type_hints(self) -> list[ComplianceIssue]:
        """Check for missing type hints in function definitions."""
        issues = []

        try:
            for py_file in self.project_root.rglob("*.py"):
                if any(
                    skip in str(py_file)
                    for skip in ["venv", ".venv", "tests", "__pycache__"]
                ):
                    continue

                try:
                    content = py_file.read_text(encoding="utf-8")
                    lines = content.splitlines()

                    for i, line in enumerate(lines, 1):
                        # Check for function definitions without return type annotation
                        if (
                            re.search(r"def\s+\w+\s*\([^)]*\)\s*:", line)
                            and "->" not in line
                        ):
                            # Skip if it's a dunder method
                            if not re.search(r"def\s+__\w+__", line):
                                issues.append(
                                    ComplianceIssue(
                                        rule_id="MISSING_RETURN_TYPE",
                                        severity=SeverityLevel.MEDIUM,
                                        category="type_annotations",
                                        message="Function missing return type annotation",
                                        file_path=str(
                                            py_file.relative_to(self.project_root)
                                        ),
                                        line_number=i,
                                        context=line.strip(),
                                        fix_suggestion="Add return type annotation, e.g., `-> None:`",
                                    )
                                )

                except (OSError, UnicodeDecodeError):
                    continue

        except Exception:
            pass

        return issues

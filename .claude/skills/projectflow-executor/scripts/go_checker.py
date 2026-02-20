"""
Go Compliance Checker

Implements compliance checking for Go projects using gofmt, go vet, and go test.
"""

from __future__ import annotations

import re
import subprocess

from .base_checker import (
    BaseComplianceChecker,
    ComplianceIssue,
    SeverityLevel,
)


class GoComplianceChecker(BaseComplianceChecker):
    """
    Go-specific compliance checker.

    Uses gofmt and go vet for code quality, and go test for coverage.
    """

    @property
    def language_name(self) -> str:
        return "go"

    @property
    def checker_name(self) -> str:
        return "Go Compliance Checker"

    def check_code_style(self) -> list[ComplianceIssue]:
        """Check code style using gofmt and go vet."""
        issues = []

        # Check gofmt
        try:
            result = subprocess.run(
                ["gofmt", "-l", "."],
                cwd=self.project_root,
                capture_output=True,
                text=True,
            )

            if result.stdout:
                for line in result.stdout.splitlines():
                    if line.strip():
                        issues.append(
                            ComplianceIssue(
                                rule_id="GOFMT_MISMATCH",
                                severity=SeverityLevel.MEDIUM,
                                category="code_style",
                                message="File not properly formatted",
                                file_path=line.strip(),
                                fix_suggestion="Run `gofmt -w .` to fix formatting",
                            )
                        )

        except FileNotFoundError:
            issues.append(
                ComplianceIssue(
                    rule_id="GO_NOT_INSTALLED",
                    severity=SeverityLevel.CRITICAL,
                    category="code_style",
                    message="Go toolchain is not installed",
                    fix_suggestion="Install Go from https://go.dev/dl/",
                )
            )
        except Exception as e:
            issues.append(
                ComplianceIssue(
                    rule_id="GOFMT_CHECK_ERROR",
                    severity=SeverityLevel.MEDIUM,
                    category="code_style",
                    message=f"Failed to run gofmt: {e}",
                )
            )

        # Check go vet
        try:
            result = subprocess.run(
                ["go", "vet", "./..."],
                cwd=self.project_root,
                capture_output=True,
                text=True,
            )

            if result.stderr or result.stdout:
                output = result.stderr + result.stdout
                for line in output.splitlines():
                    if line.strip() and not line.startswith("#"):
                        issue = self._parse_go_vet_line(line)
                        if issue:
                            issues.append(issue)

        except Exception as e:
            issues.append(
                ComplianceIssue(
                    rule_id="GO_VET_ERROR",
                    severity=SeverityLevel.MEDIUM,
                    category="code_style",
                    message=f"Failed to run go vet: {e}",
                )
            )

        return issues

    def check_type_annotations(self) -> list[ComplianceIssue]:
        """Check type annotations - Go has implicit types, check for interface{} overuse."""
        issues = []

        # Check for interface{} overuse
        try:
            for go_file in self.project_root.rglob("*.go"):
                if "vendor" in str(go_file):
                    continue

                try:
                    content = go_file.read_text(encoding="utf-8")
                    lines = content.splitlines()

                    for i, line in enumerate(lines, 1):
                        # Check for interface{} usage
                        if re.search(r"interface\{\}", line):
                            # Skip if it's in a comment
                            stripped = line.strip()
                            if not stripped.startswith("//"):
                                issues.append(
                                    ComplianceIssue(
                                        rule_id="INTERFACE_EMPTY",
                                        severity=SeverityLevel.MEDIUM,
                                        category="type_annotations",
                                        message="Use of empty interface{} detected",
                                        file_path=str(
                                            go_file.relative_to(self.project_root)
                                        ),
                                        line_number=i,
                                        context=line.strip(),
                                        fix_suggestion="Use specific type or 'any' (Go 1.18+)",
                                    )
                                )

                except (UnicodeDecodeError, IOError):
                    continue

        except Exception:
            pass

        return issues

    def check_test_coverage(self) -> list[ComplianceIssue]:
        """Check test coverage using go test."""
        issues = []

        try:
            # Run go test with coverage
            result = subprocess.run(
                ["go", "test", "-cover", "./..."],
                cwd=self.project_root,
                capture_output=True,
                text=True,
            )

            if result.stdout or result.stderr:
                output = result.stdout + result.stderr

                # Parse coverage percentage
                coverage_match = re.search(
                    r"coverage:\s*([\d.]+)%", output, re.IGNORECASE
                )
                if coverage_match:
                    coverage = float(coverage_match.group(1))
                    if coverage < 80:
                        issues.append(
                            ComplianceIssue(
                                rule_id="COVERAGE_LOW",
                                severity=SeverityLevel.HIGH
                                if coverage < 60
                                else SeverityLevel.MEDIUM,
                                category="test_coverage",
                                message=f"Test coverage is {coverage:.1f}%, below 80% threshold",
                                fix_suggestion="Add more tests to improve coverage",
                            )
                        )

                # Check for no test files
                if "no test files" in output.lower():
                    issues.append(
                        ComplianceIssue(
                            rule_id="NO_TEST_FILES",
                            severity=SeverityLevel.HIGH,
                            category="test_coverage",
                            message="No test files found",
                            fix_suggestion="Create test files with _test.go suffix",
                        )
                    )

        except FileNotFoundError:
            issues.append(
                ComplianceIssue(
                    rule_id="GO_NOT_INSTALLED",
                    severity=SeverityLevel.CRITICAL,
                    category="test_coverage",
                    message="Go toolchain is not installed",
                    fix_suggestion="Install Go from https://go.dev/dl/",
                )
            )
        except Exception as e:
            issues.append(
                ComplianceIssue(
                    rule_id="GO_TEST_ERROR",
                    severity=SeverityLevel.MEDIUM,
                    category="test_coverage",
                    message=f"Failed to run go test: {e}",
                )
            )

        return issues

    def check_error_handling(self) -> list[ComplianceIssue]:
        """Check error handling compliance."""
        issues = []

        # Check for ignored error returns
        try:
            for go_file in self.project_root.rglob("*.go"):
                if "vendor" in str(go_file):
                    continue

                try:
                    content = go_file.read_text(encoding="utf-8")
                    lines = content.splitlines()

                    for i, line in enumerate(lines, 1):
                        # Check for _ to ignore error
                        if re.search(r",\s*_\s*:=.*\(\)", line):
                            issues.append(
                                ComplianceIssue(
                                    rule_id="IGNORED_ERROR",
                                    severity=SeverityLevel.HIGH,
                                    category="error_handling",
                                    message="Error return value is ignored",
                                    file_path=str(
                                        go_file.relative_to(self.project_root)
                                    ),
                                    line_number=i,
                                    context=line.strip(),
                                    fix_suggestion="Handle the error explicitly or use errcheck",
                                )
                            )

                        # Check for blank identifier in function call
                        if (
                            re.search(r"\w+\s*:=.*\(\s*\.\.\.\s*\)", line)
                            and "_" in line
                        ):
                            issues.append(
                                ComplianceIssue(
                                    rule_id="POTENTIAL_IGNORED_ERROR",
                                    severity=SeverityLevel.MEDIUM,
                                    category="error_handling",
                                    message="Potential ignored error return value",
                                    file_path=str(
                                        go_file.relative_to(self.project_root)
                                    ),
                                    line_number=i,
                                    context=line.strip(),
                                    fix_suggestion="Verify error handling",
                                )
                            )

                except (UnicodeDecodeError, IOError):
                    continue

        except Exception:
            pass

        return issues

    def _parse_go_vet_line(self, line: str) -> ComplianceIssue | None:
        """Parse a go vet error line into a ComplianceIssue."""
        # Format: filename:line:column: message
        match = re.match(r"([^:]+):(\d+):(\d+)?:?\s*(.+)", line)
        if match:
            filename, line_no, message = match.group(1), match.group(2), match.group(4)
            return ComplianceIssue(
                rule_id="GO_VET",
                severity=SeverityLevel.HIGH,
                category="code_style",
                message=message,
                file_path=filename,
                line_number=int(line_no) if line_no else None,
                fix_suggestion="Fix the reported issue",
            )
        return None

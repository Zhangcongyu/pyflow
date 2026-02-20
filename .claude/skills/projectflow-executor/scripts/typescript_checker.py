"""
TypeScript Compliance Checker

Implements compliance checking for TypeScript/JavaScript projects using
eslint, tsc, and vitest.
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


class TypeScriptComplianceChecker(BaseComplianceChecker):
    """
    TypeScript-specific compliance checker.

    Uses eslint for linting, tsc for type checking, and vitest for coverage.
    """

    @property
    def language_name(self) -> str:
        return "typescript"

    @property
    def checker_name(self) -> str:
        return "TypeScript Compliance Checker"

    def check_code_style(self) -> list[ComplianceIssue]:
        """Check code style using eslint."""
        issues = []

        try:
            # Run eslint
            result = subprocess.run(
                ["eslint", ".", "--format=json"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
            )

            if result.stdout:
                try:
                    eslint_output = json.loads(result.stdout)
                    for file_result in eslint_output:
                        filename = file_result.get("filePath", "")
                        for message in file_result.get("messages", []):
                            severity = (
                                SeverityLevel.HIGH
                                if message.get("severity") == 2
                                else SeverityLevel.MEDIUM
                            )

                            issues.append(
                                ComplianceIssue(
                                    rule_id=message.get("ruleId", "UNKNOWN"),
                                    severity=severity,
                                    category="code_style",
                                    message=message.get("message", ""),
                                    file_path=filename,
                                    line_number=message.get("line"),
                                    column_number=message.get("column"),
                                    fix_suggestion="Run `eslint --fix .` to auto-fix",
                                )
                            )
                except json.JSONDecodeError:
                    pass

        except FileNotFoundError:
            issues.append(
                ComplianceIssue(
                    rule_id="ESLINT_NOT_INSTALLED",
                    severity=SeverityLevel.HIGH,
                    category="code_style",
                    message="eslint is not installed",
                    fix_suggestion="Install eslint: `pnpm add -D eslint`",
                )
            )
        except Exception as e:
            issues.append(
                ComplianceIssue(
                    rule_id="ESLINT_CHECK_ERROR",
                    severity=SeverityLevel.MEDIUM,
                    category="code_style",
                    message=f"Failed to run eslint: {e}",
                )
            )

        return issues

    def check_type_annotations(self) -> list[ComplianceIssue]:
        """Check type annotations using tsc."""
        issues = []

        try:
            # Run tsc
            result = subprocess.run(
                ["npx", "tsc", "--noEmit"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
            )

            if result.stderr:
                for line in result.stderr.splitlines():
                    issue = self._parse_tsc_line(line)
                    if issue:
                        issues.append(issue)

        except FileNotFoundError:
            issues.append(
                ComplianceIssue(
                    rule_id="TSC_NOT_INSTALLED",
                    severity=SeverityLevel.HIGH,
                    category="type_annotations",
                    message="TypeScript compiler is not installed",
                    fix_suggestion="Install typescript: `pnpm add -D typescript`",
                )
            )
        except Exception as e:
            issues.append(
                ComplianceIssue(
                    rule_id="TSC_CHECK_ERROR",
                    severity=SeverityLevel.MEDIUM,
                    category="type_annotations",
                    message=f"Failed to run tsc: {e}",
                )
            )

        # Additional checks for any types
        issues.extend(self._check_any_types())

        return issues

    def check_test_coverage(self) -> list[ComplianceIssue]:
        """Check test coverage using vitest."""
        issues = []

        try:
            # Run vitest with coverage
            result = subprocess.run(
                ["npx", "vitest", "run", "--coverage"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
            )

            # Parse coverage from output
            if result.stdout or result.stderr:
                output = result.stdout + result.stderr
                coverage_match = re.search(r"Coverage\s+([\d.]+)%", output)
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

        except FileNotFoundError:
            issues.append(
                ComplianceIssue(
                    rule_id="VITEST_NOT_INSTALLED",
                    severity=SeverityLevel.HIGH,
                    category="test_coverage",
                    message="vitest is not installed",
                    fix_suggestion="Install vitest: `pnpm add -D vitest @vitest/coverage-v8`",
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

        # Check for empty catch blocks
        try:
            for ts_file in self.project_root.rglob("*.ts"):
                if any(
                    skip in str(ts_file) for skip in ["node_modules", ".next", "dist"]
                ):
                    continue

                try:
                    content = ts_file.read_text(encoding="utf-8")
                    lines = content.splitlines()

                    for i, line in enumerate(lines, 1):
                        # Check for empty catch blocks
                        if re.search(r"catch\s*\([^)]*\)\s*\{\s*\}", line):
                            issues.append(
                                ComplianceIssue(
                                    rule_id="EMPTY_CATCH",
                                    severity=SeverityLevel.HIGH,
                                    category="error_handling",
                                    message="Empty catch block detected",
                                    file_path=str(
                                        ts_file.relative_to(self.project_root)
                                    ),
                                    line_number=i,
                                    context=line.strip(),
                                    fix_suggestion="Add proper error handling or logging",
                                )
                            )

                        # Check for catch with just console.error
                        if re.search(r"catch.*\{\s*console\.error", line):
                            issues.append(
                                ComplianceIssue(
                                    rule_id="WEAK_CATCH",
                                    severity=SeverityLevel.MEDIUM,
                                    category="error_handling",
                                    message="Catch block only logs to console",
                                    file_path=str(
                                        ts_file.relative_to(self.project_root)
                                    ),
                                    line_number=i,
                                    context=line.strip(),
                                    fix_suggestion="Add proper error handling or recovery",
                                )
                            )

                except (OSError, UnicodeDecodeError):
                    continue

        except Exception:
            pass

        return issues

    def _parse_tsc_line(self, line: str) -> ComplianceIssue | None:
        """Parse a tsc error line into a ComplianceIssue."""
        # Format: filename(line,col): error TSXXXX: message
        match = re.match(r"([^(]+)\((\d+),(\d+)\): error (TS\d+): (.+)", line)
        if match:
            filename, line_no, col_no, error_code, message = match.groups()
            return ComplianceIssue(
                rule_id=error_code,
                severity=SeverityLevel.HIGH,
                category="type_annotations",
                message=message,
                file_path=filename,
                line_number=int(line_no),
                column_number=int(col_no),
                fix_suggestion="Add or fix type annotations",
            )
        return None

    def _check_any_types(self) -> list[ComplianceIssue]:
        """Check for usage of any types."""
        issues = []

        try:
            for ts_file in self.project_root.rglob("*.ts"):
                if any(
                    skip in str(ts_file)
                    for skip in ["node_modules", ".next", "dist", "tests"]
                ):
                    continue

                try:
                    content = ts_file.read_text(encoding="utf-8")
                    lines = content.splitlines()

                    for i, line in enumerate(lines, 1):
                        # Check for any type usage (excluding comments)
                        stripped = line.strip()
                        if not stripped.startswith("//") and ": any" in line:
                            issues.append(
                                ComplianceIssue(
                                    rule_id="ANY_TYPE_USED",
                                    severity=SeverityLevel.MEDIUM,
                                    category="type_annotations",
                                    message="Type 'any' detected",
                                    file_path=str(
                                        ts_file.relative_to(self.project_root)
                                    ),
                                    line_number=i,
                                    context=line.strip(),
                                    fix_suggestion="Replace 'any' with specific type or 'unknown'",
                                )
                            )

                except (OSError, UnicodeDecodeError):
                    continue

        except Exception:
            pass

        return issues

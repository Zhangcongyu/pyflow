"""
Compliance Reporter

Generates compliance reports in markdown format.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from .base_checker import ComplianceResult


class ComplianceReporter:
    """
    Generates compliance reports from check results.
    """

    def __init__(self, output_dir: Path):
        """
        Initialize the reporter.

        Args:
            output_dir: Directory to write reports to
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_report(
        self,
        result: ComplianceResult,
        phase: str = "final",
        version_dir: str = "unknown",
    ) -> Path:
        """
        Generate a compliance report from the result.

        Args:
            result: Compliance check result
            phase: Phase name (e.g., "red", "green", "refactor", "final")
            version_dir: Version directory name (e.g., "v0_initial")

        Returns:
            Path to the generated report file
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        report_content = self._format_report(result, phase, timestamp)

        # Write report
        report_path = self.output_dir / "compliance_report.md"
        report_path.write_text(report_content, encoding="utf-8")

        return report_path

    def _format_report(
        self,
        result: ComplianceResult,
        phase: str,
        timestamp: str,
    ) -> str:
        """Format the compliance report as markdown."""
        status_emoji = "✅ PASSED" if result.passed else "❌ FAILED"
        status_color = "green" if result.passed else "red"

        md = "# Compliance Report\n\n"
        md += f"**Generated**: {timestamp}\n\n"
        md += f"**Language**: {result.language}\n\n"
        md += f"**Checker**: {result.checker_name}\n\n"
        md += f"**Phase**: {phase}\n\n"
        md += (
            f"**Status**: <span style='color:{status_color}'>{status_emoji}</span>\n\n"
        )
        md += "---\n\n"

        # Executive Summary
        md += "## Executive Summary\n\n"
        md += f"- **Overall Status**: {status_emoji}\n"
        md += f"- **Execution Time**: {result.execution_time_seconds:.2f}s\n"
        md += f"- **Total Issues**: {len(result.issues)}\n\n"

        md += "### Issue Breakdown\n\n"
        md += "| Severity | Count |\n"
        md += "|----------|-------|\n"
        md += f"| 🚨 Critical | {result.critical_count} |\n"
        md += f"| ⚠️ High | {result.high_count} |\n"
        md += f"| ⚡ Medium | {result.medium_count} |\n"
        md += f"| 📝 Low | {result.low_count} |\n"
        md += "\n"

        # Metrics
        if result.metrics:
            md += "## Metrics\n\n"
            for key, value in result.metrics.items():
                md += f"- **{key}**: {value}\n"
            md += "\n"

        # Issues
        if result.issues:
            md += "## Issues Found\n\n"

            # Group by category
            by_category: dict[str, list] = {}
            for issue in result.issues:
                if issue.category not in by_category:
                    by_category[issue.category] = []
                by_category[issue.category].append(issue)

            for category, issues in sorted(by_category.items()):
                md += f"### {category.title()}\n\n"
                for issue in sorted(
                    issues, key=lambda i: (i.severity.value, i.rule_id)
                ):
                    md += issue.to_markdown() + "\n"
        else:
            md += "## Issues Found\n\n"
            md += "✅ No issues found! All compliance checks passed.\n\n"

        # Recommendations
        md += "---\n\n"
        md += "## Recommendations\n\n"

        if result.critical_count > 0:
            md += "### 🚨 Critical Issues (Must Fix)\n\n"
            md += "Critical issues must be fixed before continuing. Address the following:\n\n"
            for issue in result.issues:
                if issue.severity.value == "critical":
                    md += f"- [{issue.rule_id}] {issue.message}\n"
                    if issue.fix_suggestion:
                        md += f"  - Fix: {issue.fix_suggestion}\n"
            md += "\n"

        if result.high_count > 0:
            md += "### ⚠️ High Priority Issues\n\n"
            md += "High priority issues should be fixed soon:\n\n"
            for issue in result.issues:
                if issue.severity.value == "high":
                    md += f"- [{issue.rule_id}] {issue.message}\n"
            md += "\n"

        if result.medium_count > 0 or result.low_count > 0:
            md += "### ⚡ Medium/Low Priority Issues\n\n"
            md += "Consider fixing these issues to improve code quality:\n\n"
            for issue in result.issues:
                if issue.severity.value in ("medium", "low"):
                    md += f"- [{issue.rule_id}] {issue.message}\n"
            md += "\n"

        if result.passed:
            md += "### ✅ All Checks Passed\n\n"
            md += "Great job! Your code complies with all required standards.\n\n"

        md += "---\n\n"
        md += f"*Generated by {result.checker_name}*\n"

        return md


def generate_summary_report(
    results: list[ComplianceResult],
    output_path: Path,
) -> None:
    """
    Generate a summary report from multiple check results.

    Args:
        results: List of compliance check results
        output_path: Path to write the summary report
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    md = "# Compliance Summary Report\n\n"
    md += f"**Generated**: {timestamp}\n\n"
    md += "---\n\n"

    total_issues = sum(len(r.issues) for r in results)
    total_critical = sum(r.critical_count for r in results)
    total_high = sum(r.high_count for r in results)
    passed_count = sum(1 for r in results if r.passed)

    md += "## Overall Summary\n\n"
    md += f"- **Total Checks**: {len(results)}\n"
    md += f"- **Passed**: {passed_count}\n"
    md += f"- **Failed**: {len(results) - passed_count}\n"
    md += f"- **Total Issues**: {total_issues}\n"
    md += f"- 🚨 Critical: {total_critical}\n"
    md += f"- ⚠️ High: {total_high}\n\n"

    md += "## Individual Results\n\n"
    for i, result in enumerate(results, 1):
        md += f"### {i}. {result.checker_name}\n\n"
        md += f"- **Status**: {'✅ PASSED' if result.passed else '❌ FAILED'}\n"
        md += f"- **Issues**: {len(result.issues)}\n"
        md += f"- **Execution Time**: {result.execution_time_seconds:.2f}s\n\n"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(md, encoding="utf-8")

#!/usr/bin/env python3
"""
Compliance Check CLI

Command-line interface for running compliance checks.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.checker_factory import CheckerFactory
from scripts.compliance_reporter import ComplianceReporter


def main() -> int:
    """Run compliance checks and generate report."""
    parser = argparse.ArgumentParser(description="Run ProjectFlow compliance checks")
    parser.add_argument(
        "--language",
        "-l",
        choices=["python", "typescript", "go", "auto"],
        default="auto",
        help="Programming language (default: auto-detect)",
    )
    parser.add_argument(
        "--project-root",
        "-p",
        type=Path,
        default=Path.cwd(),
        help="Project root directory (default: current directory)",
    )
    parser.add_argument(
        "--constitution",
        "-c",
        type=Path,
        default=None,
        help="Path to constitution.md (default: pjflow/constitution.md)",
    )
    parser.add_argument(
        "--requirements",
        "-r",
        type=Path,
        default=None,
        help="Path to versioned requirements.md (default: pjflow/{VERSION}/requirements.md)",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        type=Path,
        default=None,
        help="Output directory for report (default: pjflow/{VERSION}/)",
    )
    parser.add_argument(
        "--phase",
        default="final",
        help="Phase name for the report (default: final)",
    )
    parser.add_argument(
        "--version-dir",
        "-v",
        default=None,
        help="Version directory name (e.g., v0_initial)",
    )

    args = parser.parse_args()

    # Auto-detect language if needed
    if args.language == "auto":
        language = CheckerFactory.detect_language(args.project_root)
        print(f"Auto-detected language: {language}")
    else:
        language = args.language

    # Determine constitution path
    if args.constitution is None:
        constitution_path = args.project_root / "pjflow" / "constitution.md"
    else:
        constitution_path = args.constitution

    # Determine requirements path
    if args.requirements is None and args.version_dir:
        requirements_path = (
            args.project_root / "pjflow" / args.version_dir / "requirements.md"
        )
    else:
        requirements_path = args.requirements

    # Determine output directory
    if args.output_dir is None and args.version_dir:
        output_dir = args.project_root / "pjflow" / args.version_dir
    elif args.output_dir is None:
        output_dir = args.project_root / "pjflow"
    else:
        output_dir = args.output_dir

    # Create checker
    print(f"Creating {language} compliance checker...")
    checker = CheckerFactory.create(
        language=language,
        project_root=args.project_root,
        constitution_path=constitution_path,
        requirements_path=requirements_path,
    )

    # Run checks
    print("Running compliance checks...")
    result = checker.run_all_checks()

    # Print summary
    print("\n" + "=" * 60)
    print("COMPLIANCE CHECK SUMMARY")
    print("=" * 60)
    print(f"Status: {'✅ PASSED' if result.passed else '❌ FAILED'}")
    print(f"Execution Time: {result.execution_time_seconds:.2f}s")
    print(f"Total Issues: {len(result.issues)}")
    print(f"  🚨 Critical: {result.critical_count}")
    print(f"  ⚠️ High: {result.high_count}")
    print(f"  ⚡ Medium: {result.medium_count}")
    print(f"  📝 Low: {result.low_count}")

    # Generate report
    reporter = ComplianceReporter(output_dir)
    version_dir = args.version_dir or "latest"
    report_path = reporter.generate_report(
        result, phase=args.phase, version_dir=version_dir
    )

    print(f"\nReport generated: {report_path}")

    # Return exit code
    return 0 if result.passed else 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Create Simple Requirements Document

Generates a requirements document template for simple projects.
For medium/complex projects, use pyflow-brainstorming skill instead.
"""

from __future__ import annotations

import argparse
from pathlib import Path


def create_requirements_template(
    goal: str,
    project_type: str,
    complexity: str,
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
        md += f"{goal}\n\n"

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
        md += f"{goal}\n\n"

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


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Create a requirements document for simple projects"
    )
    parser.add_argument(
        "--goal",
        required=True,
        help="User's goal for this version",
    )
    parser.add_argument(
        "--project-type",
        required=True,
        choices=["new", "add-feature"],
        help="Whether this is a new project or adding features",
    )
    parser.add_argument(
        "--version-dir",
        required=True,
        help="Version directory name (e.g., v0_initial, v1_add_feature)",
    )
    parser.add_argument(
        "--complexity",
        default="simple",
        choices=["simple", "medium", "complex"],
        help="Project complexity level (default: simple)",
    )
    parser.add_argument(
        "--project-root",
        default=".",
        help="Path to project root (default: current directory)",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing requirements file",
    )

    args = parser.parse_args()

    # Import document manager
    project_root = Path(args.project_root)
    scripts_dir = (
        project_root / ".claude" / "skills" / "projectflow-executor" / "scripts"
    )

    import sys

    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))

    from document_manager import DocumentManager

    # Create document manager
    pjflow_root = project_root / "pjflow"
    doc_manager = DocumentManager(pjflow_root)

    # Generate requirements content
    requirements_content = create_requirements_template(
        goal=args.goal,
        project_type=args.project_type,
        complexity=args.complexity,
    )

    # Create versioned requirements document
    try:
        requirements_path = doc_manager.create_versioned_requirements(
            args.version_dir,
            requirements_content,
            overwrite=args.overwrite,
        )
        print(f"✅ Requirements document created: {requirements_path}")
    except FileExistsError as e:
        print(f"❌ Error: {e}")
        print("Use --overwrite to overwrite existing file")
        sys.exit(1)


if __name__ == "__main__":
    main()

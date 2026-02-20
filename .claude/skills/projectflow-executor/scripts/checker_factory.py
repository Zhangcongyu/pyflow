"""
Checker Factory

Factory for creating language-specific compliance checkers.
"""

from __future__ import annotations

from pathlib import Path

from .base_checker import BaseComplianceChecker
from .go_checker import GoComplianceChecker
from .python_checker import PythonComplianceChecker
from .typescript_checker import TypeScriptComplianceChecker


class CheckerFactory:
    """
    Factory for creating compliance checkers based on language type.

    Supported languages:
    - python
    - typescript
    - go
    """

    _checkers = {
        "python": PythonComplianceChecker,
        "typescript": TypeScriptComplianceChecker,
        "ts": TypeScriptComplianceChecker,  # Alias
        "go": GoComplianceChecker,
        "golang": GoComplianceChecker,  # Alias
    }

    @classmethod
    def create(
        cls,
        language: str,
        project_root: Path,
        constitution_path: Path | None = None,
        requirements_path: Path | None = None,
    ) -> BaseComplianceChecker:
        """
        Create a compliance checker for the specified language.

        Args:
            language: Programming language (python, typescript, go)
            project_root: Root directory of the project
            constitution_path: Path to constitution.md (optional)
            requirements_path: Path to versioned requirements.md (optional)

        Returns:
            A compliance checker instance

        Raises:
            ValueError: If language is not supported
        """
        language_key = language.lower()

        if language_key not in cls._checkers:
            supported = ", ".join(cls._checkers.keys())
            raise ValueError(
                f"Unsupported language: {language}. Supported languages: {supported}"
            )

        checker_class = cls._checkers[language_key]
        return checker_class(
            project_root=project_root,
            constitution_path=constitution_path,
            requirements_path=requirements_path,
        )

    @classmethod
    def detect_language(cls, project_root: Path) -> str:
        """
        Auto-detect the project language based on file presence.

        Args:
            project_root: Root directory of the project

        Returns:
            Detected language name
        """
        project_root = Path(project_root)

        # Check for Python
        python_indicators = [
            "pyproject.toml",
            "setup.py",
            "requirements.txt",
            "Pipfile",
        ]
        if any((project_root / f).exists() for f in python_indicators):
            return "python"

        # Check for TypeScript/JavaScript
        ts_indicators = [
            "package.json",
            "tsconfig.json",
        ]
        if any((project_root / f).exists() for f in ts_indicators):
            # Check if it's TypeScript
            if (project_root / "tsconfig.json").exists():
                return "typescript"
            # Check for .ts files
            if list(project_root.rglob("*.ts")):
                return "typescript"
            return "typescript"  # Default to TS for JS projects

        # Check for Go
        go_indicators = [
            "go.mod",
            "go.sum",
        ]
        if any((project_root / f).exists() for f in go_indicators):
            return "go"

        # Default fallback
        return "python"

    @classmethod
    def supported_languages(cls) -> list[str]:
        """Return list of supported language names."""
        return list(cls._checkers.keys())

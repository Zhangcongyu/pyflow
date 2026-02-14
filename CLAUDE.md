# CLAUDE.md - Python Project Memory

This file provides Python-specific guidance for this repository.

---

## 🐍 Technology Stack

### Core Tools
- **uv** - Package manager (virtual env, dependencies, building)
- **ruff** - Linting + formatting (replaces black, flake8, isort)
- **pytest** - Testing framework
- **mypy** - Type checking

---

## ⚙️ Essential Commands

### Environment & Dependencies
```bash
uv venv                    # Create virtual environment
source .venv/bin/activate  # Activate (Linux/Mac)
uv sync                    # Install dependencies
uv add <package>           # Add package
uv remove <package>        # Remove package
```

### Testing & Code Quality
```bash
pytest -v --cov            # Run tests with coverage
ruff format .              # Format code
ruff check --fix .         # Lint and auto-fix issues
mypy src/                  # Type checking
```

---

## ✅ Modern Python Practices

### Code Style
- **Use pathlib instead of os.path** - Modern path handling
- **Use f-strings for formatting** - Cleaner than .format() or %
- **Use type hints on all functions** - Better IDE support and type safety
- **Use dataclasses for data containers** - Less boilerplate
- **Use context managers (with statements)** - Automatic resource cleanup

### Example
```python
from pathlib import Path
from typing import Optional

def process_data(file_path: Path, max_items: Optional[int] = None) -> list[str]:
    """Process data from file with optional limit."""
    data = file_path.read_text(encoding='utf-8').splitlines()

    if max_items is not None:
        data = data[:max_items]

    return [line.strip() for line in data if line.strip()]
```

---

## ❌ Python Anti-Patterns (NEVER DO)

### Code Quality
- ❌ **Use os.path** - Use pathlib instead
- ❌ **Use .format() or %** - Use f-strings
- ❌ **Use mutable defaults** - e.g., `def foo(x=[])` is wrong
- ❌ **Skip type hints** - All functions should have type annotations
- ❌ **Leave commented-out code** - Delete it, don't comment it
- ❌ **Mix incompatible tools** - Don't use black + ruff together

### Dependencies
- ❌ **Use pip globally** - Only use uv for package management

---

## 🎯 Quality Standards

### Testing
- Mirror source structure in `tests/`
- Follow AAA pattern (Arrange-Act-Assert)
- Aim for 90%+ test coverage
- Mock external services and dependencies

### Type Safety
- All functions must have type hints
- No `any` types without justification
- No `# type: ignore` without explanation
- Run `mypy` before committing

### Code Style
- Follow PEP 8 with 88 character line limit
- Use descriptive names (snake_case for variables/functions)
- Use UPPER_SNAKE_CASE for constants
- Prefix private methods with underscore

### Documentation
- Use docstrings for public APIs
- Chinese comments allowed for complex logic
- English for code and variable names

---

## 📋 Development Workflow

### Initial Setup
```bash
uv venv
source .venv/bin/activate
uv sync
```

### Daily Development
1. Write code with type hints
2. Run tests regularly: `pytest -v`
3. Format code: `ruff format .`
4. Check linting: `ruff check --fix .`
5. Type check: `mypy src/`

### Before Committing
Run all quality checks:
```bash
pytest -v --cov && ruff format . && ruff check --fix . && mypy src/
```

---

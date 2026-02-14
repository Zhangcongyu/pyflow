# ProjectFlow

> **Intelligent Project Development Orchestration Pipeline** - Full-process automation for project creation and feature development

ProjectFlow is an intelligent project development orchestration system based on Claude Code. Through collaboration of three core components, it achieves complete automation from project creation to feature iteration.

---

**Language**: [English](README.md) | [简体中文](README.zh-CN.md)

---

## Table of Contents

- [Core Features](#core-features)
- [Architecture Overview](#architecture-overview)
- [Quick Start](#quick-start)
- [Core Components](#core-components)
- [Workflow](#workflow)
- [Version Management](#version-management)
- [Usage Examples](#usage-examples)
- [Supported Languages](#supported-languages)

---

## Core Features

### Three-Dimensional Intelligent Detection

- **Project Status Detection**: Automatically identify new projects (`--new`) vs existing projects (`--add-feature`)
- **Complexity Assessment**: Intelligently determine project complexity (`--simple` / `--medium` / `--complex`)
- **Language Type Recognition**: Support for Python, TypeScript, Go, and other programming languages

### Automated Orchestration

- **Environment Detection**: Automatically analyze Git, virtual environments, and project structure
- **Template-Driven**: Automatically generate executable plans based on comprehensive templates
- **Versioned Management**: Independent version directories for each iteration with complete history tracking

### TDD Principles

- **Test-Driven Development**: Enforce TDD toolchain for business logic development
- **Quality Gates**: CHECKLIST validation for each phase
- **Compliance Checking**: Mandatory reading of project constitution and requirements documents

### Language Agnostic

- **Universal Executor**: Executor is language-agnostic, focusing only on process orchestration
- **Extensible Architecture**: Easy to support new languages and toolchains

---

## Architecture Overview

```
User Request
    ↓
┌─────────────────────────────────────────┐
│  projectflow-router (3D Detector)       │
│  - Detect project status (new/existing) │
│  - Detect complexity (simple/medium/complex) │
│  - Detect language (Python/TS/Go)       │
│  - Pass parameters to planner          │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│  projectflow-planner (Plan Generator)   │
│  - Detect project environment           │
│  - Determine version directory          │
│  - Read comprehensive template          │
│  - Transform template content           │
│  - Generate task_plan.md               │
│  - Invoke executor                     │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│  projectflow-executor (Executor)        │
│  - Read task_plan.md                   │
│  - Find next pending Phase             │
│  - Verify documents (constitution, reqs)│
│  - Invoke Tool                         │
│  - Validate output                     │
│  - Update CHECKLIST & progress         │
│  - Mark Phase complete                │
└─────────────────────────────────────────┘
```

---

## Quick Start

### Create New Project

```bash
# User request example
"Help me create a simple Python CLI tool"

# ProjectFlow automatic execution
# 1. Router detects: --new --simple --python
# 2. Planner generates plan: pjflow/v0_initial/task_plan.md
# 3. Executor executes: Phase 1 → Phase 2 → Phase 4 → Phase 5
```

### Add Feature to Existing Project

```bash
# User request example
"Add a user authentication API to this project"

# ProjectFlow automatic execution
# 1. Router detects: --add-feature --medium --python
# 2. Planner generates plan: pjflow/v1_auth_api/task_plan.md
# 3. Executor executes: Phase 0 → Phase 3 → Phase 4 → Phase 5
```

---

## Core Components

### 1. projectflow-router (3D Detector)

**Responsibility**: Pure detector responsible for parameter passing and routing, does not execute any implementation work

**Detection Dimensions**:

| Dimension | Parameters | Description |
|-----------|-------------|--------------|
| **Project Status** | `--new` / `--add-feature` | New project vs existing project adding feature |
| **Project Complexity** | `--simple` / `--medium` / `--complex` | Simple / Medium / Complex |
| **Language Type** | `--python` / `--typescript` / `--go` | Python / TypeScript / Go |

**Detection Rules**:

- **New Project Signals**: "create", "new", "build from scratch", empty directory, no project config files
- **Existing Project Signals**: "add", "extend", "add feature", existing project config files
- **Complexity Keywords**:
  - Simple: "simple", "small", "quick", "single feature", "utility"
  - Medium: "medium", "several features", "API", "CRUD", "data processing"
  - Complex: "complex", "large-scale", "complete system", "platform", "framework", "high-performance"

### 2. projectflow-planner (Plan Generator)

**Responsibility**: Detect environment → Read template → Generate executable plan → Invoke executor

**Core Process**:

```
3D parameters input
   ↓
Step 1: Detect project environment
   ↓
Step 2: Determine version directory
   ↓
Step 3: Read comprehensive template
   ↓
Step 4: Transform template content
   ↓
Step 5: Generate task_plan.md
   ↓
Step 6: Invoke executor
```

**Environment Detection**:

```bash
python .claude/skills/projectflow-planner/scripts/detect_environment.py --json
```

**Output Fields**: Git status, virtual environment, project structure, project type, etc.

### 3. projectflow-executor (Executor)

**Responsibility**: Execute plan phase by phase, update status and CHECKLIST, validate compliance

**Orchestration Principles**:

- ✅ **Can**: Create scaffolding (project infrastructure configuration)
- ❌ **Cannot**: Write business logic code (must use TDD toolchain)
- 🌍 **Language Agnostic**: Applicable to any programming language

**Four-Step Execution Flow** (Each phase must strictly follow):

1. **Invoke tool/skill/agent** → Use Skill/Task/Bash tools
2. **Wait for completion** ⏸️ → Pause all operations, wait for tool return
3. **Validate result** ✓ → Check if output meets expectations
4. **Record status** 📝 → Update status, proceed to next phase

---

## Workflow

### Phase Execution Strategy

| Phase | New Project | Add Feature | Description |
|-------|-------------|-------------|--------------|
| **Phase 0**: Requirements Interaction | medium/complex | medium/complex | Use brainstorming to explore requirements |
| **Phase 1**: Project Rules | ✅ | ❌ | Create constitution.md |
| **Phase 2**: Project Build | ✅ | ❌ | Create project scaffolding |
| **Phase 3**: Worktree Preparation | ❌ | ✅ | Create feature branch, add dependencies |
| **Phase 4**: TDD Execution | ✅ | ✅ | Implement features using TDD tools |
| **Phase 5**: Quality Review | ✅ | ✅ | Quality check and Git commit |

### Scaffold vs Business Logic Judgment Criteria

- **Is this scaffolding?** (All projects need it) → Use **Write/Bash** tools ✅
- **Is this business logic?** (Contains specific functionality) → Use **TDD tools** ❌

**Examples**:
```
Phase 2 (Project Setup)  → Scaffold → Use Write tool to create directories and configs ✅
Phase 4 (TDD Execution)   → Business Logic → Invoke pyflow-tdd-cycle ❌
```

---

## Version Management

### Directory Structure

```
pjflow/
├── constitution.md      # Project-level constitution (shared)
├── requirements.md       # Requirements document (optional)
│
├── v0_initial/          # New project
│   ├── task_plan.md
│   ├── progress.md
│   ├── findings.md
│   └── CHECKLIST.md
│
├── v1_add_feature/      # 1st feature addition
│   ├── task_plan.md
│   ├── progress.md
│   └── findings.md
│
└── v{N}_feature/        # Nth feature addition
    └── ...
```

### Version Directory Naming Rules

| Project Status | Version Directory Name | Description |
|----------------|------------------------|--------------|
| new (new project) | `v0_initial` | Fixed name |
| add-feature (add feature) | `v{N}_{feature_name}` | N is incremental version number |

### Automatic Version Number Increment

```bash
existing_versions=$(find ./pjflow -maxdepth 1 -type d -name "v*" 2>/dev/null | sort -V)
if [ -z "$existing_versions" ]; then
    next_version=1
else
    max_version=$(echo "$existing_versions" | tail -1 | sed 's/v//')
    next_version=$((max_version + 1))
fi
echo "Next version: v${next_version}"
```

---

## Usage Examples

### Example 1: Create Simple Python CLI Tool

**User Request**: "Help me create a simple Python CLI tool"

**Router Detection**:
```bash
Skill(skill="projectflow-planner", args="--new --simple --python Help me create a simple Python CLI tool")
```

**Planner Execution**:
1. Detect environment (no Git, no virtual environment)
2. Determine version directory: `v0_initial`
3. Read `python-complete-template.md`
4. Generate `pjflow/v0_initial/task_plan.md` (Phase 1, 2, 4, 5)
5. Invoke executor

**Executor Execution**:
- **Phase 1**: Invoke `pyflow-constitution` to create constitution
- **Phase 2**: Create project scaffolding (pyproject.toml, src/, tests/)
- **Phase 4**: Invoke `pyflow-tdd-cycle` to implement features
- **Phase 5**: Quality review and Git commit

### Example 2: Add Medium Complexity API Feature to Existing Python Project

**User Request**: "Add a user authentication API to this project"

**Router Detection**:
```bash
Skill(skill="projectflow-planner", args="--add-feature --medium --python Add a user authentication API to this project")
```

**Planner Execution**:
1. Detect environment (Git and project structure already exist)
2. Determine version directory: `v1_auth_api`
3. Read `python-complete-template.md`
4. Generate `pjflow/v1_auth_api/task_plan.md` (Phase 0, 3, 4, 5)
5. Invoke executor

**Executor Execution**:
- **Phase 0**: Invoke `pyflow-brainstorming` to explore requirements
- **Phase 3**: Create feature branch, add dependencies
- **Phase 4**: Invoke `pyflow-tdd-cycle` to implement API
- **Phase 5**: Quality review and PR

---

## Supported Languages

| Language | Template File | Complexity Support | TDD Tool | Config File |
|----------|---------------|-------------------|----------|--------------|
| **Python** | `python-complete-template.md` | ✅ simple/medium/complex | `pyflow-tdd-cycle` | `pyproject.toml` |
| **TypeScript** | `typescript-complete-template.md` | ✅ simple/medium/complex | `tdd-typescript-tool` | `package.json` |
| **Go** | `go-template.md` | ⚠️ Basic structure | `go-tdd-tool` | `go.mod` |
| **Rust** | - | 🚧 Planned | `cargo-tdd-tool` | `Cargo.toml` |
| **Java** | - | 🚧 Planned | `junit-tdd-tool` | `pom.xml` |

---

## CHECKLIST Management

### Update Timing

| Phase | Update Content |
|-------|----------------|
| Phase 0 | Requirements analysis related checkboxes |
| Phase 1 | Project rules related checkboxes |
| Phase 2 | Project preparation related checkboxes (including conflict detection) |
| Phase 3 | Work environment related checkboxes (including Git branch, dependencies, system files, new files) |
| Phase 4 | TDD execution related checkboxes |
| Phase 5 | Quality review and Git related checkboxes |

### Update Method

Use **Edit tool** to replace `[ ]` with `[x]`:

```python
Edit(
    file_path="pjflow/v0_initial/CHECKLIST.md",
    old_string="- [ ] Constitution created/updated",
    new_string="- [x] Constitution created/updated"
)
```

**Important**: Unupdated CHECKLIST is considered incomplete Phase!

---

## FAQ

### Q: Why can't Executor write business code directly?

A: ProjectFlow enforces using TDD toolchain for business logic to ensure:
- Test-first principle
- Controllable code quality
- Compliance with project constitution requirements
- Traceability and maintainability

### Q: How to verify Executor executed correctly?

A: After each Phase completion, must:
1. Tool execution completed without errors
2. Output meets constitution.md requirements
3. CHECKLIST.md updated
4. progress.md updated
5. Phase status marked as complete

### Q: How are version directories managed automatically?

A: Planner automatically calculates the next version number:
- New projects always use `v0_initial`
- Adding features automatically increments version number (v1, v2, v3...)

---

## Version Information

- **Router**: 4.0.0 - 3D Detector (Language Agnostic)
- **Planner**: 4.1.0 - Environment Detection + Template Transformation + Plan Generation
- **Executor**: 4.0.0 - Phase-by-Phase Executor (Language Agnostic)

---

## Documentation

- [Complete Workflow Documentation](docs/projectflow-workflow.md)
- [Router Skill Description](.claude/skills/projectflow-router/SKILL.md)
- [Planner Skill Description](.claude/skills/projectflow-planner/SKILL.md)
- [Executor Skill Description](.claude/skills/projectflow-executor/SKILL.md)

---

## License

MIT License

---

**ProjectFlow** - Make project development smarter, make code quality more reliable!

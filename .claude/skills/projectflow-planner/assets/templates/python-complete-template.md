# Python 项目完整计划模板

**说明**: 此模板包含 Python 项目所有场景（simple/medium/complex）的完整 Phase 0-5 流程，planner 可直接阅读此文件生成可执行的 plan.md

---

## 模板变量

| 变量 | 说明 | 示例值 |
|--------|------|----------|
| `{{GOAL}}` | 用户原始需求 | "创建一个 FastAPI 待办事项应用" |
| `{{PROJECT_STATUS}}` | new / add-feature | new |
| `{{COMPLEXITY}}` | simple / medium / complex | simple |
| `{{VERSION_DIR}}` | 版本目录名称 | v0_initial / v1_add_feature |
| `{{LANGUAGE}}` | 编程语言 | python |

---

## Phase 0: 需求互动

**适用场景**: `{{COMPLEXITY}}` == medium 或 complex

**Tool**: pyflow-brainstorming

**参数**: `--version-dir {{VERSION_DIR}} {{GOAL}}`

**执行**: 探索用户需求，明确功能边界，输出到版本化需求文档

**调用**:
```
Skill(
    skill="pyflow-brainstorming",
    args="--version-dir {{VERSION_DIR}} {{GOAL}}"
)
```

**输出位置**: `pjflow/{{VERSION_DIR}}/requirements.md`

**CHECKLIST**:
- [ ] 需求分析完成
- [ ] 功能边界明确
- [ ] 技术方案确认
- [ ] 需求文档已创建到 pjflow/{{VERSION_DIR}}/requirements.md

---

## Step 5.5: 简单项目需求文档生成

**适用场景**: `{{PROJECT_STATUS}}` == new 且 `{{COMPLEXITY}}` == simple

**执行时机**: Phase 1 完成后

**说明**: Simple 项目不需要 Phase 0 brainstorming，直接生成需求文档模板

**工具**: Write

**执行**:
```
Write(
    file_path="pjflow/{{VERSION_DIR}}/requirements.md",
    content="""# Requirements

**Project Type**: {{PROJECT_STATUS}}
**Complexity**: simple
**Goal**: {{GOAL}}

---

## Project Overview

{{GOAL}}

## Core Features

### Feature 1
- Description:
- Acceptance Criteria:
- Priority:

## Technical Requirements

- Performance requirements:
- Security requirements:
- Compatibility requirements:

## Success Criteria

1.
2.
3.

---
*Created: {{PROJECT_STATUS}} - simple*
"""
)
```

**输出位置**: `pjflow/{{VERSION_DIR}}/requirements.md`

**CHECKLIST**:
- [ ] 需求文档已创建
- [ ] 输出路径正确

**Skip if**: `{{COMPLEXITY}}` != simple（medium/complex 项目通过 Phase 0 brainstorming 生成需求）

---

## Phase 1: 项目规则

**适用场景**: `{{PROJECT_STATUS}}` == new

**Tool**: pyflow-constitution

**执行**: 创建项目宪法文档 `pjflow/constitution.md`（共享，所有版本使用同一个）

**CHECKLIST**:
- [ ] Constitution 创建/更新
- [ ] 项目规则定义

**Skip if**: 老项目（`{{PROJECT_STATUS}}` == add-feature）

---

## Phase 2: 项目构建

**适用场景**: `{{PROJECT_STATUS}}` == new

### 2.0 干扰检测与清理

**Tool**: Bash + 用户确认

**检测逻辑**:
```bash
# 检测是否存在冲突目录
CONFLICT_DIRS="src tests .venv venv __pycache__"
CONFLICT_FILES="pyproject.toml setup.py requirements.txt package.json"

for dir in $CONFLICT_DIRS; do
    if [ -d "$dir" ]; then
        HAS_CONFLICT=true
        break
    fi
done

if [ "$HAS_CONFLICT" = true ]; then
    # 使用 AskUserQuestion 询问用户
    问题："检测到目录中已存在项目文件 (src/, tests/ 等)，是否删除并重新创建？"
    选项：
      - "是，删除并重新创建"
      - "否，取消操作"

    # 根据用户选择执行
fi
```

**CHECKLIST**:
- [ ] 冲突检测完成
- [ ] 用户确认
- [ ] 清理命令准备
- [ ] 目录已清理（如需要）

---

### 2.1 Git 仓库

**Tool**: Bash

**前置检测**:
- Git 是否已存在
- 当前分支名称

**判断逻辑**:
```bash
# 检查 Git 是否已初始化
if git rev-parse --git-dir > /dev/null 2>&1; then
    GIT_EXISTS=true
else
    GIT_EXISTS=false
fi

echo "Git 仓库状态: $GIT_EXISTS"
```

**执行**:
```bash
# 如果未初始化
if [ "$GIT_EXISTS" = false ]; then
    git init
    git branch -M main
    echo "Git 仓库已初始化"
fi

# 创建 .gitignore
Write(file_path=".gitignore", content="# Virtual Environment
.venv/
venv/
__pycache__/

# Testing
.pytest_cache/
.pytest_cache/
.coverage
htmlcov/
.tox/

# Build
dist/
*.egg-info/
build/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
")
```

**CHECKLIST**:
- [ ] Git 仓库初始化/确认
- [ ] .gitignore 创建

---

### 2.2 项目架构

**Tool**: Write / Bash

**项目类型判断**:

根据用户需求关键词和环境检测，选择项目架构：

| 关键词 | 项目类型 | 目录结构 |
|--------|----------|----------|
| CLI, 命令行, 工具 | **cli** | 2-3 层 |
| Library, 库, SDK, 框架 | **library** | 2-3 层 |
| FastAPI, API, REST, async | **fastapi** | 多层，使用 pyflow-fastapi-pro |
| Django, 全栈, 管理系统 | **django** | 多层 |
| Data, 数据处理, ETL, 分析 | **data** | 深层 |
| ML, 机器学习, AI, 模型 | **ml** | 深层 |

**CLI 架构** (simple/medium):
```
project-name/
├── src/
│   └── project_name/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py
│       └── commands/
│           └── __init__.py
└── tests/
    ├── __init__.py
    ├── conftest.py
    └── test_cli.py
```

**Library 架构** (simple/medium):
```
project-name/
├── src/
│   └── project_name/
│       ├── __init__.py
│       ├── core.py
│       └── utils.py
└── tests/
    ├── __init__.py
    ├── test_core.py
    └── test_utils.py
```

**FastAPI 架构** (medium/complex):
```
project-name/
├── src/
│   └── project_name/
│       ├── __init__.py
│       ├── main.py
│       ├── config.py
│       ├── api/
│       │   ├── __init__.py
│       │   └── v1/
│       │       ├── __init__.py
│       │       └── router.py
│       ├── core/
│       │   ├── __init__.py
│       │   ├── database.py
│       │   ├── security.py
│       ├── models/
│       │   ├── __init__.py
│       │   └── user.py
│       └── services/
│           └── __init__.py
└── tests/
    ├── __init__.py
    ├── conftest.py
    └── api/
        └── v1/
            └── __init__.py
```

**执行**:
```bash
# 根据选择的架构类型创建目录
# 示例：创建 FastAPI 项目架构
mkdir -p src/project_name/{api/v1,core,models,services}
mkdir -p tests/project_name/api/v1

# 创建 __init__.py 文件
for dir in src/project_name/api src/project_name/api/v1 core models services; do
    mkdir -p src/project_name/$dir
    touch src/project_name/$dir/__init__.py
done
```

**CHECKLIST**:
- [ ] 架构类型已选择
- [ ] 目录结构已创建
- [ ] __init__.py 文件已生成

---

### 2.3 系统文件

**Tool**: Write

**pyproject.toml**:
```toml
[project]
name = "project-name"
version = "0.1.0"
description = "{{GOAL}}"
requires-python = ">=3.10"
dependencies = [
    # 根据项目类型添加依赖
    # CLI: click, typer
    # FastAPI: fastapi, "uvicorn[standard]", pydantic
    # Django: django
    # Data: pandas, numpy
    # ML: torch, scikit-learn
]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]

[tool.coverage.run]
source = ["src"]

[tool.ruff]
line-length = 88
target-version = "py310"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP"]

[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

# 中文环境镜像源配置
[[tool.uv.index]]
url = "https://mirrors.aliyun.com/pypi/simple"
default = true

[tool.uv.pip]
index-url = "https://repo.huaweicloud.com/repository/pypi/simple"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

**.gitignore**: 见 2.1

**README.md**:
```markdown
# Project Name

{{GOAL}}

## Setup

\`\`\`bash
# 使用 uv (推荐）
uv venv
source .venv/bin/activate
uv pip install -e .

# 或使用 venv
python -m venv .venv
source .venv/bin/activate
pip install -e .
\`\`\`

## Development

\`\`\`bash
# Run tests
pytest

# Format code
ruff format .

# Check linting
ruff check .

# Run with coverage
pytest --cov=src --cov-report=term-missing
\`\`\`

## Compliance

Run compliance checks:
\`\`\`bash
python .claude/skills/projectflow-executor/scripts/check_compliance.py --version-dir {{VERSION_DIR}}
\`\`\`
```

---

### 2.4 项目文件

**Tool**: Write

**原则**: 创建空占位文件，**严禁编写业务逻辑**

**Python 文件模板**:
```python
# -*- coding: utf-8 -*-
"""
{{MODULE_DESCRIPTION}}

__all__ = []
```

**执行**:
```bash
# 创建空文件
for dir in src/project_name; do
    for subdir in $(find src/project_name -type d -mindepth 1); do
        mkdir -p src/project_name/$subdir
        touch src/project_name/$subdir/__init__.py
done
```

**CHECKLIST**:
- [ ] 所有目录已创建
- [ ] 占位文件已生成
- [ ] 无业务逻辑代码

---

### 2.5 虚拟环境

**Tool**: Skill (pyflow-uv-package-manager)

**前置检测**:
- 虚拟环境类型
- 是否已存在

**执行**:
```bash
# 创建 Python 虚拟环境
uv venv

# 激活并安装依赖（根据项目类型）
uv pip install -e .
```

**CHECKLIST**:
- [ ] 虚拟环境创建
- [ ] 依赖已安装

---

## Phase 3: 工作树准备（老项目）

**适用场景**: `{{PROJECT_STATUS}}` == add-feature

**Skip if**: 新项目（`{{PROJECT_STATUS}}` == new）

**前置步骤**: 创建版本化需求文档
```python
from scripts.document_manager import DocumentManager, create_requirements_template

doc_manager = DocumentManager(Path("./pjflow"))
requirements_content = create_requirements_template(
    goal="{{GOAL}}",
    project_type="add-feature",
    complexity="{{COMPLEXITY}}"
)
doc_manager.create_versioned_requirements(
    "{{VERSION_DIR}}",
    requirements_content
)
```

### 3.1 Git 分支管理

**Tool**: Bash

**执行**:
```bash
# 检查当前分支
CURRENT_BRANCH=$(git branch --show-current)
echo "当前分支: $CURRENT_BRANCH"

# 创建 feature 分支
FEATURE_NAME="{{VERSION_DIR}}"  # 例如: v1_add_percentage
git checkout -b feature/"$FEATURE_NAME"

echo "已创建并切换到分支: feature/$FEATURE_NAME"
```

**CHECKLIST**:
- [ ] 当前分支确认
- [ ] Feature 分支创建成功
- [ ] 分支命名符合规范
- [ ] 需求文档已创建

---

### 3.2 依赖管理

**Tool**: Skill (pyflow-uv-package-manager)

**执行**:
```bash
# 添加新功能所需的依赖
uv add fastapi uvicorn pydantic sqlalchemy
```

**CHECKLIST**:
- [ ] 依赖已添加到 pyproject.toml
- [ ] 依赖已安装到虚拟环境
- [ ] 无依赖冲突

---

### 3.3 系统文件更新

**Tool**: Edit

**执行**:
- 更新 README.md 添加新功能说明
- 更新版本号（如需要）

**CHECKLIST**:
- [ ] README.md 已更新
- [ ] 版本号已更新（如需要）
- [ ] 变更日志已记录

---

### 3.4 新功能文件创建

**Tool**: Write

**原则**: 创建空文件，不编写业务逻辑

**执行**:
```bash
# 根据功能需求确定需要新增的文件
# 创建占位文件
mkdir -p src/project_name/new_feature
touch src/project_name/new_feature/__init__.py
```

**CHECKLIST**:
- [ ] 新增目录已创建
- [ ] 占位文件已生成
- [ ] 无业务逻辑代码
- [ ] 与现有架构一致

---

## Phase 4: TDD 执行

**适用场景**: 所有项目

**🚨 强制要求**:
- **严禁手动创建业务代码文件**
- **严禁手动编写业务逻辑**
- 必须使用 TDD 工具完成所有编码工作

**📋 文档注入**（所有 Phase 4 子阶段）

在每个 Phase 4 子阶段调用 Tool 之前，必须注入文档上下文：

```python
# 读取文档
constitution = Read("./pjflow/constitution.md")
requirements = Read("./pjflow/{{VERSION_DIR}}/requirements.md")

# 构建增强的提示
enhanced_prompt = f"""
{original_prompt}

## 🚨 强制约束（必须遵守）

### 项目宪法 (Constitution)
{constitution}

### 需求文档 (Requirements)
{requirements}

**重要**: 违反上述约束的代码将被拒绝！必须确保所有代码符合宪法要求和需求范围。
"""
```

### Simple 项目 ({{COMPLEXITY}} == simple)

**Tool**: pyflow-tdd-cycle

**执行**: 单次 TDD 循环（RED → GREEN → REFACTOR）

**前置步骤**: 读取文档并构建增强提示

```python
# 读取文档
constitution = Read("./pjflow/constitution.md")
requirements = Read("./pjflow/{{VERSION_DIR}}/requirements.md")

# 构建增强提示
enhanced_args = f"""{{GOAL}} --single-cycle

## 🚨 强制约束（必须遵守）

### 项目宪法
{constitution}

### 需求文档
{requirements}

**重要**: 违反上述约束的代码/测试将被拒绝！
"""
```

**调用**:
```
Skill(skill="pyflow-tdd-cycle", args=enhanced_args)
```

**后置步骤**: 执行合规检查
```bash
# 运行合规检查脚本
python .claude/skills/projectflow-executor/scripts/check_compliance.py \
    --language python \
    --version-dir {{VERSION_DIR}} \
    --phase tdd-simple
```

**CHECKLIST**:
- [ ] RED Phase: 测试编写
- [ ] GREEN Phase: 最小实现通过测试
- [ ] REFACTOR Phase: 代码重构
- [ ] 所有测试通过
- [ ] 无手动编码
- [ ] 合规检查已执行
- [ ] 合规报告已生成
- [ ] Critical/High 问题已处理（如存在）

---

### Medium 项目 ({{COMPLEXITY}} == medium)

**执行方式**: RED → GREEN → REFACTOR 三阶段

#### Phase 4.1: RED - 生成测试

**前置步骤**: 注入文档上下文

**Tool**: pyflow-test-automator

**Tool Type**: Task (subagent_type)

**执行**: 生成完整测试套件

**调用**:
```
Task(
    subagent_type="pyflow-test-automator",
    subject="生成测试套件",
    description=f"""为 {{GOAL}} 生成完整测试套件

## 🚨 强制约束（必须遵守）

### 项目宪法
{constitution}

### 需求文档
{requirements}

**重要**: 测试必须覆盖所有需求功能和宪法标准！
""",
    activeForm="生成测试套件"
)
```

**CHECKLIST**:
- [ ] Test files generated
- [ ] Test structure defined
- [ ] Test cases cover requirements
- [ ] Tests cover Constitution standards
- [ ] 合规检查已执行（RED 阶段后）

---

#### Phase 4.2: GREEN - 实现功能

**前置步骤**: 注入文档上下文

**Tool**: pyflow-python-pro (或 pyflow-fastapi-pro，如果项目类型是 FastAPI)

**Agent 选择逻辑**：
根据项目类型选择 agent：
- FastAPI 项目 → pyflow-fastapi-pro
- 其他 Python 项目 → pyflow-python-pro

**Tool Type**: Task (subagent_type)

**执行**: 实现所有功能使测试通过

**调用**:
```
Task(
    subagent_type="pyflow-fastapi-pro",  // ← FastAPI 时使用
    subject="实现功能使测试通过",
    description=f"""实现所有功能使测试通过

## 🚨 强制约束（必须遵守）

### 项目宪法
{constitution}

### 需求文档
{requirements}

**重要**: 代码必须符合宪法要求，且在需求范围内！违反约束的代码将被拒绝！
""",
    activeForm="实现功能"
)
```

**后置步骤**: 执行合规检查
```bash
python .claude/skills/projectflow-executor/scripts/check_compliance.py \
    --language python \
    --version-dir {{VERSION_DIR}} \
    --phase green
```

**CHECKLIST**:
- [ ] All features implemented
- [ ] All tests pass
- [ ] Code follows constitution
- [ ] Code within Requirements scope
- [ ] 合规检查已执行
- [ ] 合规报告已生成
- [ ] Critical/High 问题已处理（如存在）

---

#### Phase 4.3: REFACTOR - 重构代码

**前置步骤**: 注入文档上下文

**Tool**: pyflow-python-pro

**Tool Type**: Task (subagent_type)

**执行**: 优化代码结构和质量

**调用**:
```
Task(
    subagent_type="pyflow-python-pro",
    subject="重构优化代码",
    description=f"""优化代码结构和质量

## 🚨 强制约束（必须遵守）

### 项目宪法
{constitution}

### 需求文档
{requirements}

**重要**: 重构不能违反宪法原则，且必须在需求范围内！
""",
    activeForm="重构优化"
)
```

**后置步骤**: 最终合规检查
```bash
python .claude/skills/projectflow-executor/scripts/check_compliance.py \
    --language python \
    --version-dir {{VERSION_DIR}} \
    --phase refactor
```

**CHECKLIST**:
- [ ] Code refactored
- [ ] All tests still pass
- [ ] Code quality improved
- [ ] Performance optimized (if needed)
- [ ] Refactor preserves Constitution compliance
- [ ] 合规检查已执行
- [ ] 最终合规报告已生成
- [ ] 所有合规问题已处理

---

### Complex 项目 ({{COMPLEXITY}} == complex)

**执行方式**: 扩展 TDD 循环

#### Phase 4.1: RED - 生成完整测试

**前置步骤**: 注入文档上下文

**Tool**: pyflow-test-automator

**调用**:
```
Task(
    subagent_type="pyflow-test-automator",
    subject="生成完整测试套件",
    description=f"""为 {{GOAL}} 生成单元测试、集成测试、性能测试、安全测试

## 🚨 强制约束

### 项目宪法
{constitution}

### 需求文档
{requirements}
""",
    activeForm="生成测试套件"
)
```

**CHECKLIST**:
- [ ] Unit tests generated
- [ ] Integration tests defined
- [ ] Performance tests defined
- [ ] Security tests defined
- [ ] Tests cover Requirements and Constitution standards
- [ ] 架构审核完成
- [ ] 合规检查已执行

---

#### Phase 4.2: GREEN - 基础实现

**前置步骤**: 注入文档上下文

**Tool**: pyflow-python-pro (或 pyflow-fastapi-pro)

**调用**:
```
Task(
    subagent_type="pyflow-fastapi-pro",
    subject="实现基础功能",
    description=f"""实现所有功能使测试通过

## 🚨 强制约束

### 项目宪法
{constitution}

### 需求文档
{requirements}
""",
    activeForm="实现基础功能"
)
```

**后置步骤**: 合规检查
```bash
python .claude/skills/projectflow-executor/scripts/check_compliance.py \
    --language python \
    --version-dir {{VERSION_DIR}} \
    --phase green
```

**CHECKLIST**:
- [ ] Basic implementation completed
- [ ] All unit tests pass
- [ ] Code follows constitution
- [ ] Code within Requirements scope
- [ ] 合规检查已执行

---

#### Phase 4.3: GREEN - 异步优化（如需要）

**前置步骤**: 注入文档上下文

**Tool**: pyflow-async-python-patterns

**执行**: 添加异步支持提高性能

**调用**:
```
Skill(skill="pyflow-async-python-patterns", args=f"""添加异步支持以提高性能

## 🚨 强制约束

### 项目宪法
{constitution}

### 需求文档
{requirements}

**重要**: 异步模式必须符合宪法要求，且满足需求中的性能指标！
""")
```

**后置步骤**: 合规检查

**CHECKLIST**:
- [ ] Async patterns implemented
- [ ] All tests still pass
- [ ] Performance improved
- [ ] Async patterns follow Constitution requirements
- [ ] 合规检查已执行

**Skip if**: `{{PROJECT_STATUS}}` == new 或项目不需要异步

---

#### Phase 4.4: GREEN - 性能优化

**前置步骤**: 注入文档上下文

**Tool**: pyflow-python-performance-optimization

**执行**: 分析并优化性能瓶颈

**调用**:
```
Skill(skill="pyflow-python-performance-optimization", args=f"""分析并优化性能瓶颈

## 🚨 强制约束

### 项目宪法
{constitution}

### 需求文档
{requirements}

**重要**: 性能优化必须符合宪法要求，且达到需求中的性能指标！
""")
```

**后置步骤**: 合规检查

**CHECKLIST**:
- [ ] Performance profiled
- [ ] Bottlenecks identified
- [ ] Optimizations applied
- [ ] Performance targets met
- [ ] 合规检查已执行

**Skip if**: 项目没有性能要求

---

#### Phase 4.5: REFACTOR - 深度优化

**前置步骤**: 注入文档上下文

**Tool**: pyflow-python-performance-optimization

**执行**: 应用高级优化技术

**调用**:
```
Task(
    subagent_type="pyflow-python-performance-optimization",
    subject="深度性能优化",
    description=f"""应用高级优化技术

## 🚨 强制约束

### 项目宪法
{constitution}

### 需求文档
{requirements}

**重要**: 深度优化必须符合宪法原则，且在需求范围内！
""",
    activeForm="深度优化"
)
```

**后置步骤**: 合规检查

**CHECKLIST**:
- [ ] Advanced optimizations applied
- [ ] Code quality excellent
- [ ] All tests still pass
- [ ] Performance significantly improved
- [ ] Refactor preserves Constitution compliance
- [ ] 合规检查已执行

---

#### Phase 4.6: REFACTOR - 最终清理

**前置步骤**: 注入文档上下文

**Tool**: pyflow-python-pro

**执行**: 清理代码、更新文档

**调用**:
```
Task(
    subagent_type="pyflow-python-pro",
    subject="最终代码清理",
    description=f"""清理代码、更新文档、确保代码质量

## 🚨 强制约束

### 项目宪法
{constitution}

### 需求文档
{requirements}

**重要**: 最终清理必须符合宪法所有标准，且满足需求！
""",
    activeForm="清理代码"
)
```

**后置步骤**: 最终合规检查
```bash
python .claude/skills/projectflow-executor/scripts/check_compliance.py \
    --language python \
    --version-dir {{VERSION_DIR}} \
    --phase final
```

**CHECKLIST**:
- [ ] Code cleaned up
- [ ] Documentation updated
- [ ] All tests pass
- [ ] Code quality excellent
- [ ] Final code follows all Constitution standards
- [ ] 最终合规报告已生成
- [ ] 所有合规问题已处理

---

## Phase 5: 质量审核

**适用场景**: 所有项目

### Simple 项目

#### 5.1 自动化合规检查

**Tool**: Bash

**执行**:
```bash
# 运行完整合规检查
python .claude/skills/projectflow-executor/scripts/check_compliance.py \
    --language python \
    --version-dir {{VERSION_DIR}} \
    --phase quality
```

**CHECKLIST**:
- [ ] 合规检查已执行
- [ ] 合规报告已生成到 pjflow/{{VERSION_DIR}}/compliance_report.md
- [ ] 无 Critical 级别问题
- [ ] High 级别问题已处理（如存在）

---

#### 5.2 质量检查

**Tool**: Bash

**执行**:
```bash
pytest tests/ -v
ruff check src/
mypy src/
```

**CHECKLIST**:
- [ ] All tests pass (100%)
- [ ] Code style checks pass (ruff)
- [ ] Type checks pass (mypy)
- [ ] Code follows constitution standards

---

#### 5.3 代码审核

**Tool**: pyflow-code-reviewer

**Tool Type**: Task (subagent_type)

**前置步骤**: 注入文档上下文

**调用**:
```
Task(
    subagent_type="pyflow-code-reviewer",
    subject="审核代码",
    description=f"""审核整个代码库

## 🚨 审核标准

### 项目宪法
{constitution}

### 需求文档
{requirements}

请验证代码符合宪法要求和需求范围！
""",
    activeForm="审核代码"
)
```

**CHECKLIST**:
- [ ] Code review completed
- [ ] Issues documented (if any)
- [ ] Constitution compliance verified
- [ ] Requirements compliance verified

---

#### 5.4 Git 提交

**Tool**: Bash

**执行**:
```bash
git add .
git commit -m "feat: {{COMMIT_MESSAGE}}

echo "✅ Git 提交完成"
```

**CHECKLIST**:
- [ ] All changes committed
- [ ] Commit message follows conventions
- [ ] Working tree clean

---

### Medium/Complex 项目

**5.1-5.4**: 与 Simple 项目相同

---

## 文档结构说明

### 版本化文档结构

```
pjflow/
├── constitution.md                 # 共享宪法（所有版本）
│
├── v0_initial/                    # 新项目
│   ├── task_plan.md
│   ├── progress.md
│   ├── findings.md
│   ├── requirements.md            # v0 需求文档（新）
│   └── compliance_report.md       # v0 合规报告（新）
│
└── v1_add_feature/                # 添加功能
    ├── task_plan.md
    ├── progress.md
    ├── findings.md
    ├── requirements.md            # v1 需求文档（新）
    └── compliance_report.md       # v1 合规报告（新）
```

### 合规检查命令

```bash
# 基本用法
python .claude/skills/projectflow-executor/scripts/check_compliance.py

# 指定版本目录
python .claude/skills/projectflow-executor/scripts/check_compliance.py --version-dir v0_initial

# 指定语言
python .claude/skills/projectflow-executor/scripts/check_compliance.py --language python

# 查看帮助
python .claude/skills/projectflow-executor/scripts/check_compliance.py --help
```

---

## CHECKLIST 模板

**说明**: executor 在每个 Phase 完成后更新对应的 CHECKLIST

**更新时机**:
| Phase | 更新时机 | 更新内容 |
|-------|---------|---------|
| Phase 0 | brainstorming 完成后 | 需求分析相关 checkbox + 需求文档已创建 |
| Phase 1 | constitution 创建后 | 项目规则相关 checkbox |
| Phase 2.0 干扰检测后 | 项目准备相关 checkbox |
| Phase 2.1 (Git) 完成后 | Git 仓库相关 checkbox |
| Phase 2.2 (架构) 完成后 | 项目架构相关 checkbox |
| Phase 2.3 (系统文件) 完成后 | pyproject.toml 等系统文件 checkbox |
| Phase 2.4 (项目文件) 完成后 | 占位文件创建 checkbox |
| Phase 2.5 (虚拟环境) 完成后 | 虚拟环境和依赖安装 checkbox |
| Phase 3.1 完成后 | Git 分支 + 需求文档已创建 |
| Phase 3.2 完成后 | 依赖管理 checkbox |
| Phase 3.3 完成后 | 系统文件更新 checkbox |
| Phase 3.4 完成后 | 新功能文件创建 checkbox |
| Phase 4 (Simple) 完成后 | TDD 执行 + 合规检查 checkbox |
| Phase 4.1 (Medium) 完成后 | 测试套件生成 + 合规检查 |
| Phase 4.2 (Medium) 完成后 | 基础实现 + 合规检查 |
| Phase 4.3 (Medium) 完成后 | 代码重构 + 合规检查 |
| Phase 4 (Complex) 各子阶段 | 完成后 | 对应子阶段 + 合规检查 |
| Phase 5.1 完成后 | 自动化合规检查 checkbox |
| Phase 5.2 完成后 | 质量检查 checkbox |
| Phase 5.3 完成后 | 代码审核 checkbox |
| Phase 5.4 完成后 | Git 提交 checkbox |

**使用示例**:

```python
Edit(
    file_path="CHECKLIST.md",
    old_string="- [ ] Phase 0: brainstorming 完成",
    new_string="- [x] Phase 0: brainstorming 完成"
)
```

---

## 复杂度差异化说明

### Simple 项目特征

**预期 LOC**: < 300 行

**特点**:
- 单一功能，明确需求
- 最小架构（2-3 层）
- 单次 TDD 循环
- 基础质量审核
- 快速迭代

**Phase 4 执行**: 单次 `pyflow-tdd-cycle --single-cycle`

### Medium 项目特征

**预期 LOC**: 300-1000 行

**特点**:
- 多个相关功能
- 标准架构（3-5 层）
- 完整 TDD 三阶段
- 代码审核
- 性能考虑

**Phase 4 执行**: RED → GREEN → REFACTOR

### Complex 项目特征

**预期 LOC**: > 1000 行

**特点**:
- 平台级或框架级
- 深层架构（5+ 层）
- 扩展 TDD 循环（异步、性能）
- 深度审核
- 安全审核
- 完整 CI/CD

**Phase 4 执行**: RED → GREEN → 异步优化 → 性能优化 → 深度优化 → 最终清理

---

## 工具调用格式与示例

### Tool 类型与调用方式

| Tool 类型 | 调用方式 | 说明 |
|-----------|----------|------|
| **Skill** | `Skill(skill="name", args="...")` | 调用其他 skill |
| **Task** | `Task(subagent_type="...", ...)` | 调用 agent |
| **Bash** | `Bash(command="...")` | 执行命令 |
| **Write** | `Write(file_path="...", content="...")` | 写入文件 |
| **Edit** | `Edit(file_path="...", old_string="...", new_string="...")` | 编辑文件 |

### 文档注入示例

```python
# 标准文档注入模式
constitution_content = Read("./pjflow/constitution.md")
requirements_content = Read("./pjflow/{{VERSION_DIR}}/requirements.md")

enhanced_description = f"""{original_description}

## 🚨 强制约束（必须遵守）

### 项目宪法 (Constitution)
{constitution_content}

### 需求文档 (Requirements)
{requirements_content}

**重要**: 违反上述约束的代码将被拒绝！
"""
```

---

**版本**: 5.0.0
**用途**: ProjectFlow Planner - Python 完整计划模板
**适用语言**: Python (pyproject.toml)
**更新内容**:
- 🆕 集成自动化合规检查
- 🆕 版本化需求文档支持
- 🆕 文档注入到所有 Phase 4 Tool 调用
- 🆕 合规报告生成步骤
- 🆕 CHECKLIST 新增合规检查项

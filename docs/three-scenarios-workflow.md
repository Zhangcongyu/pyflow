# ProjectFlow 三种场景流程详解

**版本**: 2.0.0
**更新时间**: 2026-02-20
**用途**: 详细说明三种典型场景的完整执行流程，用于验证和测试

---

## 目录

- [场景 1: 简单新建项目](#场景-1-简单新建项目)
- [场景 2: 中等新建项目](#场景-2-中等新建项目)
- [场景 3: 中等项目新增功能](#场景-3-中等项目新增功能)
- [工具调用对照表](#工具调用对照表)
- [需求文档生成方式对比](#需求文档生成方式对比)

---

## 场景 1: 简单新建项目

**参数**: `--new --simple --python`
**版本目录**: `pjflow/v0_initial/`
**预期代码量**: < 300 行

### Phase 执行概览

| Phase | 状态 | 详细说明 |
|-------|:----:|---------|
| Phase 0: 需求互动 | ❌ 跳过 | Simple 项目不需要需求探索 |
| Phase 1: 项目规则 | ✅ 执行 | 创建项目宪法文档 |
| Step 5.5: 需求文档生成 | ✅ 执行 | Phase 1 完成后，直接生成需求模板 |
| Phase 2: 项目构建 | ✅ 执行 | 创建项目脚手架 |
| Phase 3: 工作树准备 | ❌ 跳过 | 新项目不需要 |
| Phase 4: TDD 执行 | ✅ 执行 | 单次 TDD 循环 |
| Phase 5: 质量审核 | ✅ 执行 | 基础质量审核和 Git 提交 |

### 详细流程

#### Phase 0: 需求互动
**状态**: ❌ 跳过

**说明**: Simple 项目需求明确，不需要头脑风暴探索。

---

#### Phase 1: 项目规则
**状态**: ✅ 执行

**说明**: 创建项目宪法文档，定义项目规则和标准。

**工具调用**:
```
Skill(skill="pyflow-constitution", args="创建项目宪法")
```

**输出**: `pjflow/constitution.md`（共享，所有版本使用同一个）

**CHECKLIST**:
- [ ] Constitution 创建/更新
- [ ] 项目规则定义

---

#### Step 5.5: 需求文档生成
**状态**: ✅ 执行（Phase 1 完成后）

**说明**: Simple 项目不需要 Phase 0 brainstorming，直接生成需求文档模板。

**参考**: `python-complete-template.md` 中的 Step 5.5 定义

**工具调用**:
```
Write(
    file_path="pjflow/v0_initial/requirements.md",
    content="""# Requirements

**Project Type**: new
**Complexity**: simple
**Goal**: 创建一个简单的 Python CLI 工具

---

## Project Overview

创建一个简单的 Python CLI 工具

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
*Created: new - simple*
"""
)
```

**输出**: `pjflow/v0_initial/requirements.md`

**CHECKLIST**:
- [ ] 需求文档已创建
- [ ] 输出路径正确

---

#### Phase 2: 项目构建
**状态**: ✅ 执行

**说明**: 创建项目脚手架，包括 Git 仓库、项目架构、配置文件等。

##### 2.0 干扰检测与清理

**工具调用**:
```bash
# 检测冲突
Bash(command="""
CONFLICT_DIRS="src tests .venv venv __pycache__"
CONFLICT_FILES="pyproject.toml setup.py requirements.txt package.json"
...
""")

# 询问用户
AskUserQuestion(questions=[{
    "question": "检测到目录中已存在项目文件，是否删除并重新创建？",
    "options": [
        {"label": "是，删除并重新创建"},
        {"label": "否，取消操作"}
    ]
}])
```

**CHECKLIST**:
- [ ] 冲突检测完成
- [ ] 用户确认
- [ ] 目录已清理（如需要）

##### 2.1 Git 仓库

**工具调用**:
```bash
Bash(command="""
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    git init
    git branch -M main
fi
""")

Write(file_path=".gitignore", content="...")
```

**CHECKLIST**:
- [ ] Git 仓库初始化
- [ ] .gitignore 创建

##### 2.2 项目架构

**工具调用**:
```
Write(file_path="src/project_name/__init__.py", content="...")
Write(file_path="src/project_name/cli.py", content="...")
```

**架构类型**: CLI / Library

**CHECKLIST**:
- [ ] 目录结构创建
- [ ] 架构类型确认

##### 2.3 pyproject.toml

**工具调用**:
```
Write(file_path="pyproject.toml", content="[project]
name = \"project-name\"
version = \"0.1.0\"
...")
```

**CHECKLIST**:
- [ ] pyproject.toml 创建
- [ ] 依赖配置完成

##### 2.4 项目占位文件

**工具调用**:
```
Write(file_path="src/project_name/commands/__init__.py", content="...")
```

**原则**: 创建空占位文件，**严禁编写业务逻辑**

**CHECKLIST**:
- [ ] 所有目录已创建
- [ ] 占位文件已生成
- [ ] 无业务逻辑代码

##### 2.5 虚拟环境

**工具调用**:
```
Skill(skill="pyflow-uv-package-manager", args="创建虚拟环境")
```

**执行**: `uv venv && uv pip install -e .`

**CHECKLIST**:
- [ ] 虚拟环境创建
- [ ] 依赖已安装

---

#### Phase 3: 工作树准备
**状态**: ❌ 跳过

**说明**: 新项目不需要。

---

#### Phase 4: TDD 执行
**状态**: ✅ 执行

**说明**: 单次 TDD 循环（RED → GREEN → REFACTOR）

**前置步骤**: 注入文档上下文
```python
constitution = Read("./pjflow/constitution.md")
requirements = Read("./pjflow/v0_initial/requirements.md")
```

##### Simple 项目 TDD

**工具调用**:
```
Skill(skill="pyflow-tdd-cycle", args="--single-cycle")
```

**执行流程**:
1. **RED Phase**: 编写测试
2. **GREEN Phase**: 最小实现通过测试
3. **REFACTOR Phase**: 代码重构

**后置步骤**: 合规检查
```bash
python .claude/skills/projectflow-executor/scripts/check_compliance.py \
    --language python \
    --version-dir v0_initial \
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

---

#### Phase 5: 质量审核
**状态**: ✅ 执行

**说明**: 基础质量审核和 Git 提交

##### 5.1 代码风格检查

**工具调用**:
```bash
Bash(command="ruff format .")
Bash(command="ruff check --fix .")
```

**CHECKLIST**:
- [ ] Code formatted
- [ ] No lint errors

##### 5.2 测试验证

**工具调用**:
```bash
Bash(command="pytest -v")
```

**CHECKLIST**:
- [ ] All tests pass

##### 5.3 Git 提交

**工具调用**:
```bash
Bash(command="git add . && git commit -m \"feat: 初始化项目\"")
```

**CHECKLIST**:
- [ ] All changes committed
- [ ] Working tree clean

---

### 版本目录结构

```
pjflow/
├── constitution.md                 # 共享宪法
└── v0_initial/
    ├── task_plan.md
    ├── progress.md
    ├── findings.md
    ├── requirements.md            # Step 5.5 生成
    └── compliance_report.md       # Phase 4 后生成
```

---

## 场景 2: 中等新建项目

**参数**: `--new --medium --python`
**版本目录**: `pjflow/v0_initial/`
**预期代码量**: 300-1000 行

### Phase 执行概览

| Phase | 状态 | 详细说明 |
|-------|:----:|---------|
| Phase 0: 需求互动 | ✅ 执行 | 头脑风暴探索需求 |
| Phase 1: 项目规则 | ✅ 执行 | 创建项目宪法文档 |
| Phase 2: 项目构建 | ✅ 执行 | 创建项目脚手架 |
| Phase 3: 工作树准备 | ❌ 跳过 | 新项目不需要 |
| Phase 4: TDD 执行 | ✅ 执行 | 完整 TDD 三阶段 |
| Phase 5: 质量审核 | ✅ 执行 | 代码审核和质量保证 |

### 详细流程

#### Phase 0: 需求互动
**状态**: ✅ 执行

**说明**: **头脑风暴探索需求**

**流程**:
1. **理解项目上下文**: 检查文件、文档、最近提交
2. **逐一问题澄清**: 每次只问一个问题
3. **提出 2-3 种方案**: 展示权衡和推荐
4. **分段展示设计**: 每次 200-300 字
5. **增量验证确认**: 每段确认后再继续

**工具调用**:
```
Skill(
    skill="pyflow-brainstorming",
    args="--version-dir v0_initial 创建一个中等的 FastAPI 用户认证系统"
)
```

**输出**: `pjflow/v0_initial/requirements.md`（由 brainstorming 交互生成）

**CHECKLIST**:
- [ ] 需求分析完成
- [ ] 功能边界明确
- [ ] 技术方案确认
- [ ] 需求文档已创建

---

#### Phase 1: 项目规则
**状态**: ✅ 执行

**说明**: 创建项目宪法文档

**工具调用**:
```
Skill(skill="pyflow-constitution", args="创建项目宪法")
```

**输出**: `pjflow/constitution.md`

**CHECKLIST**:
- [ ] Constitution 创建/更新
- [ ] 项目规则定义

---

#### Phase 2: 项目构建
**状态**: ✅ 执行

**说明**: 与简单项目相同，参见场景 1 Phase 2

**子阶段**:
- 2.0: 干扰检测与清理
- 2.1: Git 仓库初始化
- 2.2: 项目架构创建（FastAPI 多层架构）
- 2.3: pyproject.toml 生成
- 2.4: 项目占位文件
- 2.5: 虚拟环境配置

**工具调用**: 参见场景 1 Phase 2

---

#### Phase 3: 工作树准备
**状态**: ❌ 跳过

**说明**: 新项目不需要

---

#### Phase 4: TDD 执行
**状态**: ✅ 执行

**说明**: **完整 TDD 三阶段**

**前置步骤**: 注入文档上下文
```python
constitution = Read("./pjflow/constitution.md")
requirements = Read("./pjflow/v0_initial/requirements.md")
```

##### Medium 项目 TDD

###### Phase 4.1: RED - 生成测试

**工具调用**:
```
Task(
    subagent_type="test-automator",
    subject="生成测试套件",
    description=f"""为 创建一个中等的 FastAPI 用户认证系统 生成完整测试套件

## 🚨 强制约束

### 项目宪法
{constitution}

### 需求文档
{requirements}

**重要**: 测试必须覆盖所有需求功能！"""
)
```

**CHECKLIST**:
- [ ] 测试套件生成
- [ ] 测试覆盖率规划

###### Phase 4.2: GREEN - 实现功能

**工具调用**:
```
Task(
    subagent_type="python-pro",
    subject="实现功能",
    description=f"""实现所有测试

## 🚨 强制约束

### 项目宪法
{constitution}

### 需求文档
{requirements}

**重要**: 使用最小实现使测试通过！"""
)
```

**CHECKLIST**:
- [ ] 所有测试通过
- [ ] 最小实现原则

###### Phase 4.3: REFACTOR - 代码重构

**工具调用**:
```
Skill(
    skill="pyflow-python-performance-optimization",
    args="优化代码结构和性能"
)
```

**后置步骤**: 合规检查
```bash
python .claude/skills/projectflow-executor/scripts/check_compliance.py \
    --language python \
    --version-dir v0_initial \
    --phase tdd-medium
```

**CHECKLIST**:
- [ ] 代码结构优化
- [ ] 所有测试仍通过
- [ ] 合规检查已执行

---

#### Phase 5: 质量审核
**状态**: ✅ 执行

**说明**: 代码审核和质量保证

##### 5.1 代码风格检查

**工具调用**:
```bash
Bash(command="ruff format . && ruff check --fix .")
```

**CHECKLIST**:
- [ ] Code formatted
- [ ] No lint errors

##### 5.2 测试验证

**工具调用**:
```bash
Bash(command="pytest -v --cov")
Bash(command="mypy src/")
```

**CHECKLIST**:
- [ ] All tests pass
- [ ] Type checks pass

##### 5.3 代码审核

**工具调用**:
```
Task(
    subagent_type="code-reviewer",
    subject="审核代码",
    description=f"""审核整个代码库

## 🚨 审核标准

### 项目宪法
{constitution}

### 需求文档
{requirements}

请验证代码符合宪法要求和需求范围！"""
)
```

**CHECKLIST**:
- [ ] Code review completed
- [ ] Constitution compliance verified

##### 5.4 Git 提交

**工具调用**:
```bash
Bash(command="git add . && git commit -m \"feat: 实现 FastAPI 用户认证系统\"")
```

**CHECKLIST**:
- [ ] All changes committed
- [ ] Working tree clean

---

### 版本目录结构

```
pjflow/
├── constitution.md                 # 共享宪法
└── v0_initial/
    ├── task_plan.md
    ├── progress.md
    ├── findings.md
    ├── requirements.md            # Phase 0 brainstorming 生成
    └── compliance_report.md       # Phase 4 后生成
```

---

## 场景 3: 中等项目新增功能

**参数**: `--add-feature --medium --python`
**版本目录**: `pjflow/v1_auth_api/`

### Phase 执行概览

| Phase | 状态 | 详细说明 |
|-------|:----:|---------|
| Phase 0: 需求互动 | ✅ 执行 | 头脑风暴探索需求 |
| Phase 1: 项目规则 | ❌ 跳过 | 老项目已有宪法 |
| Phase 2: 项目构建 | ❌ 跳过 | 老项目已存在 |
| Phase 3: 工作树准备 | ✅ 执行 | Git 分支、依赖管理、文件更新 |
| Phase 4: TDD 执行 | ✅ 执行 | 完整 TDD 三阶段 |
| Phase 5: 质量审核 | ✅ 执行 | 质量审核和 PR 合并 |

### 详细流程

#### Phase 0: 需求互动
**状态**: ✅ 执行

**说明**: **头脑风暴探索需求**

**流程**:
1. **理解现有项目**: 检查文件、文档、最近提交
2. **探索新功能需求**: 逐一问题澄清
3. **提出 2-3 种方案**: 展示权衡和推荐
4. **分段展示设计**: 每次 200-300 字
5. **增量验证确认**: 每段确认后再继续

**工具调用**:
```
Skill(
    skill="pyflow-brainstorming",
    args="--version-dir v1_auth_api 为这个项目添加一个用户认证 API"
)
```

**输出**: `pjflow/v1_auth_api/requirements.md`

**CHECKLIST**:
- [ ] 需求分析完成
- [ ] 功能边界明确
- [ ] 技术方案确认
- [ ] 需求文档已创建

---

#### Phase 1: 项目规则
**状态**: ❌ 跳过

**说明**: 老项目已有宪法，不需要创建

---

#### Phase 2: 项目构建
**状态**: ❌ 跳过

**说明**: 老项目已存在，不需要构建

---

#### Phase 3: 工作树准备
**状态**: ✅ 执行

**说明**: 为新功能准备工作环境

##### 3.1 Git 分支管理

**工具调用**:
```bash
Bash(command="""
CURRENT_BRANCH=$(git branch --show-current)
FEATURE_NAME="v1_auth_api"
git checkout -b feature/$FEATURE_NAME
""")
```

**CHECKLIST**:
- [ ] 当前分支确认
- [ ] Feature 分支创建成功
- [ ] 分支命名符合规范

##### 3.2 依赖管理

**工具调用**:
```
Skill(
    skill="pyflow-uv-package-manager",
    args="添加新功能依赖"
)
```

**执行**: `uv add fastapi uvicorn pydantic sqlalchemy`

**CHECKLIST**:
- [ ] 依赖已添加
- [ ] 无依赖冲突

##### 3.3 系统文件更新

**工具调用**:
```
Edit(file_path="README.md", old_string="...", new_string="...")
```

**执行**: 更新 README.md 添加新功能说明

**CHECKLIST**:
- [ ] README.md 已更新
- [ ] 版本号已更新（如需要）

##### 3.4 新功能文件创建

**工具调用**:
```
Write(
    file_path="src/project_name/auth/__init__.py",
    content="# -*- coding: utf-8 -*-\n\"\"\"\"...\"\"\"\n__all__ = []"
)
```

**原则**: 创建空文件，不编写业务逻辑

**CHECKLIST**:
- [ ] 新功能目录创建
- [ ] 占位文件已生成
- [ ] 无业务逻辑代码

---

#### Phase 4: TDD 执行
**状态**: ✅ 执行

**说明**: **完整 TDD 三阶段**

**前置步骤**: 注入文档上下文
```python
constitution = Read("./pjflow/constitution.md")
requirements = Read("./pjflow/v1_auth_api/requirements.md")
```

**执行流程**: 与场景 2 Phase 4 相同

- 4.1 RED: `Task("test-automator")`
- 4.2 GREEN: `Task("python-pro")`
- 4.3 REFACTOR: `Skill("pyflow-python-performance-optimization")`
- 合规检查: `Bash(check_compliance.py)`

---

#### Phase 5: 质量审核
**状态**: ✅ 执行

**说明**: 质量审核和 PR 合并

##### 5.1 代码风格检查

**工具调用**:
```bash
Bash(command="ruff format . && ruff check --fix .")
```

**CHECKLIST**:
- [ ] Code formatted
- [ ] No lint errors

##### 5.2 测试验证

**工具调用**:
```bash
Bash(command="pytest -v --cov")
Bash(command="mypy src/")
```

**CHECKLIST**:
- [ ] All tests pass
- [ ] Type checks pass

##### 5.3 代码审核

**工具调用**:
```
Task(
    subagent_type="code-reviewer",
    subject="审核代码",
    description=f"""审核新功能代码

## 🚨 审核标准

### 项目宪法
{constitution}

### 需求文档
{requirements}"""
)
```

**CHECKLIST**:
- [ ] Code review completed
- [ ] Issues documented (if any)

##### 5.4 PR 合并

**工具调用**:
```bash
Bash(command="""
git push -u origin feature/v1_auth_api
gh pr create --title "feat: 添加用户认证 API"
""")
```

**CHECKLIST**:
- [ ] Feature 分支已推送
- [ ] PR 已创建
- [ ] 等待合并

---

### 版本目录结构

```
pjflow/
├── constitution.md                 # 共享宪法（已存在）
│
├── v0_initial/                    # 之前的版本
│   ├── task_plan.md
│   ├── progress.md
│   └── requirements.md
│
└── v1_auth_api/                   # 新功能版本
    ├── task_plan.md
    ├── progress.md
    ├── findings.md
    ├── requirements.md            # Phase 0 brainstorming 生成
    └── compliance_report.md       # Phase 4 后生成
```

---

## 工具调用对照表

| 工具类型 | 调用方式 | 用途 | 示例 |
|---------|---------|------|------|
| **Skill** | `Skill(skill="name", args="...")` | 调用其他 skill | `Skill("pyflow-constitution")`<br>`Skill("pyflow-brainstorming")`<br>`Skill("pyflow-tdd-cycle")` |
| **Task** | `Task(subagent_type="...", ...)` | 调用 agent | `Task("test-automator")`<br>`Task("python-pro")`<br>`Task("code-reviewer")` |
| **Bash** | `Bash(command="...")` | 执行命令 | `Bash("git init")`<br>`Bash("pytest -v")`<br>`Bash("ruff format .")` |
| **Write** | `Write(file_path="...", content="...")` | 写入文件 | `Write(".gitignore", content="...")`<br>`Write("pyproject.toml", content="...")` |
| **Edit** | `Edit(file_path="...", old_string="...", new_string="...")` | 编辑文件 | `Edit("README.md", old_string="...", new_string="...")` |
| **Read** | `Read(file_path="...")` | 读取文件 | `Read("pjflow/constitution.md")`<br>`Read("pjflow/v0_initial/requirements.md")` |
| **AskUserQuestion** | `AskUserQuestion(questions=[...])` | 询问用户 | 干扰检测确认 |

---

## 需求文档生成方式对比

| 场景 | 生成时机 | 生成方式 | 工具调用 | 输出位置 | 模板来源 |
|------|---------|---------|---------|---------|---------|
| **简单新建** | Phase 1 后 | 直接生成模板 | `Write` | `pjflow/v0_initial/requirements.md` | 语言模板 Step 5.5 |
| **中等新建** | Phase 0 | brainstorming 交互 | `Skill("pyflow-brainstorming", args="--version-dir v0_initial ...")` | `pjflow/v0_initial/requirements.md` | brainstorming 生成 |
| **中等新增** | Phase 0 | brainstorming 交互 | `Skill("pyflow-brainstorming", args="--version-dir v1_auth_api ...")` | `pjflow/v1_auth_api/requirements.md` | brainstorming 生成 |

**模板定义位置**:
- Simple 项目模板: 各语言模板的 `Step 5.5` 章节
- Medium/Complex 项目: 通过 `pyflow-brainstorming` skill 交互生成

---

## Phase 执行规则总结

| Phase | simple (new) | medium/complex (new) | simple (add-feature) | medium/complex (add-feature) |
|-------|-------------|---------------------|---------------------|----------------------------|
| **Phase 0: 需求互动** | ❌ | ✅ brainstorming | ❌ | ✅ brainstorming |
| **Phase 1: 项目规则** | ✅ | ✅ | ❌ | ❌ |
| **Step 5.5: 需求文档** | ✅ Write | ❌ | ✅ Write | ❌ |
| **Phase 2: 项目构建** | ✅ | ✅ | ❌ | ❌ |
| **Phase 3: 工作树准备** | ❌ | ❌ | ✅ | ✅ |
| **Phase 4: TDD 执行** | ✅ 单次循环 | ✅ 三阶段 | ✅ 单次循环 | ✅ 三阶段 |
| **Phase 5: 质量审核** | ✅ 基础审核 | ✅ 代码审核 | ✅ 基础审核 | ✅ PR 审核 |

---

## 核心原则

1. **需求文档版本化**: 每个版本目录都有独立的需求文档
2. **宪法共享**: 所有版本共享同一个 constitution.md
3. **简单项目快速启动**: 跳过 Phase 0，直接生成需求模板
4. **复杂项目深度探索**: Phase 0 brainstorming 交互探索需求
5. **TDD 强制执行**: 所有业务逻辑必须通过 TDD 工具完成
6. **文档注入**: Phase 4 每个子阶段前注入宪法和需求文档
7. **合规检查**: Phase 4/5 后自动执行合规检查
8. **模板单一来源**: 需求模板只在语言模板中定义

---

## 关键变更说明

### v2.0.0 更新 (2026-02-20)

1. **Step 5.5 模板来源变更**: 从调用脚本改为直接从语言模板读取
2. **需求文档生成方式**:
   - Simple 项目: 使用 `Write` 工具，模板定义在语言模板的 Step 5.5
   - Medium/Complex 项目: 使用 `pyflow-brainstorming` skill
3. **executor SKILL.md 简化**: Step 5.5 改为引用语言模板，不重复定义
4. **create_simple_requirements.py**: 保留为独立工具，不在主流程中调用

---

**文档版本**: 2.0.0
**最后更新**: 2026-02-20
**维护者**: ProjectFlow Team

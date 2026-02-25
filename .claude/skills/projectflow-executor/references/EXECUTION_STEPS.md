# 执行步骤详解

## Step 1: 读取 task_plan.md 并找到下一个 Phase

```bash
# 找到最新版本目录
latest_version_dir=$(find ./pjflow -type d -name "v*" | sort -V | tail -1)
task_plan_path="$latest_version_dir/task_plan.md"
```

遍历 task_plan.md 中的 Phase，找到第一个 `Status: pending` 的 Phase。

## Step 2: 读取合规文档

**每个 Phase 执行前必须读取**:

```bash
pjflow/constitution.md               # 项目宪法（共享）
pjflow/{VERSION_DIR}/requirements.md # 版本化需求文档
pjflow/{VERSION_DIR}/task_plan.md    # 当前执行计划
```

## Step 3: 智能加载执行上下文

> 🧠 **充分利用 LLM 理解能力，动态提取需求信息**

### Phase 分类执行策略

| Phase 类型 | 信息来源 | 执行方式 |
|------------|---------|---------|
| **Phase 0, 1** | - | 直接执行（文档还不存在） |
| **Phase 2.0, 2.1, 2.5** | 🔧 模板（通用脚本） | 直接执行 |
| **Phase 2.2, 2.3, 2.4** | 📋 需求 + 🔧 模板 | LLM 理解并合并 |
| **Phase 3.1-3.4** | 📋 需求 | LLM 理解 |
| **Phase 4** | 📋 需求 + 📜 宪法 | 注入到 TDD 工具 |
| **Phase 5** | - | 运行合规检查 |

### 各子阶段详细策略

#### Phase 2.0, 2.1, 2.5: 通用脚手架

**使用 LLM 内置知识，不需要读取需求文档**

```bash
# 2.0: 干扰检测
Bash("检测并清理冲突目录")

# 2.1: Git 初始化
Bash("git init && git branch -M main")
Write(".gitignore", "# 标准 Python .gitignore 内容")

# 2.5: 虚拟环境
Bash("uv venv && source .venv/bin/activate && uv sync")
```

#### Phase 2.2: 项目架构

**LLM 理解需求文档，提取目录结构**

```python
# 读取需求文档
requirements = Read(f"pjflow/{version_dir}/requirements.md")

# LLM 理解并提取目录结构（无论在哪个章节）
"""
示例 rarcrack 项目：
需求文档第 2.1 节描述了目录结构：
- src/rarcrack/core/（cracker.py, dictionary.py, progress.py）
- src/rarcrack/utils/（rar_handler.py, config.py）
- tests/
"""

# 创建目录
Bash("mkdir -p src/rarcrack/core src/rarcrack/utils tests")
```

#### Phase 2.3: 系统文件

**LLM 合并需求文档和模板配置**

```python
# 1. 从需求文档提取依赖
requirements = Read(f"pjflow/{version_dir}/requirements.md")
"""
需求文档第 6 节：
dependencies = ["typer>=0.9.0", "rarfile>=4.0", "rich>=13.0.0"]
"""

# 2. 从模板提取工具配置
template = Read(".claude/skills/projectflow-planner/assets/templates/python-complete-template.md")
"""
模板提供：
- 中文镜像源配置
- pytest、ruff、mypy 标准配置
"""

# 3. LLM 合并生成 pyproject.toml
pyproject_content = f"""
[project]
name = "{project_name}"
dependencies = {从需求提取}

[[tool.uv.index]]
url = "https://mirrors.aliyun.com/pypi/simple"  # 从模板

[tool.pytest.ini_options]
testpaths = ["tests"]  # 从模板
"""
```

#### Phase 2.4: 项目文件

**LLM 理解需求文档，创建占位文件**

```python
# 从需求文档提取模块列表
"""
需求文档指定需要创建：
- cli.py（命令行界面）
- core/cracker.py（破解核心逻辑）
- core/dictionary.py（字典处理）
...
"""

# 使用模板的空文件格式创建
for module in modules:
    Write(f"src/{module}.py", "# -*- coding: utf-8 -*-\n\"\"\"{描述}\"\"\"\n__all__ = []")
```

**原则**：严禁编写业务逻辑

#### Phase 3: 工作树准备

**LLM 理解新版本需求文档**

```python
# 读取新版本的 requirements.md
new_requirements = Read(f"pjflow/{version_dir}/requirements.md")

# 理解需要添加哪些新功能、新依赖、新文件
# 创建分支、添加依赖、创建占位文件
```

#### Phase 4: TDD 执行

**不是自己执行，而是注入文档到 TDD 工具**

```python
# 读取文档
constitution = Read("pjflow/constitution.md")
requirements = Read(f"pjflow/{version_dir}/requirements.md")

# 注入到 TDD 工具
Skill(skill="pyflow-tdd-cycle", args=f"""
{GOAL}

## 🚨 强制约束
### 项目宪法
{constitution}

### 需求文档
{requirements}
""")
```

**关键**：Executor 不编写业务代码，只约束 TDD 工具的输出。

#### Step 4.5: 后置验证 (Post-TDD) - 仅 Phase 4/5

在 Phase 4 或 Phase 5 完成后，**必须**运行后置验证：

```bash
python .claude/skills/projectflow-executor/scripts/check_compliance.py \
    --language auto \
    --version-dir {VERSION_DIR} \
    --mode post-tdd
```

**验证内容**:
- 代码风格符合宪法
- 类型注解符合宪法
- 错误处理符合宪法
- 测试覆盖率达标
- 代码是否反映文档约束

---

## Step 3.5: 判断脚手架 vs 业务逻辑

> ⚠️ **这个判断至关重要！** 错误判断会破坏整个 TDD 流程。

### 判断树

```
当前 Phase 需要创建文件/代码
│
├─ 是否所有项目都需要这个文件？
│  ├─ 是 → 脚手架 → Write/Bash 工具 ✅
│  └─ 否 → 继续判断
│
└─ 是否包含本项目特定功能？
   ├─ 是 → 业务逻辑 → TDD 工具 ❌
   └─ 否 → 询问用户
```

### 示例

| Phase | 类型 | 工具 | 理由 |
|-------|------|------|------|
| 创建 src/ 目录 | 脚手架 | Bash ✅ | 所有项目都需要 |
| 创建 pyproject.toml | 脚手架 | Write ✅ | 所有项目都需要 |
| 实现用户登录功能 | 业务逻辑 | TDD ❌ | 项目特定功能 |
| 编写测试用例 | 业务逻辑 | TDD ❌ | 包含项目特定验证逻辑 |

## Step 4: 调用 Tool

> ⚠️ **Phase 4/5 特殊规则**: 必须注入宪法和需求！

### Phase 4/5 三步骤执行流程

#### Step 4.0: 前置检查 (Pre-TDD) - 仅 Phase 4/5

在开始 Phase 4 或 Phase 5 之前，**必须**运行前置检查：

```bash
python .claude/skills/projectflow-executor/scripts/check_compliance.py \
    --language auto \
    --version-dir {VERSION_DIR} \
    --mode pre-tdd
```

**检查内容**:
- 宪法文档是否存在
- 需求文档是否存在
- 文档内容是否完整

**阻断条件**: 如有 CRITICAL 级别问题，必须修复后才能继续。

### Phase 4/5 文档注入（强制执行）

当当前 Phase 为 4 或 5 时，**必须**执行以下注入步骤：

#### Step 4.1: 读取文档

```python
# 读取项目宪法
constitution_content = Read("pjflow/constitution.md")

# 读取版本化需求文档
requirements_content = Read(f"pjflow/{VERSION_DIR}/requirements.md")
```

#### Step 4.2: 构建增强提示

```python
enhanced_context = f"""
## 🚨 强制约束（必须遵守）

### 项目宪法 (Constitution)
{constitution_content}

### 需求文档 (Requirements)
{requirements_content}

**重要**: 违反上述约束的代码/测试将被拒绝！必须确保：
1. 所有代码符合宪法规则（类型注解、代码风格、测试覆盖率等）
2. 所有功能在需求范围内（无功能蔓延）
3. 所有需求都有对应测试覆盖
"""
```

#### Step 4.3: 注入到 Tool 调用

**Skill 调用示例** (Simple 项目 Phase 4):
```python
Skill(
    skill="pyflow-tdd-cycle",
    args=f"""{GOAL} --single-cycle

{enhanced_context}
"""
)
```

**Task 调用示例** (Medium 项目 Phase 4.1):
```python
Task(
    subagent_type="test-automator",
    subject="生成测试套件",
    description=f"""为 {GOAL} 生成完整测试套件

{enhanced_context}
""",
    activeForm="生成测试套件"
)
```

**Task 调用示例** (Medium 项目 Phase 4.2):
```python
Task(
    subagent_type="pyflow-python-pro",
    subject="实现功能使测试通过",
    description=f"""实现所有功能使测试通过

{enhanced_context}
""",
    activeForm="实现功能"
)
```

### 非 Phase 4/5 调用

对于其他 Phase，按照常规方式调用 Tool：

### Tool 类型

| Tool 类型 | 调用方式 | 用途 |
|-----------|----------|------|
| Skill | `Skill(skill="name", args="...")` | 调用其他 skill |
| Task | `Task(subagent_type="...", ...)` | 调用 agent |
| Bash | `Bash(command="...")` | 执行命令 |
| Write | `Write(file_path="...", content="...")` | 写入文件 |
| Edit | `Edit(file_path="...", old_string="...", new_string="...")` | 编辑文件 |

### 等待规则

```bash
# ✅ 正确
Skill(skill="pyflow-tdd-cycle", args="...")
# 等待返回结果...
# 验证输出
# 更新状态

# ❌ 错误
Skill(skill="pyflow-tdd-cycle", args="...")
Write(file_path="src/user.py", content="...")  # 不要这样做！
```

**在 tool 返回前**:
- ❌ 不要创建文件
- ❌ 不要编辑代码
- ❌ 不要运行命令
- ✅ 等待 tool 完成并返回结果

## Step 5: 验证结果

### 验证清单

- Tool 执行无错误
- 输出符合 `pjflow/constitution.md` 要求
- 输出符合 `pjflow/{VERSION_DIR}/requirements.md` 要求
- 文件/目录创建正确

## Step 6: 更新状态和记录

### 6.1 更新 Phase 状态

使用 **Edit 工具**将 Status 从 `pending/in_progress` 改为 `complete`

### 6.2 更新 CHECKLIST.md

```python
Edit(
    file_path="pjflow/{VERSION_DIR}/CHECKLIST.md",
    old_string="- [ ] Phase X 完成",
    new_string="- [x] Phase X 完成"
)
```

### 6.3 更新 progress.md

记录执行结果和任何发现。

```markdown
## Phase X: [Phase 名称]

**执行时间**: 2026-02-24
**状态**: ✅ 完成
**输出**: [简要描述]
**发现**: [任何值得记录的内容]
```

## Step 7: 继续下一 Phase 或完成

回到 Step 1，继续执行下一个 Phase，直到所有 Phase 完成。

## Step 5.5: 简单项目需求文档生成（特殊步骤）

**触发条件**: Phase 0 执行时，且 `{{COMPLEXITY}}` == simple

**说明**: 对于简单项目，不需要调用 brainstorming skill，直接生成需求文档模板。

**参考模板**:
- Python: `.claude/skills/projectflow-planner/assets/templates/python-complete-template.md` (Phase 0.1)
- TypeScript: `.claude/skills/projectflow-planner/assets/templates/typescript-complete-template.md` (Phase 0.1)
- Go: `.claude/skills/projectflow-planner/assets/templates/go-template.md` (Phase 0.1)

**执行方式**: 使用 Write 工具，按模板写入需求文档

**输出位置**: `pjflow/{VERSION_DIR}/requirements.md`

**Skip if**: 复杂度为 medium 或 complex

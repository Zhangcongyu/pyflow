# ProjectFlow 运行调度流程

## 概述

ProjectFlow 由三个核心 skill 组成，形成完整的项目开发编排流水线：

```
projectflow-router → projectflow-planner → projectflow-executor
```

---

## 1. projectflow-router（三维检测器）

### 职责
纯检测器，只负责参数传递和路由，不执行任何实现工作。

### 检测三维属性

| 维度 | 参数 | 说明 |
|-------|------|------|
| **项目状态** | `--new` / `--add-feature` | 新项目 vs 老项目新增功能 |
| **项目复杂度** | `--simple` / `--medium` / `--complex` | 简单 / 中等 / 复杂 |
| **语言类型** | `--python` / `--typescript` / `--go` | Python / TypeScript / Go |

### 检测规则

#### 维度 1: 项目类型（新 vs 老）

**新项目信号**: "创建"、"新建"、"build from scratch"、目录为空、无项目配置文件

**老项目信号**: "添加"、"新增"、"extend"、"add feature"、存在项目配置文件

#### 维度 2: 项目复杂度

| 复杂度 | 触发关键词 |
|---------|-------------|
| **简单** | "简单"、"小的"、"quick"、"单个功能"、"工具"、"utility" |
| **中等** | "中等"、"几个功能"、"API"、"CRUD"、"数据处理"、"service" |
| **复杂** | "复杂"、"大型的"、"完整系统"、"平台"、"框架"、"高性能"、"分布式" |

#### 维度 3: 语言类型

| 触发关键词 | 参数 | 配置文件 |
|-----------|------|----------|
| Python, FastAPI, Django | `--python` | `pyproject.toml` |
| TypeScript, React, Node.js | `--typescript` | `package.json` |
| Go, Golang, Gin | `--go` | `go.mod` |

**默认**: 未明确指定时使用 `--python`

### 调用方式

```
Skill(skill="projectflow-planner", args="--new --simple --python 用户原始需求")
```

---

## 2. projectflow-planner（计划生成器）

### 职责
检测环境 → 读取模板 → 生成具体可执行的 plan.md → 调用 executor

### 核心流程

```
三维参数输入
   ↓
Step 1: 检测项目环境
   ↓
Step 2: 确定版本目录
   ↓
Step 3: 读取综合模板
   ↓
Step 4: 转化模板内容
   ↓
Step 5: 生成 task_plan.md
   ↓
Step 6: 调用 executor
```

### Step 1: 检测项目环境

```bash
python scripts/detect_environment.py --json
```

**环境检测结果**:

| 检测项 | 输出字段 | 说明 |
|--------|---------|------|
| Git | `git.exists`, `git.branch` | Git 仓库状态和当前分支 |
| 虚拟环境 | `virtual_env.has_env`, `virtual_env.env_type` | venv/uv/node_modules 等 |
| 项目架构 | `project_structure.has_src_dir`, `project_structure.language` | 目录结构和项目语言 |
| 项目类型 | `project_structure.project_type` | cli/fastapi/django/library/react 等 |

### Step 2: 确定版本目录

#### pjflow 目录架构

```
项目根目录/pjflow/
├── constitution.md    # 共享宪法文档（项目级）
├── requirements.md      # 共享需求文档（可选）
│
├── v0_initial/        # 初始项目创建
│   ├── task_plan.md
│   ├── progress.md
│   └── findings.md
│
├── v1_add_feature/    # 第1次新增功能
│   ├── task_plan.md
│   ├── progress.md
│   └── findings.md
│
└── v{N}_feature/      # 第N次新增功能
    ├── task_plan.md
    ├── progress.md
    └── findings.md
```

#### 版本目录命名规则

| 项目状态 | 版本目录名称 | 说明 |
|---------|-------------|------|
| new (新建项目) | `v0_initial` | 固定名称 |
| add-feature (新增功能) | `v{N}_{feature_name}` | N 为递增版本号 |

**版本号递增逻辑**:
```bash
existing_versions=$(find ./pjflow -maxdepth 1 -type d -name "v*" 2>/dev/null | sort -V)
if [ -z "$existing_versions" ]; then
    next_version=1
else
    max_version=$(echo "$existing_versions" | tail -1 | sed 's/v//')
    next_version=$((max_version + 1))
fi
echo "下一个版本号: v${next_version}"
```

### Step 3: 读取综合模板

| 语言 | 模板文件 | 状态 |
|------|---------|------|
| Python | `assets/templates/python-complete-template.md` | ✅ 完整 |
| TypeScript | `assets/templates/typescript-template.md` | ⚠️ 基础结构 |
| Go | `assets/templates/go-template.md` | ⚠️ 基础结构 |

### Step 4: 转化模板内容

**核心任务**: 将描述性模板转化为具体可执行的指令

#### 变量替换

| 模板变量 | 替换为 | 来源 |
|---------|--------|------|
| `{{GOAL}}` | 用户原始需求 | router 传入 |
| `{{PROJECT_STATUS}}` | new / add-feature | router 传入 |
| `{{COMPLEXITY}}` | simple / medium / complex | router 传入 |
| `{{LANGUAGE}}` | python / typescript / go | router 传入 |
| `{{VERSION_DIR}}` | v0_initial / v{N}_{feature} | Step 2 计算 |

#### Phase 选择

| Phase | new | add-feature |
|-------|-----|-------------|
| Phase 0: 需求互动 | medium/complex | medium/complex |
| Phase 1: 项目规则 | ✅ | ❌ |
| Phase 2: 项目构建 | ✅ | ❌ |
| Phase 3: 工作树准备 | ❌ | ✅ |
| Phase 4: TDD 执行 | ✅ | ✅ |
| Phase 5: 质量审核 | ✅ | ✅ |

### Step 5: 生成 task_plan.md

#### 5.1 创建版本目录

```bash
mkdir -p pjflow/{{VERSION_DIR}}
```

#### 5.2 创建 task_plan.md

**文件路径**: `pjflow/{{VERSION_DIR}}/task_plan.md`

**内容结构**:

```markdown
# 项目执行计划

## 目标
{{GOAL}}

## 参数
- 项目状态: {{PROJECT_STATUS}}
- 复杂度: {{COMPLEXITY}}
- 语言: {{LANGUAGE}}

## Phase 执行计划

### Phase 0: 需求互动 (如适用)
**Tool**: pyflow-brainstorming
**执行**: 探索用户需求

### Phase 1: 项目规则 (新项目)
**Tool**: pyflow-constitution
**执行**: 创建 constitution.md

### Phase 2: 项目构建 (新项目)
详见对应语言模板中的 Phase 2 部分（如 `python-complete-template.md`）

### Phase 3: 工作树准备 (老项目)
详见对应语言模板中的 Phase 3 部分（如 `python-complete-template.md`）

### Phase 4: TDD 执行
**Tool**: pyflow-tdd-cycle (或对应语言 TDD 工具)
**执行**: 根据 `{{COMPLEXITY}}` 选择 TDD 流程

### Phase 5: 质量审核
**Tool**: code-reviewer + Bash
**执行**: 质量检查和 Git 提交

## CHECKLIST
(从模板复制并初始化为全部未选中)
```

#### 5.3 创建 progress.md 和 findings.md

- **progress.md**: 记录执行日志
- **findings.md**: 记录知识库和发现

### Step 6: 调用 executor

```bash
Skill(skill="projectflow-executor", args="")
```

---

## 3. projectflow-executor（执行器）

### 职责
读取 task_plan.md，逐阶段执行计划，更新 progress.md 和 CHECKLIST.md

### 核心流程

```
读取 ./pjflow/{VERSION_DIR}/task_plan.md
   ↓
找到下一个 pending 的 Phase
   ↓
【强制验证】读取需求文档和宪法文件
   ↓
调用对应的 Tool（带入文档上下文）
   ↓
【强制验证】检查输出合规性
   ↓
更新 CHECKLIST.md
更新 progress.md
标记 Phase 为 complete
   ↓
所有 Phase 完成？
```

### 版本目录结构

```
pjflow/
├── v0_initial/           ← 新建项目
│   └── task_plan.md
│
├── v1_add_feature/    ← 第1次新增功能
│   └── task_plan.md
│
└── vN_add_feature/       ← 第N次新增功能
    └── task_plan.md
```

### 检测版本目录并读取 task_plan.md

```bash
# 找到最新版本目录
latest_version_dir=$(find ./pjflow -type d -name "v*" | sort -V | tail -1)

# 读取对应的 task_plan.md
task_plan_path="$latest_version_dir/task_plan.md"
```

### 每阶段检查清单

#### 执行前检查

```
□ 已读取 pjflow/constitution.md
□ 已读取 pjflow/requirements.md（如存在）
□ 已理解当前 Phase 的 Tool 和参数
□ 已准备好对应的工具调用
□ 确认不会手动编写业务代码
```

#### 执行后检查

```
□ Tool 执行完成，无错误
□ 输出符合 constitution.md 要求
□ 输出符合 requirements.md 要求
□ CHECKLIST.md 已更新
□ progress.md 已更新
□ Phase 状态已标记为 complete
```

### CHECKLIST 更新要求

#### 更新时机

| Phase | 更新时机 | 更新内容 |
|-------|---------|---------|
| Phase 0 | brainstorming 完成后 | 需求分析相关 checkbox |
| Phase 1 | constitution 创建后 | 项目规则相关 checkbox |
| Phase 2 | 脚手架创建后 | 项目准备相关 checkbox（含干扰检测） |
| Phase 3 | worktree 创建后 | 工作环境相关 checkbox（含 Git 分支、依赖、系统文件、新文件） |
| Phase 4 | TDD 完成后 | TDD 执行相关 checkbox |
| Phase 5 | 质量审核完成后 | 质量审核和 Git 相关 checkbox |

#### 更新方法

使用 **Edit 工具** 将 `[ ]` 替换为 `[x]`：

```python
Edit(
    file_path="CHECKLIST.md",
    old_string="- [ ] Constitution created/updated",
    new_string="- [x] Constitution created/updated"
)
```

**重要**: 未更新 CHECKLIST 视为 Phase 未完成！

### 编排者行为准则

**你是编排者（ORCHESTRATOR）**，不是执行者：
- ✅ **可以**创建脚手架（项目基础设施配置）
- ❌ **禁止**编写业务逻辑代码（必须使用 TDD 工具链）
- 🌍 **语言无关** - 适用于 Python, TypeScript, Go 等任何语言

### 四步执行流程

**每个 Phase 必须严格遵守**：

1. **调用 tool/skill/agent** → 使用 Skill/Task/Bash 工具
2. **等待完成** ⏸️ → 暂停所有操作，等待 tool 返回
3. **验证结果** ✓ → 检查输出是否符合预期
4. **记录状态** 📝 → 更新状态，继续下一阶段

### 判断标准

- 这是脚手架吗？（所有项目都需要） → 使用 **Write/Bash** 工具 ✅
- 这是业务逻辑吗？（包含具体功能） → 使用 **TDD 工具** ❌

### Tool 调用方式

| Tool 类型 | 调用方式 | 说明 |
|-----------|----------|------|
| **Skill** | `Skill(skill="name", args="...")` | 调用其他 skill |
| **Task** | `Task(subagent_type="...", ...)` | 调用 agent |
| **Bash** | `Bash(command="...")` | 执行命令 |
| **Write** | `Write(file_path="...", content="...")` | 写入文件 |
| **Edit** | `Edit(file_path="...", old_string="...", new_string="...")` | 编辑文件 |

### 语言无关性

| 语言 | TDD 工具示例 | 配置文件 |
|------|-------------|---------|
| Python | pyflow-tdd-cycle | pyproject.toml |
| TypeScript | tdd-typescript-tool | package.json |
| Go | go-tdd-tool | go.mod |
| Rust | cargo-tdd-tool | Cargo.toml |
| Java | junit-tdd-tool | pom.xml |

**Executor 不关心具体语言**，只关心：
1. 读取 task_plan.md
2. 调用定义的 Tool
3. 更新状态
4. 验证合规性

---

## 完整调度流程图

```
用户请求
    ↓
┌─────────────────────────────────────────┐
│  projectflow-router (三维检测器)      │
│  - 检测项目状态 (新/老)            │
│  - 检测复杂度 (简单/中等/复杂)        │
│  - 检测语言 (Python/TS/Go)        │
│  - 传递参数给 planner              │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│  projectflow-planner (计划生成器)     │
│  Step 1: 检测项目环境             │
│  Step 2: 确定版本目录            │
│  Step 3: 读取综合模板             │
│  Step 4: 转化模板内容             │
│  Step 5: 生成 task_plan.md         │
│  - 调用 executor                 │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│  projectflow-executor (执行器)        │
│  - 读取 task_plan.md              │
│  - 找到下一个 pending 的 Phase        │
│  - 验证文档 (constitution, reqs)    │
│  - 调用 Tool                    │
│  - 验证输出                      │
│  - 更新 CHECKLIST & progress        │
│  - 标记 Phase complete            │
│  - 循环直到所有 Phase 完成           │
└─────────────────────────────────────────┘
```

---

## 调度示例

### 示例 1: 新建简单的 Python CLI 工具

**用户请求**: "帮我创建一个简单的 Python CLI 工具"

**Router 检测**:
```bash
Skill(skill="projectflow-planner", args="--new --simple --python 帮我创建一个简单的 Python CLI 工具")
```

**Planner 执行**:
1. 检测环境（无 Git，无虚拟环境）
2. 确定版本目录: `v0_initial`
3. 读取 `python-complete-template.md`
4. 生成 `pjflow/v0_initial/task_plan.md`（Phase 1, 2, 4, 5）
5. 调用 executor

**Executor 执行**:
- Phase 1: 调用 `pyflow-constitution` 创建宪法
- Phase 2: 创建项目脚手架
- Phase 4: 调用 `pyflow-tdd-cycle` 实现功能
- Phase 5: 质量审核和 Git 提交

### 示例 2: 为现有 Python 项目添加中等复杂度的 API 功能

**用户请求**: "为这个项目添加一个用户认证 API"

**Router 检测**:
```bash
Skill(skill="projectflow-planner", args="--add-feature --medium --python 为这个项目添加一个用户认证 API")
```

**Planner 执行**:
1. 检测环境（已存在 Git 和项目结构）
2. 确定版本目录: `v1_auth_api`
3. 读取 `python-complete-template.md`
4. 生成 `pjflow/v1_auth_api/task_plan.md`（Phase 0, 3, 4, 5）
5. 调用 executor

**Executor 执行**:
- Phase 0: 调用 `pyflow-brainstorming` 探索需求
- Phase 3: 创建 feature 分支，添加依赖
- Phase 4: 调用 `pyflow-tdd-cycle` 实现 API
- Phase 5: 质量审核和 PR

---

## 版本信息

- **Router**: 4.0.0 - 三维检测器（语言无关）
- **Planner**: 4.0.0 - 环境检测 + 模板转化 + 计划生成
- **Executor**: 4.0.0 - 逐阶段执行器（语言无关）

---

**文档版本**: 1.0.0
**最后更新**: 2025-02-12

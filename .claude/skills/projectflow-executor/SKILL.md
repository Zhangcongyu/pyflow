---
name: projectflow-executor
description: |
  读取 pjflow/versioned/task_plan.md，逐阶段执行计划，更新 progress.md 和 CHECKLIST.md。

  触发条件: 由 projectflow-planner 调用，或用户说"继续执行 task_plan.md"

  核心职责: 逐阶段执行计划，更新 CHECKLIST.md 和 progress.md，标记 Phase 状态

  编排原则: ✅ 可创建脚手架 | ❌ 禁止编写业务逻辑 | ❌ 语言无关
---

# Projectflow Executor

## 核心流程

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

## 每阶段检查清单

### 执行前检查

```
□ 已读取 pjflow/constitution.md
□ 已读取 pjflow/requirements.md（如存在）
□ 已理解当前 Phase 的 Tool 和参数
□ 已准备好对应的工具调用
□ 确认不会手动编写业务代码
```

### 执行后检查

```
□ Tool 执行完成，无错误
□ 输出符合 constitution.md 要求
□ 输出符合 requirements.md 要求
□ CHECKLIST.md 已更新
□ progress.md 已更新
□ Phase 状态已标记为 complete
```

## CHECKLIST 更新要求 ⭐

### 更新时机

| Phase | 更新时机 | 更新内容 |
|-------|---------|---------|
| Phase 0 | brainstorming 完成后 | 需求分析相关 checkbox |
| Phase 1 | constitution 创建后 | 项目规则相关 checkbox |
| Phase 2 | 脚手架创建后 | 项目准备相关 checkbox（含干扰检测） |
| Phase 3 | worktree 创建后 | 工作环境相关 checkbox（含 Git 分支、依赖、系统文件、新文件） |
| Phase 4 | TDD 完成后 | TDD 执行相关 checkbox |
| Phase 5 | 质量审核完成后 | 质量审核和 Git 相关 checkbox |

### 更新方法

使用 **Edit 工具** 将 `[ ]` 替换为 `[x]`：

```python
Edit(
    file_path="CHECKLIST.md",
    old_string="- [ ] Constitution created/updated",
    new_string="- [x] Constitution created/updated"
)
```

### 验证 CHECKLIST 已更新

```bash
# 确认至少有一个 [x] 标记
grep -q "\[x\]" CHECKLIST.md && echo "✅ CHECKLIST 已更新" || echo "❌ CHECKLIST 未更新"

# 统计已完成的项
echo "已完成: $(grep '\[x\]' CHECKLIST.md | wc -l) 项"
```

**重要**: 未更新 CHECKLIST 视为 Phase 未完成！

## 编排者行为准则

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

### 绝对禁止

- ❌ 在 tool 执行期间自己写代码
- ❌ 在 tool 执行期间自己创建文件
- ❌ 认为"tool 太慢，我来帮忙"
- ❌ 跳过等待直接进入下一阶段
- ❌ 手动编写业务逻辑代码

### 判断标准

- 这是脚手架吗？（所有项目都需要） → 使用 **Write/Bash** 工具 ✅
- 这是业务逻辑吗？（包含具体功能） → 使用 **TDD 工具** ❌

## 执行流程

### Step 1: 检测版本目录并读取 task_plan.md

**版本目录结构**:
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

**检测逻辑**:
```bash
# 找到最新版本目录
latest_version_dir=$(find ./pjflow -type d -name "v*" | sort -V | tail -1)

# 读取对应的 task_plan.md
task_plan_path="$latest_version_dir/task_plan.md"
```

### Step 2: 找到下一个 pending 的 Phase

遍历 task_plan.md 中的所有 Phase，找到第一个 `Status: pending` 的 Phase

### Step 3: 执行前强制验证

**读取合规文档**:

```bash
# 始终检查这些文档
pjflow/constitution.md          # 项目宪法（共享）
pjflow/requirements.md          # 需求文档（如存在）
pjflow/{VERSION_DIR}/task_plan.md  # 当前执行计划
```

**验证要点**:
- 确认计划中的 Tool 类型
- 确认参数和配置
- 确认是否需要传入文档上下文

### Step 4: 更新 Phase 状态为 in_progress

使用 **Edit 工具**将 Status 从 `pending` 改为 `in_progress`

### Step 5: 判断脚手架 vs 业务编码

**在调用任何 Tool 之前**，必须判断当前 Phase 是否属于脚手架创建：

**判断标准**:
- 这是脚手架吗？（所有项目都需要） → 使用 **Write/Bash** 工具 ✅
- 这是业务逻辑吗？（包含具体功能） → 使用 **TDD 工具** ❌

**示例**:
```
Phase 2 (项目准备)     → 脚手架 → 使用 Write 工具创建目录和配置 ✅
Phase 4 (TDD 执行)      → 业务逻辑 → 调用 pyflow-tdd-cycle ❌
```

### Step 6: 调用 Tool

根据 task_plan.md 中定义的 Tool 类型调用：

| Tool 类型 | 调用方式 | 说明 |
|-----------|----------|------|
| **Skill** | `Skill(skill="name", args="...")` | 调用其他 skill |
| **Task** | `Task(subagent_type="...", ...)` | 调用 agent |
| **Bash** | `Bash(command="...")` | 执行命令 |
| **Write** | `Write(file_path="...", content="...")` | 写入文件 |
| **Edit** | `Edit(file_path="...", old_string="...", new_string="...")` | 编辑文件 |

**重要**: 必须等待 Tool 返回结果后再继续

### Step 7: 验证输出

**验证清单**:
- Tool 执行无错误
- 输出符合 constitution.md
- 输出符合 requirements.md（如存在）
- 文件/目录创建正确

### Step 8: 更新状态和记录

1. **更新 CHECKLIST.md**: 将对应 checkbox 改为 `[x]`
2. **更新 progress.md**: 记录执行结果
3. **标记 Phase 为 complete**: 使用 Edit 工具更新状态

### Step 9: 继续下一 Phase 或完成

回到 Step 2，继续执行下一个 Phase，直到所有 Phase 完成。

## 语言无关性

**Executor 是语言无关的**，适用于任何编程语言：

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

## 常见错误对照

| ❌ 错误 | ✅ 正确 | 说明 |
|---------|--------|------|
| 手动创建业务代码文件 | 调用 TDD 工具 | 禁止手动编码 |
| 跳过等待直接下一阶段 | 等待 Tool 返回 | 必须等待完成 |
| 忘记更新 CHECKLIST | 每个 Phase 完成后更新 | P0 级别要求 |
| 未读取 constitution | 每个 Phase 前读取 | 强制验证 |
| 认为自己更快 | 让工具完成 | 工具更可靠 |

---

**版本**: 4.0.0
**用途**: ProjectFlow 架构 - 执行器（语言无关）
**更新**:
- 强化每阶段强制检查，严格落实需求和宪法文件
- 扩展 Phase 3 旧项目工作流程（Git 分支、依赖管理、系统文件更新、新功能文件创建）
- 完善 CHECKLIST 更新要求

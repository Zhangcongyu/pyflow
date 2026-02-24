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

## Step 3: 判断脚手架 vs 业务逻辑

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

**触发条件**: Phase 1 完成后，且 `{{COMPLEXITY}}` == simple

**说明**: 对于简单项目，不需要调用 brainstorming skill，直接生成需求文档模板。

**参考模板**:
- Python: `../projectflow-planner/assets/templates/python-complete-template.md` (Step 5.5)
- TypeScript: `../projectflow-planner/assets/templates/typescript-complete-template.md` (Step 5.5)
- Go: `../projectflow-planner/assets/templates/go-template.md` (Step 5.5)

**执行方式**: 使用 Write 工具，按模板写入需求文档

**输出位置**: `pjflow/{VERSION_DIR}/requirements.md`

**Skip if**: 复杂度为 medium 或 complex

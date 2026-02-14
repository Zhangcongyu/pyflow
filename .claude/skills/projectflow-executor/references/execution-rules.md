# Execution Rules

本文档详细说明 Tool 调用格式和 CHECKLIST 更新规则。

---

## Tool Type 调用格式

### Skill

**格式**:
```python
Skill(skill="skill-name", args="arguments")
```

**示例**:
```python
# Constitution 创建
Skill(skill="pyflow-constitution", args="--simple")

# TDD 流程
Skill(skill="pyflow-tdd-cycle", args="创建待办事项应用")

# 需求分析
Skill(skill="pyflow-brainstorming", args="新项目：待办事项应用")

# Git worktree
Skill(skill="pyflow-using-git-worktrees", args="feature/add-todo")
```

---

### Task (subagent_type)

**格式**:
```python
Task(
    subagent_type="agent-type",
    subject="简短标题（imperative form）",
    activeForm="正在进行时",
    description="详细描述",
    prompt="完整上下文"
)
```

**参数说明**:
- `subagent_type`: Agent 类型（必需，第一位）
- `subject`: 简短标题，imperative form（必需）
- `activeForm`: 正在进行时，用于 spinner 显示（必需）
- `description`: 详细描述（必需）
- `prompt`: 完整上下文（必需）

**示例**:
```python
# Python 开发
Task(
    subagent_type="pyflow-python-pro",
    subject="实现 FastAPI CRUD 接口",
    activeForm="实现 FastAPI CRUD 接口中",
    description="根据测试文件实现所有 CRUD 功能",
    prompt="请实现 tests/test_api.py 中定义的所有测试，使用 FastAPI 和 SQLAlchemy"
)

# 测试生成
Task(
    subagent_type="pyflow-test-automator",
    subject="生成测试用例",
    activeForm="生成测试用例中",
    description="为待办事项应用生成完整测试套件",
    prompt="生成包含 CRUD 操作的完整测试，使用 pytest"
)

# 代码审核
Task(
    subagent_type="pyflow-code-reviewer",
    subject="审核代码质量",
    activeForm="审核代码质量中",
    description="检查代码质量和 constitution 合规性",
    prompt="审核 src/ 目录下的所有代码，确保符合项目规范"
)
```

**⚠️ 常见错误对照**:

| ❌ 错误 | ✅ 正确 | 说明 |
|---------|--------|------|
| `description="..."` 在第一位 | `subagent_type="..."` 在第一位 | 参数顺序重要 |
| 无 `subject` | `subject="..."` (必需) | 必须有 subject |
| 无 `activeForm` | `activeForm="..."` (必需) | 必须有 activeForm |
| 凭记忆调用 | 参考本文档 | 必须遵守格式 |

---

### Command / Bash

**格式**:
```python
Bash(command="command arguments")
```

**示例**:
```python
# 运行测试
Bash(command="pytest tests/ -v")

# 代码检查
Bash(command="ruff check src/")

# 类型检查
Bash(command="mypy src/")

# 覆盖率测试
Bash(command="pytest --cov=src --cov-report=term-missing")

# 组合命令
Bash(command="pytest tests/ -v && ruff check src/ && mypy src/")
```

---

## CHECKLIST 更新规则

### 更新时机

每个 Phase 完成后，**必须**更新 CHECKLIST.md 对应的 checkbox。

### 更新方法

使用 **Edit 工具**将 `[ ]` 替换为 `[x]`：

```python
Edit(
    file_path="CHECKLIST.md",
    old_string="- [ ] Constitution created/updated\n- [ ] Project-specific rules defined",
    new_string="- [x] Constitution created/updated\n- [x] Project-specific rules defined"
)
```

### Phase 对应的 CHECKLIST 项

| Phase | CHECKLIST 项 |
|-------|-------------|
| Phase 0 | Requirements clarified, Design document created |
| Phase 1 | Constitution created/updated, Project-specific rules defined |
| Phase 2 | Project scaffold created, Git initialized, CHECKLIST.md created |
| Phase 4.1 | Tests generated (RED), Test structure defined |
| Phase 4.2 | All features implemented (GREEN), All tests pass |
| Phase 4.3 | Code refactored (REFACTOR), All tests still pass |
| Phase 5.1 | All tests pass, Coverage meets minimum, Code style checks pass |
| Phase 5.2 | Code review completed, Constitution compliance verified |
| Phase 5.3 | Security audit completed, Security best practices verified |
| Phase 5.4 | All changes committed, Feature branch merged |

### 验证 CHECKLIST 已更新

```bash
# 确认至少有一个 [x] 标记
grep -q "\[x\]" CHECKLIST.md && echo "✅ CHECKLIST 已更新" || echo "❌ CHECKLIST 未更新"

# 统计已完成的项
echo "已完成: $(grep '\[x\]' CHECKLIST.md | wc -l) 项"
```

---

## progress.md 更新规则

### 更新格式

```markdown
## [YYYY-MM-DD HH:MM:SS] Phase N: <Description>

**执行结果**: ✅ 成功 / ❌ 失败

**工具**: <Tool>

**详情**:
- [列出关键结果]

**CHECKLIST 更新**: 已更新 / 跳过

**合规性验证**: ✅ 通过 / ⚠️ 部分违规 / ❌ 不合规 / N/A
- Constitution 合规性: [验证结果]
- Requirements 合规性: [验证结果，如适用]

**Status**: complete / failed
```

### 更新方法

使用 **Edit 工具**在 progress.md 顶部添加新的 Section：

```python
Edit(
    file_path="./pjflow/progress.md",
    old_string="# Progress Log\n\n## Session Start",
    new_string="# Progress Log\n\n## [2026-02-11 10:30:00] Phase 1: 项目规则\n\n**执行结果**: ✅ 成功\n\n**工具**: pyflow-constitution\n\n**详情**:\n- Constitution 创建成功\n- 项目规则已定义\n\n**CHECKLIST 更新**: 已更新\n\n**合规性验证**: ✅ 通过\n- Constitution 合规性: 已创建，无占位符\n\n**Status**: complete\n\n---\n\n## Session Start"
)
```

---

## task_plan.md 更新规则

### 更新 Current Phase

使用 **Edit 工具**更新 `Current Phase` 字段：

```python
Edit(
    file_path="./pjflow/task_plan.md",
    old_string="## Current Phase\nPhase 1",
    new_string="## Current Phase\nPhase 2"
)
```

### 更新 Phase Status

使用 **Edit 工具**将 Phase 的 `Status: pending` 改为 `Status: in_progress`，完成后改为 `Status: complete`：

```python
# 标记为 in_progress
Edit(
    file_path="./pjflow/task_plan.md",
    old_string="- Status: pending",
    new_string="- Status: in_progress"
)

# 标记为 complete
Edit(
    file_path="./pjflow/task_plan.md",
    old_string="- Status: in_progress",
    new_string="- Status: complete"
)
```

---

## 完整执行示例

### 示例: 执行 Phase 1（项目规则）

**初始状态** (task_plan.md):
```markdown
## Current Phase
Phase 1

### Phase 1: 项目规则
- Tool: pyflow-constitution
- Tool Type: Skill
- Args: --simple
- CHECKLIST:
  - [ ] Constitution created/updated
  - [ ] Project-specific rules defined
- Status: pending
```

**执行步骤**:

1. **标记为 in_progress**:
```python
Edit(file_path="./pjflow/task_plan.md", old_string="- Status: pending", new_string="- Status: in_progress")
```

2. **调用 Tool**:
```python
Skill(skill="pyflow-constitution", args="--simple")
```

3. **更新 CHECKLIST.md**:
```python
Edit(
    file_path="CHECKLIST.md",
    old_string="- [ ] Constitution created/updated\n- [ ] Project-specific rules defined",
    new_string="- [x] Constitution created/updated\n- [x] Project-specific rules defined"
)
```

4. **更新 progress.md**:
```python
Edit(
    file_path="./pjflow/progress.md",
    old_string="# Progress Log\n",
    new_string="# Progress Log\n\n## [2026-02-11 10:30:00] Phase 1: 项目规则\n\n**执行结果**: ✅ 成功\n\n**工具**: pyflow-constitution\n\n**详情**:\n- Constitution 创建成功\n- 项目规则已定义\n\n**CHECKLIST 更新**: 已更新\n\n**合规性验证**: ✅ 通过\n- Constitution 合规性: 已创建，无占位符\n\n**Status**: complete\n\n---\n\n"
)
```

5. **标记 Phase 为 complete**:
```python
Edit(file_path="./pjflow/task_plan.md", old_string="- Status: in_progress", new_string="- Status: complete")
```

6. **更新 Current Phase**:
```python
Edit(file_path="./pjflow/task_plan.md", old_string="## Current Phase\nPhase 1", new_string="## Current Phase\nPhase 2")
```

**最终状态** (task_plan.md):
```markdown
## Current Phase
Phase 2

### Phase 1: 项目规则
...
- Status: complete
```

---

## 错误处理

### Tool 执行失败

**处理流程**:
1. 记录错误到 progress.md
2. 标记 Phase 为 `Status: failed`
3. 询问用户是否重试或跳过

**示例**:
```markdown
## [2026-02-11 10:35:00] Phase 2: 项目准备

**执行结果**: ❌ 失败

**工具**: Bash (uv init)

**错误**: uv: command not found

**建议**: 安装 uv 后重试 (pip install uv)

**Status**: failed
```

### CHECKLIST.md 不存在

**处理流程**:
1. 在 progress.md 中记录警告
2. 跳过 CHECKLIST 更新
3. 继续执行下一个 Phase

### task_plan.md 损坏

**处理流程**:
1. 在 progress.md 中记录错误详情
2. 停止执行
3. 询问用户提供正确的 task_plan.md

---

**文档版本**: 1.0.0
**最后更新**: 2026-02-11

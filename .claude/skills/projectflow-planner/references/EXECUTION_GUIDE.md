# 生成并执行 task_plan.md

## Step 5.1: 创建版本目录

```bash
mkdir -p pjflow/{{VERSION_DIR}}
```

## Step 5.2: 创建 task_plan.md

**文件路径**: `pjflow/{{VERSION_DIR}}/task_plan.md`

**最小内容结构**:

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
详见对应语言模板中的 Phase 2 部分

### Phase 3: 工作树准备 (老项目)
详见对应语言模板中的 Phase 3 部分

### Phase 4: TDD 执行
**Tool**: pyflow-tdd-cycle (或对应语言 TDD 工具)
**执行**: 根据 `{{COMPLEXITY}}` 选择 TDD 流程

### Phase 5: 质量审核
**Tool**: code-reviewer + Bash
**执行**: 质量检查和 Git 提交

## CHECKLIST
(从模板复制并初始化为全部未选中)
```

## Step 5.3: 创建 progress.md 和 findings.md

- **progress.md**: 记录执行日志
- **findings.md**: 记录知识库和发现

## Step 6: 调用 executor

```bash
Skill(skill="projectflow-executor", args="")
```

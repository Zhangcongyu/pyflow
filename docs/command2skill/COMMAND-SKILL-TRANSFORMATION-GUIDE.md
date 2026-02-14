# Command/Skill 双重机制改造指南

**版本**: 1.0
**创建时间**: 2026-02-06
**基于**: `tdd-cycle.md` 改造经验

---

## 📖 概述

本文档总结将纯 command 文档改造成 **command/skill 双重格式** 的经验和方法。

### 目标

使 command 文档既能：
- ✅ 作为 **command** 被用户直接调用
- ✅ 作为 **skill** 被编排器自动调用
- ✅ 保持自包含，无需额外代码
- ✅ 支持参数传递和交互

### 适用场景

- 将现有的 command 改造成通用格式
- 创建可被编排器调用的工作流
- 实现灵活的触发机制

---

## 🔍 参考模式分析

### speckit.constitution.md 的核心特征

#### 1. YAML Frontmatter

```yaml
---
description: Create or update the project constitution from interactive or provided principle inputs, ensuring all dependent templates stay in sync.
handoffs:
  - label: Build Specification
    agent: speckit.specify
    prompt: Implement the feature specification based on the updated constitution. I want to build...
---
```

**作用**:
- `description`: 触发条件和使用场景
- `handoffs`: 执行后的推荐操作

#### 2. User Input 接收

```markdown
## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).
```

**作用**:
- 作为 command: 接收命令行参数
- 作为 skill: 接收 `args` 参数
- 通用占位符机制

#### 3. 自包含逻辑

整个文档包含完整的执行指令：
- 执行流程
- 验证步骤
- 输出要求
- 错误处理

**无需额外代码**: 文档本身就是可执行指令

---

## 🛠️ 改造步骤

### Step 1: 分析源文件

#### 1.1 理解原始结构

**任务**: 分析源文件的组成部分

**检查项**:
- [ ] 文件的主要功能
- [ ] 执行流程（有几个阶段）
- [ ] 涉及的 agents/tools
- [ ] 输入输出
- [ ] 验证步骤

**示例 - tdd-cycle.md 分析**:

```markdown
# 原始结构分析

## 功能
TDD 工作流执行（RED-GREEN-REFACTOR）

## 执行流程（6 个 Phase）
1. Test Specification and Design
2. RED - Write Failing Tests
3. GREEN - Make Tests Pass
4. REFACTOR - Improve Code Quality
5. Integration and System Tests
6. Continuous Improvement Cycle

## 涉及的 agents
- unit-testing::test-automator
- comprehensive-review::architect-review
- backend-development::backend-architect

## 输入
$ARGUMENTS (feature description)

## 输出
- Tests
- Implementation
- Reports
```

#### 1.2 识别需要改造的部分

**检查清单**:
- [ ] 缺少 YAML frontmatter
- [ ] 没有 User Input 接收部分
- [ ] Agent 调用格式过时（使用 `::` 而不是 `:`）
- [ ] 缺少明确的 Prompt Template
- [ ] 缺少 Validation 步骤
- [ ] 缺少 Output 说明

---

### Step 2: 添加 YAML Frontmatter

#### 2.1 编写 description

**要求**: 清晰描述触发条件和使用场景

**模板**:
```yaml
---
description: |
  [功能描述]，[使用场景]。

  Use for [主要用途]:
  1. [场景 1]
  2. [场景 2]
  3. [场景 3]

  Ensure [关键目标] through [方法]。
```

**示例 - tdd-cycle**:
```yaml
---
description: |
  Execute comprehensive Test-Driven Development (TDD) workflow with strict red-green-refactor discipline.
  Use for implementing features or bugfixes with test-first methodology, ensuring quality through
  coordinated agent orchestration with fail-first verification, incremental implementation, and
  continuous refactoring.
```

**关键要素**:
- ✅ 动作开头
- ✅ 明确功能
- ✅ 使用场景
- ✅ 保证结果

#### 2.2 编写 handoffs

**要求**: 推荐执行后的后续操作

**模板**:
```yaml
handoffs:
  - label: [后续操作名称]
    agent: [agent 类型]
    prompt: [推荐的提示词]
  - label: [另一个后续操作]
    agent: [另一个 agent]
    prompt: [另一个提示词]
```

**示例 - tdd-cycle**:
```yaml
handoffs:
  - label: Code Review
    agent: comprehensive-review:code-reviewer
    prompt: Review the TDD implementation for code quality, test coverage, and adherence to TDD principles...
  - label: Security Audit
    agent: comprehensive-review:security-auditor
    prompt: Perform security analysis of the TDD implementation...
```

**原则**:
- 2-4 个 handoffs 为宜
- 按优先级排序
- prompt 要具体

---

### Step 3: 添加 User Input 接收

#### 3.1 标准格式

```markdown
## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).
```

#### 3.2 放置位置

- ✅ 紧跟 YAML frontmatter
- ✅ 在任何执行流程之前
- ✅ 作为独立的顶级标题

#### 3.3 使用 $ARGUMENTS

在文档的适当位置引用 `$ARGUMENTS`：

```markdown
## Outline

Execute [功能] for: $ARGUMENTS

This workflow will...
```

**最佳实践**:
- 在开头说明整体目标
- 在每个 agent 的 prompt 中引用
- 保持一致的变量名

---

### Step 4: 优化文档结构

#### 4.1 标准化每个步骤

**改造前**（tdd-cycle 原始格式）:
```markdown
### 1. Requirements Analysis

- Use Task tool with subagent_type="comprehensive-review::architect-review"
- Prompt: "Analyze requirements for: $ARGUMENTS. Define acceptance criteria..."
- Output: Test specification, acceptance criteria, edge case matrix
- Validation: Ensure all requirements have corresponding test scenarios
```

**改造后**（标准化格式）:
```markdown
### 1. Requirements Analysis

**Agent**: `comprehensive-review:architect-review`

**Prompt Template**:
```
Analyze requirements for: $ARGUMENTS

Define:
- Acceptance criteria with measurable outcomes
- Edge cases and boundary conditions
- Test scenarios covering happy paths and error paths

Output: Comprehensive test specification document.
```

**Validation**:
- [ ] All requirements have corresponding test scenarios
- [ ] Edge cases identified and documented
- [ ] Acceptance criteria are measurable and testable

**Output**: Test specification, acceptance criteria, edge case matrix
```

**改进点**:
1. ✅ 明确标注 **Agent** 类型
2. ✅ **Prompt Template** 使用代码块
3. ✅ **Validation** 使用检查清单
4. ✅ **Output** 明确说明

#### 4.2 添加验证门禁

在关键步骤后添加：

```markdown
**GATE**: Do not proceed until [条件]
```

**示例**:
```markdown
**GATE**: All tests must pass before proceeding
**GATE**: Do not proceed until all tests fail appropriately
```

#### 4.3 添加检查清单

为关键阶段添加验证清单：

```markdown
### RED Phase Validation

- [ ] All tests written before implementation
- [ ] All tests fail with meaningful error messages
- [ ] Test failures are due to missing implementation
- [ ] No test passes accidentally
- [ ] Test code has no syntax errors
```

---

### Step 5: 更新 Agent 调用格式

#### 5.1 识别过时格式

**过时格式**:
```markdown
subagent_type="unit-testing::test-automator"
subagent_type="comprehensive-review::architect-review"
```

**当前格式**:
```markdown
subagent_type="unit-testing:test-automator"
subagent_type="comprehensive-review:architect-review"
```

**区别**: `::` → `:`

#### 5.2 批量替换

**方法**: 使用编辑器的查找替换功能

```
查找: ::(\w+)
替换: :\1
```

**注意事项**:
- ✅ 确保只替换 agent 类型中的 `::`
- ⚠️ 不要替换文本中的其他 `::`
- ⚠️ 保留代码块中的 `::`（如 C++ 的作用域解析）

#### 5.3 更新 agent 引用

**改造前**:
```markdown
- Use Task tool with subagent_type="backend-development::backend-architect"
```

**改造后**:
```markdown
**Agent**: `python-development:python-pro` (for Python) or appropriate language agent
```

**改进**:
- ✅ 使用独立的 **Agent** 标注
- ✅ 使用代码格式（反引号）
- ✅ 添加语言说明

---

### Step 6: 优化 Prompt

#### 6.1 Prompt Template 结构

**标准结构**:
```
[任务说明] for: $ARGUMENTS

Requirements:
- [要求 1]
- [要求 2]
- [要求 3]

Constraints:
- [约束 1]
- [约束 2]

Output: [输出说明]
```

**示例**:
```markdown
**Prompt Template**:
```
Write FAILING unit tests for: $ARGUMENTS

Requirements:
- Tests must fail initially (before implementation)
- Include edge cases, error scenarios, and happy paths
- DO NOT implement any production code
- Follow test architecture design from Phase 1

Test coverage:
- Unit tests for all public methods
- Boundary value tests
- Error handling tests
- State transition tests

Output: Complete test suite with all tests failing.
```
```

#### 6.2 Prompt 编写原则

1. **明确任务**: 使用祈使句开头
2. **引用参数**: 使用 `$ARGUMENTS`
3. **列举要求**: 使用列表
4. **明确输出**: 说明期望的输出
5. **添加约束**: 说明限制条件

---

### Step 7: 验证和测试

#### 7.1 文件结构验证

**检查清单**:
- [ ] YAML frontmatter 正确（description, handoffs）
- [ ] User Input 部分存在
- [ ] $ARGUMENTS 在适当位置引用
- [ ] 所有步骤使用标准化格式
- [ ] Agent 格式正确（使用 `:`）
- [ ] Prompt Template 完整
- [ ] Validation 步骤明确
- [ ] Output 说明清晰

#### 7.2 系统识别验证

**方法**: 检查 system-reminder

**期望结果**:
```
- [command-name]: [description]...
```

**示例**:
```
- tdd-cycle: Execute comprehensive Test-Driven Development (TDD) workflow with strict red-green-refactor discipline...
```

#### 7.3 功能测试

**作为 command 测试**:
```bash
# 检查文件是否存在
ls .claude/commands/[command-name].md

# 检查文件权限
chmod +x .claude/commands/[command-name].md
```

**作为 skill 测试**:
```python
# 在对话中测试调用
Skill(
    skill="[command-name]",
    args="[测试参数]"
)
```

---

## 📋 改造模板

### 完整模板

```markdown
---
description: |
  [简短描述]。Use for [主要用途]:
  1. [场景 1]
  2. [场景 2]
  3. [场景 3]

  Ensure [关键目标] through [方法]。
handoffs:
  - label: [后续操作 1]
    agent: [agent-1]
    prompt: [推荐提示词 1]
  - label: [后续操作 2]
    agent: [agent-2]
    prompt: [推荐提示词 2]
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

Execute [功能] for: `$ARGUMENTS`

This workflow will [整体说明]。

Follow this execution flow:

## [Phase/Section 1]

### Step 1.1: [步骤名称]

**Agent**: `agent-type:agent-name`

**Prompt Template**:
```
[任务描述] for: $ARGUMENTS

Requirements:
- [要求 1]
- [要求 2]

Constraints:
- [约束 1]
- [约束 2]

Output: [输出说明]
```

**Validation**:
- [ ] [验证项 1]
- [ ] [验证项 2]
- [ ] [验证项 3]

**Output**: [输出内容]

**GATE**: [门禁条件] (如果适用)

---

## [Phase/Section 2]

... (重复相同结构)

---

## Validation Checkpoints

### [阶段 1] Validation

- [ ] [检查项 1]
- [ ] [检查项 2]
- [ ] [检查项 3]

### [阶段 2] Validation

... (重复相同结构)

---

## Success Criteria

- [ ] [成功标准 1]
- [ ] [成功标准 2]
- [ ] [成功标准 3]

---

## Notes

### Key Principles

- [原则 1]
- [原则 2]
- [原则 3]

### Best Practices

- [最佳实践 1]
- [最佳实践 2]

### Troubleshooting

**Problem**: [问题描述]
**Solution**: [解决方案]

---

**Execution for**: $ARGUMENTS

**Start Time**: [timestamp]

**Completion**: When all success criteria are met
```

---

## 🎯 改造示例对比

### 示例 1: 简单步骤改造

#### 改造前

```markdown
### 3. Write Unit Tests

- Use Task tool with subagent_type="unit-testing::test-automator"
- Prompt: "Write FAILING unit tests for: $ARGUMENTS"
- Output: Failing unit tests
```

#### 改造后

```markdown
### 3. Write Unit Tests (Failing)

**Agent**: `unit-testing:test-automator`

**Prompt Template**:
```
Write FAILING unit tests for: $ARGUMENTS

Requirements:
- Tests must fail initially (before implementation)
- Include edge cases, error scenarios, and happy paths
- DO NOT implement any production code

Output: Complete test suite with all tests failing.
```

**CRITICAL Validation**:
- [ ] All tests fail with expected error messages
- [ ] Test failures are due to missing implementation
- [ ] No test passes accidentally

**Output**: Failing unit tests, test documentation

**GATE**: Do not proceed until all tests fail appropriately
```

---

### 示例 2: Agent 格式更新

#### 改造前

```markdown
- Use Task tool with subagent_type="comprehensive-review::architect-review"
- Prompt: "Analyze requirements for: $ARGUMENTS"
```

#### 改造后

```markdown
**Agent**: `comprehensive-review:architect-review`

**Prompt Template**:
```
Analyze requirements for: $ARGUMENTS

Define:
- Acceptance criteria with measurable outcomes
- Edge cases and boundary conditions
- Test scenarios covering all paths

Output: Comprehensive test specification document.
```
```

---

## ⚠️ 常见问题和解决方法

### 问题 1: 系统不识别改造后的文件

**症状**: system-reminder 中看不到新的 skill

**可能原因**:
1. YAML frontmatter 格式错误
2. description 不清晰
3. 文件位置不正确

**解决方法**:
```yaml
# 确保 frontmatter 格式正确
---
description: [清晰的描述]
handoffs:
  - label: [名称]
    agent: [agent]
    prompt: [提示词]
---
```

**验证**:
```bash
# 检查文件位置
ls .claude/commands/[filename].md

# 检查文件权限
chmod 644 .claude/commands/[filename].md
```

---

### 问题 2: $ARGUMENTS 没有被替换

**症状**: 文档中出现 `$ARGUMENTS` 字符串而不是实际参数

**可能原因**:
1. 没有在正确的位置引用
2. 使用了错误的变量名

**解决方法**:
```markdown
## User Input

```text
$ARGUMENTS
```

# 在正文中引用
Execute [功能] for: $ARGUMENTS

# 在 prompt 中引用
**Prompt Template**:
```
[任务] for: $ARGUMENTS
```
```

---

### 问题 3: Agent 调用失败

**症状**: Agent 执行时报错

**可能原因**:
1. Agent 名称格式错误（使用了 `::`）
2. Agent 不存在
3. Prompt 不完整

**解决方法**:
```markdown
# 错误格式
**Agent**: `unit-testing::test-automator`

# 正确格式
**Agent**: `unit-testing:test-automator`

# 确保使用当前系统支持的 agent
# 参考 system-reminder 中的 agent 列表
```

---

### 问题 4: 结构过于复杂

**症状**: 文档过长，难以维护

**可能原因**:
1. 包含过多细节
2. 重复内容过多
3. 没有使用渐进式披露

**解决方法**:
```markdown
# 主体保持简洁
## Main Workflow

[核心流程]

# 详细内容放到最后
## Appendix: Detailed Prompts

[完整的 prompt 列表]

## Appendix: Validation Criteria

[详细的验证标准]
```

---

## 📊 改造检查清单

### 准备阶段

- [ ] 阅读参考文件（speckit.constitution.md）
- [ ] 分析源文件结构
- [ ] 识别需要改造的部分
- [ ] 规划改造步骤

### 执行阶段

- [ ] 添加 YAML frontmatter
  - [ ] 编写 description
  - [ ] 编写 handoffs
- [ ] 添加 User Input 部分
- [ ] 更新文档结构
  - [ ] 标准化每个步骤
  - [ ] 添加 Agent 标注
  - [ ] 添加 Prompt Template
  - [ ] 添加 Validation
  - [ ] 添加 Output
- [ ] 更新 Agent 格式
  - [ ] 替换 `::` 为 `:`
  - [ ] 验证 agent 存在
- [ ] 添加验证门禁
- [ ] 添加检查清单
- [ ] 优化 Prompt

### 验证阶段

- [ ] 文件结构检查
- [ ] YAML 格式验证
- [ ] Agent 格式验证
- [ ] 系统识别验证
- [ ] 功能测试

### 完成阶段

- [ ] 创建改造总结文档
- [ ] 记录关键改进
- [ ] 更新相关文档
- [ ] 提交到版本控制

---

## 🎓 最佳实践

### 1. 保持自包含

- ✅ 所有逻辑在一个文件中
- ✅ 不依赖外部文件
- ✅ 文档即代码

### 2. 使用标准化格式

- ✅ 统一的步骤结构
- ✅ 统一的标注格式
- ✅ 统一的验证方式

### 3. 渐进式披露

- ✅ 核心流程在前
- ✅ 详细内容在后
- ✅ 使用附录和引用

### 4. 明确的验证

- ✅ 每个步骤都有验证
- ✅ 关键步骤有门禁
- ✅ 使用检查清单

### 5. 清晰的输出

- ✅ 明确说明每个步骤的输出
- ✅ 输出格式清晰
- ✅ 可追踪可验证

---

## 📚 参考资料

### 参考文件

1. **speckit.constitution.md**
   - 位置: `/home/congyu/project/pyflow/.claude/commands/speckit.constitution.md`
   - 特点: 完整的双重机制示例

2. **tdd-cycle.md**
   - 位置: `/home/congyu/project/pyflow/.claude/commands/tdd-cycle.md`
   - 特点: 改造后的复杂工作流示例

### 相关文档

1. **skill-creator**: 创建和编辑 skills 的指导
2. **SKILL-IMPROVEMENT-PROPOSAL.md**: skill 改进方案
3. **PYTHON-PROJECT-SCHEDULER-USER-GUIDE.md**: skill 使用说明

---

## 🔄 持续改进

### 记录改造经验

每次改造后记录：
1. 遇到的问题
2. 解决方法
3. 改进建议
4. 最佳实践

### 更新指南

根据新经验：
1. 添加新的示例
2. 更新模板
3. 补充常见问题
4. 优化检查清单

---

**文档版本**: 1.0
**最后更新**: 2026-02-06
**维护者**: Claude Code
**状态**: ✅ 可用

---

## 附录: 快速参考

### 改造 5 步法

1. **分析**: 理解源文件结构
2. **添加**: YAML + User Input
3. **优化**: 标准化每个步骤
4. **更新**: Agent 格式
5. **验证**: 功能和结构

### 关键公式

```yaml
# Frontmatter 公式
---
description: [动作] + [功能] + [场景] + [保证]
handoffs:
  - label: [操作名]
    agent: [agent]
    prompt: [提示词]
---
```

```markdown
# 步骤公式
### [步骤名称]

**Agent**: `agent-type:agent-name`

**Prompt Template**:
```
[任务] for: $ARGUMENTS

Requirements:
- [要求]

Output: [输出]
```

**Validation**:
- [ ] [检查项]

**Output**: [输出]
```

### 验证公式

```markdown
# 检查清单公式
- [ ] 主流程完成
- [ ] 验证步骤齐全
- [ ] 格式统一
- [ ] 系统识别
```

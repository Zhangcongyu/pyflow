# Compliance Enforcement Rules

本文档详细说明如何确保 Constitution 和 Requirements 文档在整个项目执行过程中得到持续遵守。

---

## 核心原则

**两条红线，贯穿始终**：
1. **Constitution** (`./pjflow/constitution.md`) - 项目规则、原则、标准
2. **Requirements** (`./pjflow/requirements.md`) - 需求设计、技术方案

所有执行决策、代码实现、技术选择都必须符合这两个文档的要求。

---

## 执行流程中的合规检查

### Phase 开始前：文档读取

在每个 Phase 执行前，**必须**先读取相关文档：

```python
# Step 0: 读取核心文档（所有 Phase 通用）
constitution_content = Read("./pjflow/constitution.md")
requirements_content = Read("./pjflow/requirements.md")

# Phase 1 执行前：
# 已在 Phase 0 (brainstorming) 生成 requirements.md
# 确认需求文档存在后再执行

# Phase 4 (TDD) 执行前：
# 确保 constitution.md 已创建
# 确认 requirements.md 已创建（如果适用）
```

### Phase 执行中：实时遵守

#### Phase 1: Constitution 创建

- **输入**: 用户需求 + Constitution 模板
- **输出**: `./pjflow/constitution.md`
- **合规**: 填充模板，确保所有原则明确
- **验证**: 无遗留占位符 `[]`

#### Phase 2: 项目准备

- **输入**: Constitution 规则
- **输出**: 项目脚手架 + 配置
- **合规**:
  - 代码风格符合 Constitution 要求
  - 类型注解策略符合要求
  - 测试框架符合要求
- **验证**: 检查生成的配置文件

#### Phase 4: TDD 执行

**在 TDD 执行过程中，必须持续遵守**：

1. **RED 阶段** - 编写测试时：
   - 测试覆盖 Requirements 中的所有功能点
   - 测试用例反映 Constitution 的质量标准
   - 边界条件测试符合安全要求

2. **GREEN 阶段** - 实现功能时：
   - 代码风格符合 Constitution
   - 类型注解符合要求
   - 错误处理符合标准
   - 不添加需求范围外的功能

3. **REFACTOR 阶段** - 重构时：
   - 保持测试通过
   - 提升代码质量但仍符合 Constitution
   - 不违反设计原则

#### Phase 5: 质量审核

**必须验证合规性**：

```python
# Phase 5.2: 代码审核
Tool: pyflow-code-reviewer
Args: |
  验证项目合规性：
  1. 读取 ./pjflow/constitution.md，确认代码符合所有原则
  2. 读取 ./pjflow/requirements.md，确认实现了所有需求
  3. 列出违规项（如有）
  4. 提供修复建议
```

---

## 各 Phase 的合规验证规则

### Phase 1: 项目规则 (Constitution 创建)

**验证清单**:
- [ ] Constitution 文件已创建在 `./pjflow/constitution.md`
- [ ] 所有占位符 `[]` 已替换
- [ ] 版本号已正确设置
- [ ] 日期格式为 ISO YYYY-MM-DD
- [ ] 原则清晰、可测试

### Phase 0: 需求分析 (brainstorming)

**验证清单**:
- [ ] Requirements 文件已创建在 `./pjflow/requirements.md`
- [ ] 需求完整、明确
- [ ] 技术方案已定义
- [ ] 约束条件已记录

### Phase 4: TDD 执行

**每个子阶段验证**:

#### Phase 4.1: RED (生成测试)

```python
# 执行前检查
requirements = Read("./pjflow/requirements.md")
constitution = Read("./pjflow/constitution.md")

# 验证要点
assert "测试覆盖所有需求" in requirements
assert "测试覆盖类型注解要求" in constitution
```

**验证清单**:
- [ ] 测试用例覆盖 Requirements 中的所有功能
- [ ] 测试覆盖 Constitution 中的质量标准（类型注解、错误处理等）
- [ ] 测试文件结构符合项目标准

#### Phase 4.2: GREEN (实现功能)

**验证清单**:
- [ ] 实现的功能在 Requirements 范围内
- [ ] 代码风格符合 Constitution 要求
- [ ] 类型注解符合要求
- [ ] 错误处理符合标准
- [ ] 无需求外的功能蔓延

#### Phase 4.3: REFACTOR (重构代码)

**验证清单**:
- [ ] 重构未违反 Constitution 原则
- [ ] 测试仍然 100% 通过
- [ ] 代码质量提升但仍符合规范

### Phase 5: 质量审核

#### Phase 5.2: 代码审核

**合规验证必须包含**:

```markdown
## Code Review Report

### 1. Constitution 合规性

- [x] 代码风格符合 Constitution 要求
- [x] 类型注解符合标准
- [x] 错误处理符合规范
- [x] 测试覆盖符合要求
- [ ] 违规项：无（或列出具体违规）

### 2. Requirements 合规性

- [x] 所有已识别需求已实现
- [x] 技术方案符合设计
- [ ] 遗漏需求：无（或列出遗漏）

### 3. 质量标准

- [x] 代码可读性
- [x] 代码可维护性
- [x] 性能考虑
```

---

## 工具调用时的合规参数

### pyflow-tdd-cycle

```python
Skill(
    skill="pyflow-tdd-cycle",
    args="""
    执行 TDD 流程，遵守以下文档：
    1. Constitution: ./pjflow/constitution.md
    2. Requirements: ./pjflow/requirements.md

    在每个阶段（RED/GREEN/REFACTOR）都要验证合规性
    """
)
```

### pyflow-code-reviewer

```python
Task(
    subagent_type="pyflow-code-reviewer",
    subject="审核代码质量和文档合规性",
    activeForm="审核代码质量和文档合规性中",
    description="全面审核代码，验证是否符合 Constitution 和 Requirements",
    prompt="""
    请执行代码审核，重点验证：

    1. Constitution 合规性
       - 读取 ./pjflow/constitution.md
       - 验证代码风格、类型注解、错误处理等是否符合要求
       - 列出所有违规项

    2. Requirements 合规性
       - 读取 ./pjflow/requirements.md
       - 验证所有需求是否已实现
       - 确认无功能蔓延

    3. 质量标准
       - 代码可读性、可维护性
       - 测试覆盖率
       - 性能考虑

    输出包含违规项和修复建议的报告
    """
)
```

### pyflow-python-pro

```python
Task(
    subagent_type="pyflow-python-pro",
    subject="实现功能并遵守项目规则",
    activeForm="实现功能并遵守项目规则中",
    description="根据测试实现功能，同时遵守 Constitution 和 Requirements",
    prompt="""
    请实现测试中定义的功能，严格遵守：

    1. 读取 ./pjflow/constitution.md
       - 遵循代码风格要求
       - 添加类型注解
       - 实现适当的错误处理

    2. 读取 ./pjflow/requirements.md
       - 仅实现需求范围内的功能
       - 按照技术方案实现
       - 不添加额外功能

    3. 确保所有测试通过
    """
)
```

---

## projectflow-executor 执行流程中的合规检查

### 修改后的执行流程

```
读取 ./pjflow/task_plan.md
   ↓
找到下一个 pending 的 Phase
   ↓
【新增】Step 0: 读取合规文档
   - 读取 ./pjflow/constitution.md
   - 读取 ./pjflow/requirements.md（如果存在）
   ↓
解析 Phase 信息
   ↓
标记 Phase 为 in_progress
   ↓
【新增】验证前置条件
   - 如果 Phase > 1，确认 constitution.md 已存在
   - 如果 Phase >= 4，确认 requirements.md 已存在（对于新项目）
   ↓
调用 Tool（带入文档上下文）
   ↓
【新增】验证输出合规性
   - 检查输出是否符合 Constitution 要求
   - 检查输出是否符合 Requirements（如适用）
   ↓
更新 CHECKLIST.md
   - 添加合规性检查项
   ↓
更新 ./pjflow/progress.md
   - 记录合规性验证结果
   ↓
标记 Phase 为 complete
   ↓
下一个 Phase
```

### 每个 Phase 的验证规则

| Phase | 前置条件 | 输出验证 | CHECKLIST 添加项 |
|-------|---------|---------|----------------|
| Phase 0 | - | requirements.md 已创建 | Requirements 已验证 |
| Phase 1 | - | constitution.md 已创建，无占位符 | Constitution 已验证 |
| Phase 2 | Phase 1 完成 | 项目配置符合 Constitution | 配置合规验证 |
| Phase 4.1 | Phase 0, Phase 1 完成 | 测试覆盖 Requirements | 测试覆盖验证 |
| Phase 4.2 | Phase 4.1 完成 | 代码符合 Constitution | 代码合规验证 |
| Phase 4.3 | Phase 4.2 完成 | 重构仍符合 Constitution | 重构合规验证 |
| Phase 5.2 | Phase 4 完成 | 全面合规性审核 | 合规性审核完成 |

---

## 合规性检查清单模板

### Phase 4.2: GREEN 阶段完成验证

```markdown
## Compliance Check - Phase 4.2: GREEN

### Constitution 验证
- [ ] 代码风格符合（检查 pyproject.toml 或 ruff.toml）
- [ ] 类型注解覆盖率 >= X%
- [ ] 错误处理符合标准
- [ ] 日志记录符合要求（如需要）
- [ ] 无禁止的模式（如硬编码路径等）

### Requirements 验证
- [ ] 所有已实现功能在 Requirements 中有对应
- [ ] 无超出需求范围的实现
- [ ] 技术选型符合设计方案

### 测试验证
- [ ] 所有测试通过
- [ ] 测试覆盖率符合要求
```

### Phase 5.2: 代码审核合规性报告

```markdown
## Compliance Report

### Constitution 合规性分析

**检查项目**:
1. 代码风格
2. 类型注解
3. 错误处理
4. 测试覆盖
5. 文档注释

**结果**: ✅ 合格 / ⚠️ 部分违规 / ❌ 不合格

**违规详情**:
- 列出具体违规项
- 提供修复建议

### Requirements 合规性分析

**检查项目**:
1. 功能完整性
2. 技术方案符合度
3. 约束条件遵守

**结果**: ✅ 合格 / ⚠️ 部分遗漏 / ❌ 严重遗漏

**遗漏详情**:
- 列出未实现的需求
- 提供补充建议
```

---

## 不合规处理流程

### 发现违规时的处理

1. **记录违规**: 在 progress.md 中记录具体违规项
2. **标记 Phase**: 将 Phase 标记为 `Status: failed`
3. **提供修复建议**: 详细说明如何修复
4. **询问用户**:
   - "发现 X 项违规，是否需要立即修复？"
   - "选项 A: 立即修复，选项 B: 记录并继续，选项 C: 跳过此验证"

### 修复后重新验证

```python
# 修复完成后，重新验证
Edit(
    file_path="./pjflow/progress.md",
    old_string="**Status**: failed",
    new_string="**Status**: fixed\n**重新验证**: ✅ 合规"
)
```

---

**文档版本**: 1.0.0
**创建时间**: 2026-02-11
**用途**: ProjectFlow 合规性强制执行规则

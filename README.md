# ProjectFlow

[English](#english) | [中文](#中文)

---

<a name="english"></a>
## English

ProjectFlow is an automated project development orchestration pipeline consisting of three core skills:

```
projectflow-router → projectflow-planner → projectflow-executor
```

### Overview

ProjectFlow automates the complete development workflow from initial request to implementation:

| Component | Role | Description |
|-----------|------|-------------|
| **projectflow-router** | Detector | Detects project attributes (new/old + complexity + language) and routes to planner |
| **projectflow-planner** | Planner | Generates executable task plans based on project environment and templates |
| **projectflow-executor** | Executor | Executes plans phase by phase with compliance checking |

### Three-Dimensional Detection

ProjectFlow analyzes projects along three dimensions:

1. **Project Status**: New project (`--new`) vs. Feature addition to existing project (`--add-feature`)
2. **Complexity**: Simple (`--simple`) vs. Medium (`--medium`) vs. Complex (`--complex`)
3. **Language**: Python vs. TypeScript vs. Go

### Decision Priority

ProjectFlow follows a priority-based detection strategy:

```
User explicit parameters > User explicit description > Keyword matching > Technical analysis > Default
```

**When users explicitly specify complexity, their choice takes priority over auto-detection.**

### Workflow

```
User Request
    ↓
┌─────────────────────────────────────┐
│ 1. Router: Detect Attributes        │
│    - Check for explicit parameters  │
│    - Auto-detect if unspecified     │
│    - Show detection rationale       │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 2. User Confirmation               │
│    - Review detected attributes     │
│    - Adjust if needed               │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 3. Planner: Generate Plan          │
│    - Read environment context       │
│    - Load appropriate templates     │
│    - Generate task_plan.md          │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 4. Executor: Implement             │
│    - Execute phase by phase         │
│    - Update progress.md             │
│    - Run compliance checks          │
│    - Update CHECKLIST.md            │
└─────────────────────────────────────┘
```

### Usage Example

```
User: "Create a simple file counter CLI tool in Python"

Router Detection:
• Project Status: New project (--new) [User said "create"]
• Complexity: Simple (--simple) [Keyword: "tool"]
• Language: Python (--python) [User specified]

Confirmation: ✓

Planner: Generates task_plan.md with appropriate phases

Executor: Implements with 90%+ test coverage
```

### Project Constitution

All projects managed by ProjectFlow follow core principles:

- **TYPE_SAFETY_AND_CODE_QUALITY** - Type annotations, strict checking
- **TEST_DRIVEN_DEVELOPMENT** - 90%+ test coverage required
- **SIMPLICITY** - Simple solutions preferred

### Version History

| Version | Date | Changes |
|---------|------|---------|
| 5.0.0 | 2026-02-24 | Added user priority principle, interactive confirmation |
| 4.0.0 | 2026-02-11 | Initial stable release |

### File Structure

```
.claude/skills/
├── projectflow-router/
│   ├── SKILL.md                    # Main skill definition
│   └── references/
│       ├── detection-criteria.md   # Detailed detection rules
│       └── routing-table.md        # Parameter combinations
├── projectflow-planner/
│   ├── SKILL.md
│   └── references/
│       ├── VERSION_NAMING.md
│       ├── ENVIRONMENT_FIELDS.md
│       └── EXECUTION_GUIDE.md
└── projectflow-executor/
    ├── SKILL.md
    └── references/
        └── requirements-compliance.md

pjflow/
└── versioned/
    └── {version_name}/
        ├── task_plan.md           # Generated task plan
        ├── requirements.md        # Versioned requirements
        ├── CHECKLIST.md          # Progress tracking
        ├── progress.md           # Detailed progress log
        └── compliance_report.md  # Compliance check results
```

---

<a name="中文"></a>
## 中文

ProjectFlow 是一个自动化项目开发编排流水线，由三个核心 skill 组成：

```
projectflow-router → projectflow-planner → projectflow-executor
```

### 概述

ProjectFlow 自动化从初始请求到实现的完整开发工作流：

| 组件 | 角色 | 描述 |
|------|------|------|
| **projectflow-router** | 检测器 | 检测项目属性（新/老 + 复杂度 + 语言）并路由到规划器 |
| **projectflow-planner** | 规划器 | 根据项目环境和模板生成可执行的任务计划 |
| **projectflow-executor** | 执行器 | 逐阶段执行计划并进行合规检查 |

### 三维检测

ProjectFlow 沿三个维度分析项目：

1. **项目状态**: 新项目 (`--new`) vs. 老项目添加功能 (`--add-feature`)
2. **复杂度**: 简单 (`--simple`) vs. 中等 (`--medium`) vs. 复杂 (`--complex`)
3. **语言**: Python vs. TypeScript vs. Go

### 判断优先级

ProjectFlow 遵循基于优先级的检测策略：

```
用户明确参数 > 用户明确描述 > 关键词匹配 > 技术分析 > 默认值
```

**当用户明确指定复杂度时，其选择优先于自动检测。**

### 工作流程

```
用户请求
    ↓
┌─────────────────────────────────────┐
│ 1. Router: 检测属性                │
│    - 检查明确参数                  │
│    - 未指定时自动检测              │
│    - 展示判断依据                  │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 2. 用户确认                        │
│    - 审查检测到的属性              │
│    - 需要时进行调整                │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 3. Planner: 生成计划               │
│    - 读取环境上下文                │
│    - 加载适当模板                  │
│    - 生成 task_plan.md              │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 4. Executor: 执行实现              │
│    - 逐阶段执行                    │
│    - 更新 progress.md               │
│    - 运行合规检查                  │
│    - 更新 CHECKLIST.md              │
└─────────────────────────────────────┘
```

### 使用示例

```
用户: "用 Python 创建一个简单的文件计数器 CLI 工具"

Router 检测:
• 项目状态: 新项目 (--new) [用户说"创建"]
• 复杂度: 简单 (--simple) [关键词: "工具"]
• 语言: Python (--python) [用户指定]

确认: ✓

Planner: 生成包含适当阶段的 task_plan.md

Executor: 实现并达到 90%+ 测试覆盖率
```

### 项目宪法

所有由 ProjectFlow 管理的项目遵循核心原则：

- **TYPE_SAFETY_AND_CODE_QUALITY** - 类型注解，严格检查
- **TEST_DRIVEN_DEVELOPMENT** - 要求 90%+ 测试覆盖率
- **SIMPLICITY** - 优先采用简单解决方案

### 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 5.0.0 | 2026-02-24 | 添加用户优先原则，交互式确认 |
| 4.0.0 | 2026-02-11 | 初始稳定版本 |

### 文件结构

```
.claude/skills/
├── projectflow-router/
│   ├── SKILL.md                    # 主技能定义
│   └── references/
│       ├── detection-criteria.md   # 详细检测规则
│       └── routing-table.md        # 参数组合
├── projectflow-planner/
│   ├── SKILL.md
│   └── references/
│       ├── VERSION_NAMING.md
│       ├── ENVIRONMENT_FIELDS.md
│       └── EXECUTION_GUIDE.md
└── projectflow-executor/
    ├── SKILL.md
    └── references/
        └── requirements-compliance.md

pjflow/
└── versioned/
    └── {版本名称}/
        ├── task_plan.md           # 生成的任务计划
        ├── requirements.md        # 版本化需求
        ├── CHECKLIST.md          # 进度跟踪
        ├── progress.md           # 详细进度日志
        └── compliance_report.md  # 合规检查结果
```

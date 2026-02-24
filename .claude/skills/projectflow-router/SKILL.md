---
name: projectflow-router
description: |
  三维检测器，检测项目属性（新/老 + 简单/中等/复杂 + 语言）并路由到 projectflow-planner。
  触发条件: 用户请求项目开发、创建应用、添加功能
  接收参数: --new/--add-feature + --simple/--medium/--complex + --python/--typescript/--go + 用户原始请求
  核心职责: 纯检测器，只负责参数传递和路由，不执行任何实现工作
---

# ProjectFlow Router

## 职责

检测项目三维属性并路由到 projectflow-planner：

1. **项目状态**: 新项目 (--new) vs 老项目新增功能 (--add-feature)
2. **项目复杂度**: 简单 (--simple) vs 中等 (--medium) vs 复杂 (--complex)
3. **语言类型**: Python (--python) vs TypeScript (--typescript) vs Go (--go)

## 执行流程

```
用户请求 → 解析明确参数 → 自动检测缺失参数 → 展示结果 → 用户确认 → 调用 planner
```

## 判断优先级

### 核心原则：用户明确指定优先

| 优先级 | 判断方式 | 示例 |
|--------|----------|------|
| **最高** | 用户明确参数 | `--simple`, `--medium`, `--complex` |
| **高** | 用户明确描述 | "这是一个简单项目", "做中等的API" |
| **中** | 关键词匹配 | "工具"→简单, "平台"→复杂, "API"→中等 |
| **低** | 技术特征推断 | 代码量、架构复杂度分析 |
| **默认** | 无依据时默认 | `--medium`, `--python` |

**当用户明确指定复杂度时，直接使用用户指定值，不进行自动检测覆盖。**

## 检测规则

### 维度 1: 项目类型（新 vs 老）

**新项目信号**: "创建"、"新建"、"build from scratch"

**老项目信号**: "添加"、"新增"、"extend"、"add feature"

### 维度 2: 项目复杂度

**Step 1**: 检查用户明确指定
- 参数形式: `--simple`, `--medium`, `--complex`
- 明确描述: "简单项目", "中等规模", "复杂系统"

**Step 2**: 无明确指定时，使用关键词匹配
- **简单**: "简单"、"小的"、"quick"、"单个功能"、"工具"、"utility"
- **中等**: "中等"、"几个功能"、"API"、"CRUD"、"数据处理"、"service"
- **复杂**: "复杂"、"大型的"、"完整系统"、"平台"、"框架"、"高性能"、"分布式"

### 维度 3: 语言类型

| 触发关键词 | 参数 | 配置文件 |
|-----------|------|----------|
| Python, FastAPI, Django | `--python` | `pyproject.toml` |
| TypeScript, React, Node.js | `--typescript` | `package.json` |
| Go, Golang, Gin | `--go` | `go.mod` |

**默认**: 未明确指定时使用 `--python`

## 用户交互与确认

检测完成后，使用 **AskUserQuestion** 工具展示结果并请求确认。

### 交互示例

```
检测到项目属性:

• 项目类型: 新项目 (--new)  [依据: 用户说"创建"]
• 复杂度: 简单 (--simple)    [依据: 关键词"工具"]
• 语言: Python (--python)    [依据: 默认]

检测是否正确？
- 是，继续执行
- 否，修正参数
```

### 确认后调用

使用 **Skill 工具**传递最终确认的参数给 projectflow-planner：

```python
Skill(skill="projectflow-planner", args="--new --simple --python 用户原始需求")
```

## 路由表

详见 [references/routing-table.md](references/routing-table.md) 获取完整的参数组合和调用示例。

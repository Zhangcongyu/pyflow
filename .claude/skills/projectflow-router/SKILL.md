---
name: projectflow-router
description: |
  三维检测器，检测项目属性（新/老 + 简单/中等/复杂 + 语言）并路由到 projectflow-planner。
  触发条件: 用户请求项目开发、创建应用、添加功能
  接收参数: --new/--add-feature + --simple/--medium/--complex + --python/--typescript/--go + 用户原始请求
  核心职责: 纯检测器，只负责参数传递和路由，不执行任何实现工作
---

# Projectflow Router

## 职责

检测项目三维属性并路由到 projectflow-planner：

1. **项目状态**: 新项目 (--new) vs 老项目新增功能 (--add-feature)
2. **项目复杂度**: 简单 (--simple) vs 中等 (--medium) vs 复杂 (--complex)
3. **语言类型**: Python (--python) vs TypeScript (--typescript) vs Go (--go)

## 执行流程

```
用户请求 → 检测三维参数 → 调用 projectflow-planner
```

## 检测规则

### 维度 1: 项目类型（新 vs 老）

**新项目信号**: "创建"、"新建"、"build from scratch"、目录为空、无项目配置文件

**老项目信号**: "添加"、"新增"、"extend"、"add feature"、存在项目配置文件

### 维度 2: 项目复杂度

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

## 调用方式

使用 **Skill 工具**传递检测到的参数给 projectflow-planner：

```
Skill(skill="projectflow-planner", args="--new --simple --python 用户原始需求")
```

## 路由示例

详见 [references/routing-table.md](references/routing-table.md) 获取完整的参数组合和调用示例。

---

**版本**: 4.0.0
**用途**: ProjectFlow Router - 三维检测器（语言无关）

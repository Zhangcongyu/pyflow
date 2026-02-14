# Detection Criteria

## 详细检测标准

本文档提供 projectflow-router 三维检测的详细标准和示例。

---

## 维度 1: 项目状态检测

### 新项目 (--new)

**检测标准**:
1. 用户明确表达"创建"、"新建"意图
2. 当前目录为空或没有项目配置文件
3. 不存在项目基础设施（pyproject.toml, package.json 等）

**用户语言示例**:
```
"创建一个 FastAPI 应用"
"新建一个待办事项项目"
"从零开始构建一个工具"
"初始化一个新的项目"
"build from scratch"
"start a new project"
```

**技术检测命令**:
```bash
# Python 项目检测
test -f pyproject.toml || test -f setup.py || test -f requirements.txt

# TypeScript/Node 项目检测
test -f package.json || test -f tsconfig.json

# Go 项目检测
test -f go.mod
```

**判断逻辑**:
- 如果用户说"创建" + 目录为空 → **新项目**
- 如果用户说"创建" + 有配置文件 → **询问用户**："当前目录已有项目，是创建新项目还是在现有项目添加功能？"

---

### 老项目 (--add-feature)

**检测标准**:
1. 用户明确表达"添加"、"新增"意图
2. 当前目录存在项目配置文件
3. 用户提到"在现有项目..."或"在当前项目..."

**用户语言示例**:
```
"添加一个用户认证功能"
"在现有项目添加 API 接口"
"extend the application with..."
"add feature to..."
"在当前项目添加..."
```

**技术检测命令**:
```bash
# 检查项目文件是否存在
test -f pyproject.toml && echo "Existing Python project"
test -f package.json && echo "Existing Node project"
test -f go.mod && echo "Existing Go project"
```

**判断逻辑**:
- 如果用户说"添加" + 有配置文件 → **老项目**
- 如果用户说"添加" + 目录为空 → **询问用户**："当前目录为空，是否需要先创建项目？"

---

## 维度 2: 项目复杂度检测

### 简单项目 (--simple)

**特征**:
- 预估代码量: < 300 LOC
- 单一功能或少量相关功能
- 无需复杂架构设计
- 需求明确，无需深入分析

**用户语言示例**:
```
"创建一个简单的待办事项 CLI"
"写一个小的文件转换工具"
"一个简单的脚本"
"quick utility"
"简单工具"
```

**技术特征**:
- 单一模块或文件
- 无数据库或简单文件存储
- 无复杂依赖关系
- 同步执行（无异步）

**典型场景**:
- CLI 工具（单个命令）
- 文件处理脚本
- 简单的数据转换工具
- 单一功能的 API

---

### 中等项目 (--medium)

**特征**:
- 预估代码量: 300-1000 LOC
- 多个相关功能
- 需要一定架构设计
- 可能需要数据库

**用户语言示例**:
```
"创建一个 FastAPI CRUD 应用"
"添加用户认证和数据管理"
"数据处理 service"
"几个相关功能"
"中等规模的应用"
```

**技术特征**:
- 多模块设计
- 数据库集成（SQLite, PostgreSQL）
- API 接口（RESTful）
- 配置管理
- 测试覆盖

**典型场景**:
- RESTful API 服务
- CRUD 应用
- 数据处理 pipeline
- Web 应用（基础）

---

### 复杂项目 (--complex)

**特征**:
- 预估代码量: > 1000 LOC
- 多模块/微服务架构
- 高性能要求
- 需要详细架构设计

**用户语言示例**:
```
"创建一个高并发异步平台"
"构建完整的微服务系统"
"分布式任务处理框架"
"复杂的企业级应用"
"高性能系统"
```

**技术特征**:
- 异步编程（asyncio, concurrent）
- 微服务架构
- 消息队列（Redis, RabbitMQ）
- 分布式系统
- 高性能优化
- 安全认证（OAuth, JWT）
- 监控和日志

**典型场景**:
- 分布式任务处理平台
- 实时数据流处理
- 微服务架构
- 高并发 API 网关
- 企业级应用

---

## 维度 3: 语言类型检测

### Python (--python)

**触发关键词**:
- Python, python3, py
- FastAPI, Django, Flask, Tornado
- asyncio, aiohttp
- SQLAlchemy, Django ORM
- pytest, unittest
- pyproject.toml, setup.py, requirements.txt

**示例请求**:
```
"创建一个 FastAPI 应用"
"使用 Django 构建网站"
"Python 异步任务处理"
"pytest 测试框架"
```

---

### TypeScript (--typescript)

**触发关键词**:
- TypeScript, JavaScript, Node.js, TS
- Express, NestJS, Koa
- React, Next.js, Vue, Angular
- package.json, tsconfig.json
- npm, yarn, pnpm

**示例请求**:
```
"创建一个 Express API"
"使用 React 构建前端"
"Next.js 全栈应用"
"Node.js 服务"
```

---

### Go (--go)

**触发关键词**:
- Go, Golang
- Gin, Echo, Fiber
- Gorm, sqlx
- go.mod, go.sum

**示例请求**:
```
"创建一个 Gin API"
"Go 微服务"
"Golang 并发处理"
```

---

## 检测流程图

```
用户请求
   ↓
┌─────────────────────────────┐
│ Step 1: 检测项目状态        │
├─────────────────────────────┤
│ 用户说"创建"？              │
│  ├─ 是 → 检查目录          │
│  │   ├─ 空 → --new         │
│  │   └─ 有文件 → 询问      │
│  └─ 否 → 用户说"添加"？    │
│      ├─ 是 → --add-feature  │
│      └─ 否 → 默认 --new     │
└─────────────────────────────┘
   ↓
┌─────────────────────────────┐
│ Step 2: 检测复杂度          │
├─────────────────────────────┤
│ 关键词匹配：                │
│ "简单"、"小的" → --simple   │
│ "API"、"CRUD" → --medium    │
│ "平台"、"系统" → --complex  │
│ 无明确关键词 → 默认 --medium │
└─────────────────────────────┘
   ↓
┌─────────────────────────────┐
│ Step 3: 检测语言类型        │
├─────────────────────────────┤
│ 技术关键词匹配：            │
│ "Python"、"FastAPI" → --python     │
│ "TypeScript"、"Node.js" → --typescript │
│ "Go"、"Golang" → --go       │
│ 无明确关键词 → 默认 --python │
└─────────────────────────────┘
   ↓
输出: 三维参数组合
```

---

## 常见场景示例

### 场景 1: 简单 CLI 工具

**输入**: "创建一个简单的待办事项 CLI 工具"

**检测过程**:
1. "创建" → --new
2. "简单的"、"CLI" → --simple
3. 无语言关键词 → 默认 --python

**输出**: `--new --simple --python`

---

### 场景 2: FastAPI CRUD 应用

**输入**: "创建一个 FastAPI 用户管理 API，包含增删改查功能"

**检测过程**:
1. "创建" → --new
2. "API"、"CRUD"、"多个功能" → --medium
3. "FastAPI" → --python

**输出**: `--new --medium --python`

---

### 场景 3: 现有项目添加认证

**输入**: "在当前项目添加用户认证功能"

**检测过程**:
1. "添加" → --add-feature
2. "认证"（通常中等复杂）→ --medium
3. 检测当前目录语言 → 假设是 Python

**输出**: `--add-feature --medium --python`

---

### 场景 4: 高性能异步平台

**输入**: "构建一个高并发的异步任务处理平台，使用 Python"

**检测过程**:
1. "构建" → --new
2. "高并发"、"平台"、"异步" → --complex
3. "Python" → --python

**输出**: `--new --complex --python`

---

## 边界情况处理

### 情况 1: 用户请求模糊

**输入**: "做一个项目"

**处理**: 使用 AskUserQuestion 工具询问：
1. 是创建新项目还是在现有项目添加功能？
2. 项目的主要功能是什么？（用于判断复杂度）
3. 使用什么语言？

### 情况 2: 检测冲突

**输入**: "创建一个简单的平台"

**处理**: "简单"和"平台"矛盾
- 优先级: **复杂 > 中等 > 简单**
- 结果: --complex（因为"平台"更具体）

### 情况 3: 目录状态与用户意图不符

**输入**: "创建新项目"（但目录有 pyproject.toml）

**处理**: 询问用户：
"检测到当前目录已有 Python 项目，是否要：
1. 创建新项目（需要切换目录）
2. 在现有项目添加功能"

---

## 检测最佳实践

1. **信任用户的明确表达**
   - 用户说"简单"就是简单，即使技术特征显示中等

2. **关键词优先级**
   - 复杂度关键词 > 技术特征 > 默认值
   - 项目状态关键词 > 目录检测

3. **语言检测多样化**
   - 技术关键词（FastAPI）
   - 文件扩展名（.py, .ts）
   - 配置文件（pyproject.toml, package.json）

4. **不确定时询问**
   - 避免猜测导致错误
   - 使用 AskUserQuestion 工具

---

**文档版本**: 1.0.0
**最后更新**: 2026-02-11

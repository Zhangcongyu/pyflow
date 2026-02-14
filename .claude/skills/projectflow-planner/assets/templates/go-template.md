# Go 项目计划模板

**说明**: Go 项目基础模板（保持简化的结构），详细内容请参考 Python 模板

**适用语言**: Go (go.mod)

---

## 模板变量

| 变量 | 说明 | 示例值 |
|--------|------|----------|
| `{{GOAL}}` | 用户原始需求 | "创建一个高性能的 Go 微服务平台" |
| `{{PROJECT_STATUS}}` | new / add-feature | new |
| `{{COMPLEXITY}}` | simple / medium / complex | simple |
| `{{VERSION_DIR}}` | 版本目录名称 | v0_initial |

---

## Phase 0: 需求互动

**适用场景**: `{{COMPLEXITY}}` == medium 或 complex

**Tool**: pyflow-brainstorming

**执行**: 探索用户需求

**CHECKLIST**:
- [ ] 需求分析完成

---

## Phase 1: 项目规则

**适用场景**: `{{PROJECT_STATUS}}` == new

**Tool**: pyflow-constitution

**执行**: 创建项目宪法文档 `pjflow/constitution.md`

**CHECKLIST**:
- [ ] Constitution 创建/更新

**Skip if**: 老项目

---

## Phase 2: 项目构建

**适用场景**: `{{PROJECT_STATUS}}` == new

### 2.0 干扰检测与清理

**Tool**: Bash + 用户确认

**执行**: 检测冲突目录并清理（参考 Python 模板）

---

### 2.1 Git 仓库

**Tool**: Bash

**执行**: 初始化 Go module（参考 Python 模板）

---

### 2.2 虚拟环境

**Tool**: Bash

**执行**: Go module 自动下载依赖

---

### 2.3 项目架构

**Tool**: Write / Bash

**项目类型**:

| 类型 | 目录结构 |
|------|-----------|
| **cli** | cmd/ + internal/ |
| **web** | cmd/server/ + internal/ + pkg/ |
| **library** | internal/ + pkg/ |

---

### 2.4 系统文件

**Tool**: Write

**go.mod** (参考 Python 模板中的系统文件配置)

---

### 2.5 项目文件

**Tool**: Write

**原则**: 创建空占位文件，不编写业务逻辑

---

## Phase 3: 工作树准备（老项目）

**适用场景**: `{{PROJECT_STATUS}}` == add-feature

### 3.1 Git 分支管理

**Tool**: Bash

**执行**: 创建并切换到 feature 分支

---

### 3.2 依赖管理

**Tool**: Bash

**执行**: go get 添加新功能依赖

---

### 3.3 系统文件更新

**Tool**: Edit

**执行**: 更新 README.md 和版本号

---

### 3.4 新功能文件创建

**Tool**: Write

**原则**: 创建空占位文件

---

## Phase 4: TDD 执行

**适用场景**: 所有项目

**🚨 强制要求**:
- **严禁手动创建业务代码文件**
- **严禁手动编写业务逻辑代码**
- 必须使用 TDD 工具完成所有编码工作

### Simple/Medium 项目

**Tool**: TBD (Go TDD 工具)

**执行**: TDD 流程（RED → GREEN → REFACTOR）

---

## Phase 5: 质量审核

**适用场景**: 所有项目

### 5.1 质量检查

**Tool**: Bash

**执行**:
```bash
go test ./...
go build ./...
```

---

## CHECKLIST 模板

（参考 Python 模板中的 CHECKLIST 部分）

---

**版本**: 1.0.0
**用途**: ProjectFlow Planner - Go 基础计划模板
**状态**: 基础结构（待完善）

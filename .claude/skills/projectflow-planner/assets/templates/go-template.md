# Go 项目完整计划模板

**说明**: 此模板包含 Go 项目所有 Phase 的框架。Planner 读取此模板生成 task_plan.md，Executor 根据计划执行。

---

## 模板变量

| 变量 | 说明 | 示例值 |
|--------|------|----------|
| `{{GOAL}}` | 用户原始需求 | "创建一个高性能的 Go 微服务平台" |
| `{{PROJECT_STATUS}}` | new / add-feature | new |
| `{{COMPLEXITY}}` | simple / medium / complex | medium |
| `{{VERSION_DIR}}` | 版本目录名称 | v0_initial / v1_add_feature |

**说明**: 其他如项目名称、模块路径等均为示例值，Executor 执行时根据当前目录和需求自动填充。Go 模块路径可以是 GitHub 路径（`github.com/user/repo`）或本地路径（`./myapp`）。

---

## 文档注入标准格式（Phase 4/5 必须遵守）

**重要**: Phase 4/5 所有子阶段必须使用以下格式注入文档上下文。

**标准格式**:
```go
// 读取文档
constitution := Read("./pjflow/constitution.md")
requirements := Read("./pjflow/{VERSION_DIR}//requirements.md")

// 构建增强提示
enhancedArgs := fmt.Sprintf("%s

## 🚨 强制约束（必须遵守）

### 项目宪法 (Constitution)
%s

### 需求文档 (Requirements)
%s

**重要**: 违反上述约束的代码将被拒绝！必须确保所有代码符合宪法要求和需求范围。
", originalPrompt, constitution, requirements)
```

**强制要求**:
1. **全文注入**: 必须读取完整文档内容，禁止手动总结
2. **三步骤执行**: 前置检查 → 文档注入 → 后置验证
3. **路径规范**:
   - 宪法: `./pjflow/constitution.md`
   - 需求: `./pjflow/{VERSION_DIR}/requirements.md`

---

## Phase 0: 需求互动

### Phase 0.0: 需求探索

**适用场景**: `{{COMPLEXITY}}` == medium 或 complex

**执行顺序**: 优先执行

**状态**: pending

**Tool**: pyflow-brainstorming

**参数**: `--version-dir {{VERSION_DIR}} {{GOAL}}`

**目标**: 探索用户需求，明确功能边界，输出版本化需求文档

**输出位置**: `pjflow/{{VERSION_DIR}}/requirements.md`

**CHECKLIST**:
- [ ] 需求分析完成
- [ ] 功能边界明确
- [ ] 技术方案确认
- [ ] 需求文档已创建

**Skip if**: `{{COMPLEXITY}}` == simple

---

### Phase 0.1: 简单项目需求文档生成

**适用场景**: `{{PROJECT_STATUS}}` == new 且 `{{COMPLEXITY}}` == simple

**执行顺序**: 优先执行（在 Phase 1 之前）

**Tool**: Write

**目标**: 生成简单项目的需求文档模板

**内容**:
\`\`\`
Write(
    file_path="pjflow/{{VERSION_DIR}}/requirements.md",
    content="""# Requirements

**Project Type**: {{PROJECT_STATUS}}
**Complexity**: simple
**Goal**: {{GOAL}}

---

## Project Overview

{{GOAL}}

## Core Features

### Feature 1
- Description:
- Acceptance Criteria:
- Priority:

### Feature 2
- Description:
- Acceptance Criteria:
- Priority:

## Project Architecture

### 目录结构

\`\`\`
{{PROJECT_NAME}}/
├── cmd/
│   └── {{PROJECT_NAME}}/
│       └── main.go
├── internal/
│   ├── cli/
│   └── core/
├── go.mod
├── go.sum
└── README.md
\`\`\`

### 技术栈

- **语言**: Go 1.21+
- **CLI 框架**: cobra /urfave/cli
- **测试框架**: 标准库 testing + testify

### 模块划分

| 模块 | 目录 | 职责 |
|------|------|------|
| CLI | cmd/{{PROJECT_NAME}} | 命令行入口 |
| CLI Logic | internal/cli | CLI 逻辑处理 |
| Core | internal/core | 核心业务逻辑 |

## Technical Requirements

- Performance requirements:
- Security requirements:
- Compatibility requirements:

## Success Criteria

1.
2.
3.

---
*Created: {{PROJECT_STATUS}} - simple*
"""
)
```

**输出位置**: `pjflow/{{VERSION_DIR}}/requirements.md`

**CHECKLIST**:
- [ ] 需求文档模板已创建
- [ ] 输出路径正确

**Skip if**: `{{COMPLEXITY}}` == medium 或 complex

---

## Phase 1: 项目规则

**适用场景**: `{{PROJECT_STATUS}}` == new

**Tool**: pyflow-constitution

**执行**: 创建项目宪法文档 `pjflow/constitution.md`

**CHECKLIST**:
- [ ] Constitution 创建/更新
- [ ] 项目规则定义
- [ ] 共享文档已创建

**后置步骤**: 验证宪法文档创建
```bash
# 确认宪法文档已创建
ls -la pjflow/constitution.md
```

**Skip if**: 老项目（`{{PROJECT_STATUS}}` == add-feature）

---

## Phase 2: 项目构建

**适用场景**: `{{PROJECT_STATUS}}` == new

### 2.0 干扰检测与清理

**Tool**: Bash + 用户确认

**检测逻辑**:
```bash
# 检测是否存在冲突目录
CONFLICT_DIRS="cmd internal pkg vendor"
CONFLICT_FILES="go.mod go.sum"

for dir in $CONFLICT_DIRS; do
    if [ -d "$dir" ]; then
        HAS_CONFLICT=true
        break
    fi
done

if [ "$HAS_CONFLICT" = true ]; then
    # 使用 AskUserQuestion 询问用户
    问题："检测到目录中已存在项目文件 (cmd/, internal/ 等)，是否删除并重新创建？"
    选项：
      - "是，删除并重新创建"
      - "否，取消操作"

    # 根据用户选择执行
fi
```

**CHECKLIST**:
- [ ] 冲突检测完成
- [ ] 用户确认
- [ ] 清理命令准备
- [ ] 目录已清理（如需要）

---

### 2.1 Git 仓库

**Tool**: Bash

**前置检测**:
- Git 是否已存在
- 当前分支名称

**判断逻辑**:
```bash
# 检查 Git 是否已初始化
if git rev-parse --git-dir > /dev/null 2>&1; then
    GIT_EXISTS=true
else
    GIT_EXISTS=false
fi

echo "Git 仓库状态: $GIT_EXISTS"
```

**执行**:
```bash
# 如果未初始化
if [ "$GIT_EXISTS" = false ]; then
    git init
    git branch -M main
    echo "Git 仓库已初始化"
fi

# 创建 .gitignore
cat > .gitignore << 'EOF'
# Binaries
*.exe
*.exe~
*.dll
*.so
*.dylib
/bin/
/

# Test binary
*.test

# Output of the go coverage tool
*.out
coverage.html

# Dependency directories
vendor/

# Go workspace file
go.work

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
EOF
```

**CHECKLIST**:
- [ ] Git 仓库初始化/确认
- [ ] .gitignore 创建

---

### 2.2 项目架构

**Tool**: Write / Bash

**项目类型判断**:

根据用户需求关键词和环境检测，选择项目架构：

| 关键词 | 项目类型 | 目录结构 | 专用 Agent |
|--------|----------|----------|------------|
| CLI, 命令行, 工具 | **cli** | cmd/ + internal/ | pyflow-go-pro |
| Library, 库, SDK | **library** | internal/ + pkg/ | pyflow-go-pro |
| Web, API, Server | **web** | cmd/server/ + internal/ + pkg/ | pyflow-go-pro |
| Microservice, 微服务 | **microservice** | cmd/ + internal/ + pkg/ | pyflow-go-pro |

**CLI 架构** (simple/medium):
```
project-name/
├── cmd/
│   └── project-name/
│       └── main.go
├── internal/
│   ├── cli/
│   │   ├── root.go
│   │   ├── add.go
│   │   └── list.go
│   └── models/
│       └── task.go
├── go.mod
└── go.sum
```

**Library 架构** (simple/medium):
```
project-name/
├── internal/
│   ├── core.go
│   └── utils.go
├── pkg/
│   └── api.go
├── go.mod
└── go.sum
```

**Web 架构** (medium/complex):
```
project-name/
├── cmd/
│   └── server/
│       └── main.go
├── internal/
│   ├── config/
│   │   └── config.go
│   ├── api/
│   │   └── v1/
│   │       └── router.go
│   ├── models/
│   │   └── user.go
│   └── services/
│       └── service.go
├── pkg/
│   └── middleware/
│       └── auth.go
├── go.mod
└── go.sum
```

**执行**:
```bash
# 根据选择的架构类型创建目录
# 示例：创建 CLI 项目架构
mkdir -p cmd/project-name
mkdir -p internal/{cli,models}
mkdir -p pkg/api

# Go 使用目录作为包，无需 __init__.py
```

**CHECKLIST**:
- [ ] 架构类型已选择
- [ ] 目录结构已创建
- [ ] 无 __init__.py（Go 不需要）

---

### 2.3 系统文件

**Tool**: Write

**go.mod**:
```go
module github.com/username/project-name

go 1.21

require (
    // 根据项目类型添加依赖
    // CLI: cobra, viper
    // Web: gin, gorm
    // Library: 无额外依赖
)
```

**go.sum** (自动生成):
```bash
go mod download
go mod tidy
```

**Makefile**:
```makefile
.PHONY: test build clean run

test:
	go test -v -race -cover ./...

build:
	go build -o bin/project-name ./cmd/project-name

clean:
	go clean
	rm -rf bin/

run:
	go run ./cmd/project-name

fmt:
	go fmt ./...

lint:
	golangci-lint run ./...

mod-tidy:
	go mod tidy
```

**README.md**:
```markdown
# Project Name

{{GOAL}}

## Setup

\`\`\`bash
# Download dependencies
go mod download

# Run tests
make test

# Build
make build
\`\`\`

## Development

\`\`\`bash
# Format code
make fmt

# Run linter
make lint

# Run with coverage
make test
\`\`\`
```

**CHECKLIST**:
- [ ] go.mod 创建
- [ ] Makefile 创建
- [ ] README.md 创建
- [ ] .gitignore 创建（Phase 2.1）

---

### 2.4 项目文件

**Tool**: Write

**原则**: 创建空占位文件，**严禁编写业务逻辑**

**Go 文件模板**:
```go
// Package cli provides CLI commands for the application.
package cli

// RootCmd represents the base command when called without any subcommands.
var RootCmd = &cobra.Command{
    Use:   "project-name",
    Short: "A brief description of your application",
}
```

**执行**:
```bash
# 创建空占位文件
touch cmd/project-name/main.go
touch internal/cli/root.go
touch internal/models/task.go
# 等等...
```

**CHECKLIST**:
- [ ] 所有目录已创建
- [ ] 占位文件已生成
- [ ] 无业务逻辑代码

---

### 2.5 依赖安装

**Tool**: Bash

**执行**:
```bash
# 下载依赖
go mod download

# 整理依赖
go mod tidy
```

**说明**:
- Go 使用 go.mod 管理依赖
- 自动下载 go.mod 中指定的依赖

**注意**: 必须在创建项目架构（2.2）和系统文件（2.3）之后执行，因为需要 go.mod

**CHECKLIST**:
- [ ] 依赖已下载
- [ ] go.sum 已生成
- [ ] 无依赖冲突

---

## Phase 3: 工作树准备（老项目）

**适用场景**: `{{PROJECT_STATUS}}` == add-feature

**Skip if**: 新项目（`{{PROJECT_STATUS}}` == new）

### 3.1 Git 分支管理

**Tool**: Bash

**执行**:
```bash
# 检查当前分支
CURRENT_BRANCH=$(git branch --show-current)
echo "当前分支: $CURRENT_BRANCH"

# 创建 feature 分支
FEATURE_NAME="{{VERSION_DIR}}"  # 例如: v1_add_percentage
git checkout -b feature/"$FEATURE_NAME"

echo "已创建并切换到分支: feature/$FEATURE_NAME"
```

**CHECKLIST**:
- [ ] 当前分支确认
- [ ] Feature 分支创建成功
- [ ] 分支命名符合规范

---

### 3.2 依赖管理

**Tool**: Bash

**执行**:
```bash
# 添加新功能所需的依赖
go get github.com/gin-gonic/gin
go get gorm.io/gorm

# 整理依赖
go mod tidy
```

**CHECKLIST**:
- [ ] 依赖已添加到 go.mod
- [ ] 依赖已下载
- [ ] 无依赖冲突

---

### 3.3 系统文件更新

**Tool**: Edit

**执行**:
- 更新 README.md 添加新功能说明
- 更新版本号（如需要）

**README.md 更新示例**:
```markdown
## 功能列表

### v{{N}} - {{FEATURE_NAME}}

- 功能描述1
- 功能描述2

\`\`\`
```

**CHECKLIST**:
- [ ] README.md 已更新
- [ ] 版本号已更新（如需要）
- [ ] 变更日志已记录

---

### 3.4 新功能文件创建

**Tool**: Write

**原则**: 创建空文件，不编写业务逻辑

**执行**:
```bash
# 根据功能需求确定需要新增的文件
# 创建占位文件
mkdir -p internal/new_feature
touch internal/new_feature/handler.go
```

**CHECKLIST**:
- [ ] 新增目录已创建
- [ ] 占位文件已生成
- [ ] 无业务逻辑代码
- [ ] 与现有架构一致

---

## Phase 4: TDD 执行

**适用场景**: 所有项目

**🚨 强制要求**:
- **严禁手动创建业务代码文件**
- **严禁手动编写业务逻辑**
- 必须使用 TDD 工具完成所有编码工作

**📋 文档注入**: 所有 Phase 4 子阶段使用本文档顶部定义的标准格式。

### Simple 项目 ({{COMPLEXITY}} == simple)

**Tool**: pyflow-golang-testing

**前置步骤**: 使用本文档顶部定义的标准格式读取文档

```python
constitution = Read("./pjflow/constitution.md")
requirements = Read("./pjflow/{{VERSION_DIR}}/requirements.md")
```

**执行**: 单次 TDD 循环（RED → GREEN → REFACTOR）

**调用**:
```
Skill(skill="pyflow-golang-testing", args="""
{{GOAL}} --single-cycle

## 🚨 强制约束（必须遵守）

### 项目宪法
{constitution}

### 需求文档
{requirements}

**重要**: 违反上述约束的代码/测试将被拒绝！
""")
```

**后置步骤**: 合规检查
```bash
python .claude/skills/projectflow-executor/scripts/check_compliance.py \
    --language go \
    --version-dir {{VERSION_DIR}} \
    --phase tdd
```

**CHECKLIST**:
- [ ] RED Phase: 测试编写
- [ ] GREEN Phase: 最小实现通过测试
- [ ] REFACTOR Phase: 代码重构
- [ ] 所有测试通过
- [ ] 无手动编码
- [ ] Compliance check passed
- [ ] Compliance report generated

---

### Medium 项目 ({{COMPLEXITY}} == medium)

**执行方式**: RED → GREEN → REFACTOR 三阶段

#### Phase 4.1: RED - 生成测试

**Tool**: pyflow-golang-testing

**Tool Type**: Task (subagent_type)

**前置步骤**: 使用本文档顶部定义的标准格式读取文档

```python
constitution = Read("./pjflow/constitution.md")
requirements = Read("./pjflow/{{VERSION_DIR}}/requirements.md")
```

**执行**: 生成完整测试套件

**调用**:
```
Task(
    subagent_type="pyflow-golang-testing",
    subject="生成测试套件",
    description=f"""
    为 {{GOAL}} 生成完整测试套件

    ## 🚨 强制约束（必须遵守）

    ### 项目宪法（完整内容）
    {constitution}

    ### 需求文档（完整内容）
    {requirements}

    **重要**: 违反上述约束的代码/测试将被拒绝！
    """,
    activeForm="生成测试套件"
)
```

**后置步骤**: 合规检查
```bash
python .claude/skills/projectflow-executor/scripts/check_compliance.py \
    --language go \
    --version-dir {{VERSION_DIR}} \
    --phase red
```

**CHECKLIST**:
- [ ] Test files generated
- [ ] Test structure defined
- [ ] Test cases cover requirements
- [ ] 文档已读取（使用 Read 工具）
- [ ] Compliance: Tests cover Requirements and Constitution standards
- [ ] Compliance check passed
- [ ] Compliance report generated

---

#### Phase 4.2: GREEN - 实现功能

**Tool**: pyflow-go-pro

**Tool Type**: Task (subagent_type)

**前置步骤**: 使用本文档顶部定义的标准格式读取文档

```python
constitution = Read("./pjflow/constitution.md")
requirements = Read("./pjflow/{{VERSION_DIR}}/requirements.md")
```

**执行**: 实现所有功能使测试通过

**调用**:
```
Task(
    subagent_type="pyflow-go-pro",
    subject="实现功能使测试通过",
    description=f"""
    实现所有功能使测试通过

    ## 🚨 强制约束（必须遵守）

    ### 项目宪法（完整内容）
    {constitution}

    ### 需求文档（完整内容）
    {requirements}

    **重要**: 违反上述约束的代码将被拒绝！
    """,
    activeForm="实现功能"
)
```

**后置步骤**: 合规检查
```bash
python .claude/skills/projectflow-executor/scripts/check_compliance.py \
    --language go \
    --version-dir {{VERSION_DIR}} \
    --phase green
```

**CHECKLIST**:
- [ ] All features implemented
- [ ] All tests pass
- [ ] Code follows constitution
- [ ] 文档已读取（使用 Read 工具）
- [ ] Compliance: Code within Requirements scope, follows Constitution standards
- [ ] Compliance check passed
- [ ] Compliance report generated

---

#### Phase 4.3: REFACTOR - 重构代码

**Tool**: pyflow-go-pro

**Tool Type**: Task (subagent_type)

**前置步骤**: 使用本文档顶部定义的标准格式读取文档

```python
constitution = Read("./pjflow/constitution.md")
requirements = Read("./pjflow/{{VERSION_DIR}}/requirements.md")
```

**执行**: 优化代码结构和质量

**调用**:
```
Task(
    subagent_type="pyflow-go-pro",
    subject="重构优化代码",
    description=f"""
    优化代码结构和质量

    ## 🚨 强制约束（必须遵守）

    ### 项目宪法（完整内容）
    {constitution}

    ### 需求文档（完整内容）
    {requirements}

    **重要**: 违反上述约束的代码将被拒绝！
    """,
    activeForm="重构优化"
)
```

**后置步骤**: 合规检查
```bash
python .claude/skills/projectflow-executor/scripts/check_compliance.py \
    --language go \
    --version-dir {{VERSION_DIR}} \
    --phase refactor
```

**CHECKLIST**:
- [ ] Code refactored
- [ ] All tests still pass
- [ ] Code quality improved
- [ ] Performance optimized (if needed)
- [ ] Compliance: Refactor preserves Constitution compliance
- [ ] Compliance check passed
- [ ] Compliance report generated

---

### Complex 项目 ({{COMPLEXITY}} == complex)

**执行方式**: 扩展 TDD 循环

#### Phase 4.1: RED - 生成完整测试

**Tool**: pyflow-golang-testing

**前置步骤**: 使用本文档顶部定义的标准格式读取文档

```python
constitution = Read("./pjflow/constitution.md")
requirements = Read("./pjflow/{{VERSION_DIR}}/requirements.md")
```

**调用**:
```
Task(
    subagent_type="pyflow-golang-testing",
    subject="生成完整测试套件",
    description=f"""
    为 {{GOAL}} 生成单元测试、集成测试、性能测试、并发测试

    ## 🚨 强制约束（必须遵守）

    ### 项目宪法（完整内容）
    {constitution}

    ### 需求文档（完整内容）
    {requirements}

    **重要**: 违反上述约束的代码/测试将被拒绝！
    """,
    activeForm="生成测试套件"
)
```

**后置步骤**: 合规检查
```bash
python .claude/skills/projectflow-executor/scripts/check_compliance.py \
    --language go \
    --version-dir {{VERSION_DIR}} \
    --phase red
```

**CHECKLIST**:
- [ ] Unit tests generated
- [ ] Integration tests defined
- [ ] Performance tests defined
- [ ] Concurrency tests defined
- [ ] 文档已读取（使用 Read 工具）
- [ ] Compliance: Tests cover Requirements and Constitution standards
- [ ] Compliance check passed
- [ ] Compliance report generated

---

#### Phase 4.2: GREEN - 基础实现

**Tool**: pyflow-go-pro

**前置步骤**: 使用本文档顶部定义的标准格式读取文档

```python
constitution = Read("./pjflow/constitution.md")
requirements = Read("./pjflow/{{VERSION_DIR}}/requirements.md")
```

**调用**:
```
Task(
    subagent_type="pyflow-go-pro",
    subject="实现基础功能",
    description=f"""
    实现所有功能使测试通过

    ## 🚨 强制约束（必须遵守）

    ### 项目宪法（完整内容）
    {constitution}

    ### 需求文档（完整内容）
    {requirements}

    **重要**: 违反上述约束的代码将被拒绝！
    """,
    activeForm="实现基础功能"
)
```

**后置步骤**: 合规检查
```bash
python .claude/skills/projectflow-executor/scripts/check_compliance.py \
    --language go \
    --version-dir {{VERSION_DIR}} \
    --phase green
```

**CHECKLIST**:
- [ ] Basic implementation completed
- [ ] All unit tests pass
- [ ] Code follows constitution
- [ ] 文档已读取（使用 Read 工具）
- [ ] Compliance: Code within Requirements scope, follows Constitution standards
- [ ] Compliance check passed
- [ ] Compliance report generated

---

#### Phase 4.3: GREEN - 并发优化（如需要）

**Tool**: pyflow-go-pro

**前置步骤**: 使用本文档顶部定义的标准格式读取文档

```python
constitution = Read("./pjflow/constitution.md")
requirements = Read("./pjflow/{{VERSION_DIR}}/requirements.md")
```

**执行**: 添加并发支持提高性能

**调用**:
```
Task(
    subagent_type="pyflow-go-pro",
    subject="添加并发支持以提高性能",
    description=f"""
    添加 goroutine/channel 支持

    ## 🚨 强制约束（必须遵守）

    ### 项目宪法（完整内容）
    {constitution}

    ### 需求文档（完整内容）
    {requirements}

    **重要**: 违反上述约束的代码将被拒绝！
    """,
    activeForm="优化并发性能"
)
```

**后置步骤**: 合规检查
```bash
python .claude/skills/projectflow-executor/scripts/check_compliance.py \
    --language go \
    --version-dir {{VERSION_DIR}} \
    --phase concurrent
```

**CHECKLIST**:
- [ ] Concurrent patterns implemented
- [ ] All tests still pass
- [ ] Performance improved
- [ ] 文档已读取（使用 Read 工具）
- [ ] Compliance: Concurrent patterns follow Constitution requirements
- [ ] Compliance check passed
- [ ] Compliance report generated

**Skip if**: `{{PROJECT_STATUS}}` == new 或项目不需要并发

---

#### Phase 4.4: GREEN - 性能优化

**Tool**: pyflow-golang-patterns

**前置步骤**: 使用本文档顶部定义的标准格式读取文档

```python
constitution = Read("./pjflow/constitution.md")
requirements = Read("./pjflow/{{VERSION_DIR}}/requirements.md")
```

**执行**: 分析并优化性能瓶颈

**调用**:
```
Task(
    subagent_type="pyflow-golang-patterns",
    subject="分析并优化性能瓶颈",
    description=f"""
    分析并优化性能瓶颈

    ## 🚨 强制约束（必须遵守）

    ### 项目宪法（完整内容）
    {constitution}

    ### 需求文档（完整内容）
    {requirements}

    **重要**: 违反上述约束的代码将被拒绝！
    """,
    activeForm="优化性能"
)
```

**后置步骤**: 合规检查
```bash
python .claude/skills/projectflow-executor/scripts/check_compliance.py \
    --language go \
    --version-dir {{VERSION_DIR}} \
    --phase performance
```

**CHECKLIST**:
- [ ] Performance profiled
- [ ] Bottlenecks identified
- [ ] Optimizations applied
- [ ] Performance targets met
- [ ] 文档已读取（使用 Read 工具）
- [ ] Compliance: Performance optimizations meet Requirements targets
- [ ] Compliance check passed
- [ ] Compliance report generated

**Skip if**: 项目没有性能要求

---

#### Phase 4.5: REFACTOR - 深度优化

**Tool**: pyflow-golang-patterns

**前置步骤**: 使用本文档顶部定义的标准格式读取文档

```python
constitution = Read("./pjflow/constitution.md")
requirements = Read("./pjflow/{{VERSION_DIR}}/requirements.md")
```

**执行**: 应用高级优化技术

**调用**:
```
Task(
    subagent_type="pyflow-golang-patterns",
    subject="深度性能优化",
    description=f"""
    应用高级优化技术

    ## 🚨 强制约束（必须遵守）

    ### 项目宪法（完整内容）
    {constitution}

    ### 需求文档（完整内容）
    {requirements}

    **重要**: 违反上述约束的代码将被拒绝！
    """,
    activeForm="深度优化"
)
```

**后置步骤**: 合规检查
```bash
python .claude/skills/projectflow-executor/scripts/check_compliance.py \
    --language go \
    --version-dir {{VERSION_DIR}} \
    --phase deep-refactor
```

**CHECKLIST**:
- [ ] Advanced optimizations applied
- [ ] Code quality excellent
- [ ] All tests still pass
- [ ] Performance significantly improved
- [ ] 文档已读取（使用 Read 工具）
- [ ] Compliance: Refactor preserves Constitution compliance
- [ ] Compliance check passed
- [ ] Compliance report generated

---

#### Phase 4.6: REFACTOR - 最终清理

**Tool**: pyflow-go-pro

**前置步骤**: 使用本文档顶部定义的标准格式读取文档

```python
constitution = Read("./pjflow/constitution.md")
requirements = Read("./pjflow/{{VERSION_DIR}}/requirements.md")
```

**执行**: 清理代码、更新文档

**调用**:
```
Task(
    subagent_type="pyflow-go-pro",
    subject="最终代码清理",
    description=f"""
    清理代码、更新文档、确保代码质量

    ## 🚨 强制约束（必须遵守）

    ### 项目宪法（完整内容）
    {constitution}

    ### 需求文档（完整内容）
    {requirements}

    **重要**: 违反上述约束的代码将被拒绝！
    """,
    activeForm="清理代码"
)
```

**后置步骤**: 合规检查
```bash
python .claude/skills/projectflow-executor/scripts/check_compliance.py \
    --language go \
    --version-dir {{VERSION_DIR}} \
    --phase final
```

**CHECKLIST**:
- [ ] Code cleaned up
- [ ] Documentation updated
- [ ] All tests pass
- [ ] Code quality excellent
- [ ] 文档已读取（使用 Read 工具）
- [ ] Compliance: Final code follows all Constitution standards
- [ ] Compliance check passed
- [ ] Compliance report generated

---

## Phase 5: 质量审核

**适用场景**: 所有项目

### Simple 项目

#### 5.1 质量检查

**前置步骤**: 读取合规文档
```python
constitution = Read("./pjflow/constitution.md")
requirements = Read("./pjflow/{{VERSION_DIR}}/requirements.md")
```

**Tool**: Bash

**执行**:
```bash
make test
make build
go vet ./...
go fmt ./...

# 运行完整合规检查
python .claude/skills/projectflow-executor/scripts/check_compliance.py \
    --language go \
    --version-dir {{VERSION_DIR}} \
    --phase review
```

**CHECKLIST**:
- [ ] All tests pass (100%)
- [ ] Build succeeds
- [ ] go vet passes
- [ ] Code formatted
- [ ] Compliance: Code follows constitution standards
- [ ] Compliance report verified
- [ ] No critical/high issues

---

#### 5.2 代码审核

**前置步骤**: 读取合规文档和最新合规报告
```python
constitution = Read("./pjflow/constitution.md")
requirements = Read("./pjflow/{{VERSION_DIR}}/requirements.md")
compliance_report = Read("./pjflow/{{VERSION_DIR}}/compliance_report.md")
```

**Tool**: pyflow-go-reviewer

**Tool Type**: Task (subagent_type)

**调用**:
```
Task(
    subagent_type="pyflow-go-reviewer",
    subject="审核代码",
    description=f"""
    审核整个代码库

    ## 参考文档

    ### 项目宪法
    {constitution}

    ### 需求文档
    {requirements}

    ### 合规报告
    {compliance_report}

    请验证代码是否符合宪法和需求要求，并审核合规报告中的问题。
    """,
    activeForm="审核代码"
)
```

**CHECKLIST**:
- [ ] Code review completed
- [ ] Issues documented (if any)
- [ ] Constitution compliance verified
- [ ] Requirements compliance verified
- [ ] Compliance issues reviewed (if any)

---

#### 5.2a 架构审核（Medium/Complex 项目）

**适用场景**: `{{COMPLEXITY}}` == medium 或 complex

**Tool**: pyflow-architect-review

**Tool Type**: Task (subagent_type)

**执行**: 审核系统架构设计

**调用**:
```
Task(
    subagent_type="pyflow-architect-review",
    subject="审核系统架构",
    description="审核系统架构设计、可扩展性、可维护性",
    activeForm="审核架构"
)
```

**CHECKLIST**:
- [ ] Architecture review completed
- [ ] Scalability verified
- [ ] Maintainability assessed
- [ ] Architecture decision records created (if needed)

**Skip if**: `{{COMPLEXITY}}` == simple

---

#### 5.3 Git 提交

**Tool**: Bash

**执行**:
```bash
git add .
git commit -m "feat: {{COMMIT_MESSAGE}}"

echo "✅ Git 提交完成"
```

**CHECKLIST**:
- [ ] All changes committed
- [ ] Commit message follows conventions
- [ ] Working tree clean

---

## CHECKLIST 模板

**说明**: executor 在每个 Phase 完成后更新对应的 CHECKLIST

**更新时机**:
| Phase | 更新时机 | 更新内容 |
|-------|---------|---------|
| Phase 0 | brainstorming 完成后 | 需求分析相关 checkbox |
| Phase 1 | constitution 创建后 | 项目规则相关 checkbox |
| Phase 2.0 干扰检测后 | 项目准备相关 checkbox |
| Phase 2.1 (Git) 完成后 | Git 仓库相关 checkbox |
| Phase 2.2 (架构) 完成后 | 项目架构相关 checkbox |
| Phase 2.3 (系统文件) 完成后 | go.mod 等系统文件 checkbox |
| Phase 2.4 (项目文件) 完成后 | 占位文件创建 checkbox |
| Phase 2.5 (依赖安装) 完成后 | 依赖安装 checkbox |
| Phase 3.1 完成后 | 工作环境相关 checkbox |
| Phase 3.2 完成后 | 工作环境相关 checkbox |
| Phase 3.3 完成后 | 工作环境相关 checkbox |
| Phase 3.4 完成后 | 工作环境相关 checkbox |
| Phase 4 (Simple) 完成后 | TDD 执行相关 checkbox |
| Phase 4.1 (Medium) 完成后 | 测试套件生成 checkbox |
| Phase 4.2 (Medium) 完成后 | 基础实现 checkbox |
| Phase 4.3 (Medium) 完成后 | 代码重构 checkbox |
| Phase 4 (Complex) 完成后 | 完整测试套件生成 checkbox |
| Phase 4.2 (Complex) 完成后 | 基础实现 checkbox |
| Phase 4.3 (Complex) 完成后 | 并发优化 checkbox |
| Phase 4.4 (Complex) 完成后 | 性能优化 checkbox |
| Phase 4.5 (Complex) 完成后 | 深度优化 checkbox |
| Phase 4.6 (Complex) 完成后 | 最终清理 checkbox |
| Phase 5 (Simple) 完成后 | 质量检查通过 checkbox |
| Phase 5 (Simple) 完成后 | 代码审核完成 checkbox |
| Phase 5 (Medium/Complex) 完成后 | Git 提交完成 checkbox |

**使用示例**:

```go
Edit(
    file_path="CHECKLIST.md",
    old_string="- [ ] Phase 0: brainstorming 完成",
    new_string="- [x] Phase 0: brainstorming 完成"
)
```

---

## 复杂度差异化说明

### Simple 项目特征

**预期 LOC**: < 300 行

**特点**:
- 单一功能，明确需求
- 最小架构（2-3 层）
- 单次 TDD 循环
- 基础质量审核
- 快速迭代

**Phase 4 执行**: 单次 `pyflow-golang-testing --single-cycle`

### Medium 项目特征

**预期 LOC**: 300-1000 行

**特点**:
- 多个相关功能
- 标准架构（3-5 层）
- 完整 TDD 三阶段
- 代码审核
- 性能考虑

**Phase 4 执行**: RED → GREEN → REFACTOR

### Complex 项目特征

**预期 LOC**: > 1000 行

**特点**:
- 平台级或框架级
- 深层架构（5+ 层）
- 扩展 TDD 循环（并发、性能）
- 深度审核
- 安全审核
- 完整 CI/CD

**Phase 4 执行**: RED → GREEN → 并发优化 → 性能优化 → 深度优化 → 最终清理

---

## 工具调用格式与示例

### Tool 类型与调用方式

| Tool 类型 | 调用方式 | 说明 |
|-----------|----------|------|
| **Skill** | `Skill(skill="name", args="...")` | 调用其他 skill |
| **Task** | `Task(subagent_type="...", ...)` | 调用 agent |
| **Bash** | `Bash(command="...")` | 执行命令 |
| **Write** | `Write(file_path="...", content="...")` | 写入文件 |
| **Edit** | `Edit(file_path="...", old_string="...", new_string="...")` | 编辑文件 |

### Skill 调用示例

```go
// 调用 pyflow-brainstorming 探索需求
Skill(skill="pyflow-brainstorming", args="{{GOAL}}")

// 调用 pyflow-constitution 创建宪法
Skill(skill="pyflow-constitution", args="{{GOAL}}")

// 调用 pyflow-golang-testing 执行 TDD
Skill(skill="pyflow-golang-testing", args="{{GOAL}} --single-cycle")

// 调用 code-reviewer 审核代码
Task(
    subagent_type="pyflow-go-reviewer",
    subject="审核代码",
    description="审核整个代码库"
)
```

### Task 调用（Agent）

```go
// 调用 pyflow-golang-testing 生成测试
Task(
    subagent_type="pyflow-golang-testing",
    subject="生成测试套件",
    description="为 {{GOAL}} 生成完整测试套件"
)

// 调用 pyflow-go-pro 实现 Go 功能
Task(
    subagent_type="pyflow-go-pro",
    subject="实现功能使测试通过",
    description="实现所有功能使测试通过"
)

// 调用 pyflow-architect-review 审核架构
Task(
    subagent_type="pyflow-architect-review",
    subject="审核系统架构",
    description="审核系统架构设计、可扩展性、可维护性"
)
```

### Bash 命令示例

```bash
# Git 初始化
git init
git branch -M main

# Go module 初始化
go mod init github.com/username/project-name

# 安装依赖
go mod download
go mod tidy

# 创建目录
mkdir -p cmd/project-name
mkdir -p internal/{cli,models}

# 运行测试
go test -v -race -cover ./...

# 代码格式化
go fmt ./...

# Go vet
go vet ./...

# Git 提交
git add .
git commit -m "feat: implement feature"
```

---

## 合规性检查说明

**自动化合规检查**: 每个重要阶段完成后，系统会自动运行合规检查脚本

### 检查内容

1. **代码风格**: gofmt 格式检查
2. **静态分析**: go vet 检查
3. **测试覆盖率**: go test 覆盖率检查
4. **错误处理**: 忽略的错误返回值检测
5. **类型注解**: interface{} 过度使用检测
6. **宪法合规**: 代码是否遵循项目宪法规则
7. **需求合规**: 代码是否超出需求范围

### 合规报告

每次检查后生成合规报告到 `pjflow/{{VERSION_DIR}}/compliance_report.md`

### 问题等级

- **Critical**: 必须修复才能继续
- **High**: 强烈建议修复
- **Medium**: 建议修复
- **Low**: 可选修复

### 文档注入模式

所有 Task 调用都会注入项目宪法和需求文档，确保 sub-agent 遵守约束：

```python
# 读取文档
constitution = Read("./pjflow/constitution.md")
requirements = Read("./pjflow/{{VERSION_DIR}}/requirements.md")

# 注入到 prompt
enhanced_prompt = f"""
{original_task_description}

## 🚨 强制约束（必须遵守）

### 项目宪法
{constitution}

### 需求文档
{requirements}

**重要**: 违反上述约束的代码将被拒绝！
"""
```

---

**版本**: 2.0.0
**用途**: ProjectFlow Planner - Go 完整计划模板
**适用语言**: Go (go.mod, go.sum)
**更新内容**: 完整 Phase 0-5 结构 + 合规性检查集成

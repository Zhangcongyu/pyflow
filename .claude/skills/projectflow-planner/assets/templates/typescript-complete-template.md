# TypeScript 项目完整计划模板

**说明**: 此模板包含 TypeScript 项目所有 Phase 的框架。Planner 读取此模板生成 task_plan.md，Executor 根据计划执行。

---

## 模板变量

| 变量 | 说明 | 示例值 |
|--------|------|----------|
| `{{GOAL}}` | 用户原始需求 | "创建一个 CLI 待办事项应用" |
| `{{PROJECT_STATUS}}` | new / add-feature | new |
| `{{COMPLEXITY}}` | simple / medium / complex | medium |
| `{{VERSION_DIR}}` | 版本目录名称 | v0_initial / v1_add_feature |
| `{{PROJECT_NAME}}` | 项目名称 | myapp |

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
├── src/
│   ├── index.ts
│   └── cli.ts
├── tests/
│   └── {{PROJECT_NAME}}.test.ts
├── package.json
├── tsconfig.json
└── README.md
\`\`\`

### 技术栈

- **语言**: TypeScript 5.0+
- **包管理**: pnpm
- **CLI 框架**: commander / yargs
- **测试框架**: vitest

### 模块划分

| 模块 | 文件 | 职责 |
|------|------|------|
| CLI | cli.ts | 命令行界面，参数解析 |
| Main | index.ts | 程序入口 |

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
CONFLICT_DIRS="src tests node_modules dist .next .nuxt"
CONFLICT_FILES="package.json package-lock.json pnpm-lock.yaml yarn.lock tsconfig.json"

for dir in $CONFLICT_DIRS; do
    if [ -d "$dir" ]; then
        HAS_CONFLICT=true
        break
    fi
done

if [ "$HAS_CONFLICT" = true ]; then
    # 使用 AskUserQuestion 询问用户
    问题："检测到目录中已存在项目文件 (src/, tests/ 等)，是否删除并重新创建？"
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
| CLI, 命令行, 工具 | **cli** | 2-3 层 | pyflow-typescript-pro |
| Library, 库, SDK, 框架 | **library** | 2-3 层 | pyflow-typescript-pro |
| Express, API, REST | **express** | 多层 | pyflow-typescript-pro |
| Next.js, 全栈, Web 应用 | **nextjs** | 多层 | pyflow-frontend-developer |
| React, 前端, 组件库 | **react** | 组件层 | pyflow-frontend-developer |
| Nuxt, Vue, 全栈 | **nuxt** | 多层 | pyflow-frontend-developer |
| Data, 数据处理, ETL, 分析 | **data** | 深层 | pyflow-typescript-pro |

**CLI 架构** (simple/medium):
```
project-name/
├── src/
│   ├── index.ts
│   ├── cli.ts
│   ├── commands/
│   │   ├── add.ts
│   │   ├── list.ts
│   │   └── index.ts
│   └── models/
│       └── task.ts
├── tests/
│   ├── cli.test.ts
│   └── commands/
│       ├── add.test.ts
│       └── list.test.ts
├── package.json
├── tsconfig.json
└── vitest.config.ts
```

**Library 架构** (simple/medium):
```
project-name/
├── src/
│   ├── index.ts
│   ├── core.ts
│   └── utils.ts
├── tests/
│   ├── core.test.ts
│   └── utils.test.ts
├── package.json
├── tsconfig.json
└── vitest.config.ts
```

**Express 架构** (medium/complex):
```
project-name/
├── src/
│   ├── index.ts
│   ├── app.ts
│   ├── config/
│   │   └── index.ts
│   ├── api/
│   │   └── v1/
│   │       └── router.ts
│   ├── core/
│   │   ├── database.ts
│   │   └── security.ts
│   ├── models/
│   │   └── user.ts
│   └── services/
│       └── index.ts
└── tests/
    ├── api/
    │   └── v1/
    │       └── router.test.ts
    └── core/
        └── database.test.ts
```

**Next.js 架构** (medium/complex):
```
project-name/
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── api/
│   │       └── v1/
│   │           └── route.ts
│   ├── components/
│   │   ├── ui/
│   │   └── forms/
│   ├── lib/
│   │   └── utils.ts
│   └── models/
│       └── user.ts
├── tests/
│   ├── unit/
│   └── integration/
└── next.config.js
```

**React 架构** (medium/complex):
```
project-name/
├── src/
│   ├── index.tsx
│   ├── components/
│   │   ├── ui/
│   │   └── forms/
│   ├── hooks/
│   │   └── index.ts
│   ├── lib/
│   │   └── utils.ts
│   └── models/
│       └── task.ts
├── tests/
│   ├── components/
│   └── hooks/
└── vite.config.ts
```

**执行**:
```bash
# 根据选择的架构类型创建目录
# 示例：创建 Express 项目架构
mkdir -p src/{api/v1,core,models,services}
mkdir -p tests/{api/v1,core}

# TypeScript 不需要 __init__.py
# 文件通过 .ts/.tsx 扩展名识别
```

**CHECKLIST**:
- [ ] 架构类型已选择
- [ ] 目录结构已创建
- [ ] 无 __init__.py（TypeScript 不需要）

---

### 2.3 系统文件

**Tool**: Write

**package.json**:
```json
{
  "name": "project-name",
  "version": "0.1.0",
  "description": "{{GOAL}}",
  "type": "module",
  "main": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "scripts": {
    "dev": "tsx watch src/index.ts",
    "build": "tsup",
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest --coverage",
    "lint": "eslint src/",
    "lint:fix": "eslint src/ --fix",
    "format": "prettier --write src/",
    "typecheck": "tsc --noEmit"
  },
  "dependencies": [
    // 根据项目类型添加依赖
    // CLI: commander, zod
    // Express: express, zod
    // React: react, zod
    // Next.js: next, zod
  ],
  "devDependencies": {
    "typescript": "^5.3.0",
    "vitest": "^1.0.0",
    "@vitest/coverage-v8": "^1.0.0",
    "eslint": "^8.57.0",
    "prettier": "^3.2.0",
    "tsup": "^8.0.0",
    "tsx": "^4.7.0"
  }
}
```

**tsconfig.json**:
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "lib": ["ES2022"],
    "moduleResolution": "Bundler",
    "resolveJsonModule": true,
    "allowJs": true,
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "forceConsistentCasingInFileNames": true,
    "isolatedModules": true,
    "outDir": "./dist",
    "rootDir": "./src",
    "declaration": true,
    "declarationMap": true
  },
  "include": ["src/**/*.ts", "src/**/*.tsx"],
  "exclude": ["node_modules", "dist"]
}
```

**vitest.config.ts**:
```typescript
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    include: ['tests/**/*.test.ts', 'tests/**/*.test.tsx'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: ['tests/**/*.test.ts', 'tests/**/*.test.tsx'],
    },
  },
})
```

**.gitignore**: 见 2.1（调整为 Node.js）

**README.md**:
```markdown
# Project Name

{{GOAL}}

## Setup

\`\`\`bash
# 使用 npm
npm install

# 或使用 pnpm
pnpm install

# 或使用 yarn
yarn install
\`\`\`

## Development

\`\`\`bash
# Run tests
npm test

# Format code
npm run format

# Run with coverage
npm run test:coverage

# Type check
npm run typecheck
\`\`\`
```

**CHECKLIST**:
- [ ] package.json 创建
- [ ] tsconfig.json 创建
- [ ] vitest.config.ts 创建
- [ ] README.md 创建
- [ ] .gitignore 创建（Phase 2.1）

---

### 2.4 项目文件

**Tool**: Write

**原则**: 创建空占位文件，**严禁编写业务逻辑**

**TypeScript 文件模板**:
```typescript
/**
 * {{MODULE_DESCRIPTION}}
 */

export * from './index';
```

**执行**:
```bash
# 创建空占位文件
touch src/index.ts
touch src/cli.ts
touch src/models/task.ts
# 等等...
```

**CHECKLIST**:
- [ ] 所有目录已创建
- [ ] 占位文件已生成
- [ ] 无业务逻辑代码

---

### 2.5 虚拟环境

**Tool**: Bash

**前置检测**:
- 虚拟环境类型
- 是否已存在

**执行**:
```bash
# 安装依赖（根据包管理器）
npm install
# 或
pnpm install
# 或
yarn install
```

**说明**:
- TypeScript 使用 npm/pnpm/yarn，无需专用工具
- 自动安装 package.json 中的 dependencies

**注意**: 必须在创建项目架构（2.2）和系统文件（2.3）之后执行，因为需要 package.json 和 tsconfig.json

**CHECKLIST**:
- [ ] 依赖安装
- [ ] node_modules 已创建
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
npm install zod express
# 或
pnpm add zod express
```

**说明**:
- TypeScript 无需专用包管理器
- 直接使用 npm/pnpm/yarn

**CHECKLIST**:
- [ ] 依赖已添加到 package.json
- [ ] 依赖已安装到 node_modules
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
mkdir -p src/new_feature
touch src/new_feature/index.ts
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

### Simple 项目 ({{COMPLEXITY}} == simple)

**Tool**: pyflow-tdd-cycle

**前置步骤**: 读取合规文档
```python
constitution = Read("./pjflow/constitution.md")
requirements = Read("./pjflow/{{VERSION_DIR}}/requirements.md")
```

**执行**: 单次 TDD 循环（RED → GREEN → REFACTOR）

**调用**:
```
Skill(skill="pyflow-tdd-cycle", args="""
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
    --language typescript \
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

**Tool**: pyflow-test-automator

**Tool Type**: Task (subagent_type)

**前置步骤**: 读取合规文档
```python
constitution = Read("./pjflow/constitution.md")
requirements = Read("./pjflow/{{VERSION_DIR}}/requirements.md")
```

**执行**: 生成完整测试套件

**调用**:
```
Task(
    subagent_type="pyflow-test-automator",
    subject="生成测试套件",
    description="""
    为 {{GOAL}} 生成完整测试套件

    ## 🚨 强制约束（必须遵守）

    ### 项目宪法
    {constitution}

    ### 需求文档
    {requirements}

    **重要**: 违反上述约束的代码/测试将被拒绝！
    """,
    activeForm="生成测试套件"
)
```

**后置步骤**: 合规检查
```bash
python .claude/skills/projectflow-executor/scripts/check_compliance.py \
    --language typescript \
    --version-dir {{VERSION_DIR}} \
    --phase red
```

**CHECKLIST**:
- [ ] Test files generated
- [ ] Test structure defined
- [ ] Test cases cover requirements
- [ ] Compliance: Tests cover Requirements and Constitution standards
- [ ] Compliance check passed
- [ ] Compliance report generated

---

#### Phase 4.2: GREEN - 实现功能

**Tool**: pyflow-typescript-pro (或 pyflow-frontend-developer，如果项目类型是 Next.js/React)

**Agent 选择逻辑**：
根据项目类型选择 agent：
- Next.js/React 项目 → pyflow-frontend-developer
- Express 项目 → pyflow-typescript-pro
- 其他 TypeScript 项目 → pyflow-typescript-pro

**Tool Type**: Task (subagent_type)

**前置步骤**: 读取合规文档
```python
constitution = Read("./pjflow/constitution.md")
requirements = Read("./pjflow/{{VERSION_DIR}}/requirements.md")
```

**执行**: 实现所有功能使测试通过

**调用**:
```
Task(
    subagent_type="pyflow-frontend-developer",  // ← Next.js/React 时使用
    subject="实现功能使测试通过",
    description="""
    实现所有功能使测试通过

    ## 强制约束（必须遵守）

    ### 项目宪法
    {constitution}

    ### 需求文档
    {requirements}

    违反上述约束的代码将被拒绝！
    """,
    activeForm="实现功能"
)
```

**后置步骤**: 合规检查
```bash
python .claude/skills/projectflow-executor/scripts/check_compliance.py \
    --language typescript \
    --version-dir {{VERSION_DIR}} \
    --phase green
```

**CHECKLIST**:
- [ ] All features implemented
- [ ] All tests pass
- [ ] Code follows constitution
- [ ] Compliance: Code within Requirements scope, follows Constitution standards
- [ ] Compliance check passed
- [ ] Compliance report generated

---

#### Phase 4.3: REFACTOR - 重构代码

**Tool**: pyflow-typescript-pro

**Tool Type**: Task (subagent_type)

**前置步骤**: 读取合规文档
```python
constitution = Read("./pjflow/constitution.md")
requirements = Read("./pjflow/{{VERSION_DIR}}/requirements.md")
```

**执行**: 优化代码结构和质量

**调用**:
```
Task(
    subagent_type="pyflow-typescript-pro",
    subject="重构优化代码",
    description="""
    优化代码结构和质量

    ## 强制约束（必须遵守）

    ### 项目宪法
    {constitution}

    ### 需求文档
    {requirements}

    违反上述约束的代码将被拒绝！
    """,
    activeForm="重构优化"
)
```

**后置步骤**: 合规检查
```bash
python .claude/skills/projectflow-executor/scripts/check_compliance.py \
    --language typescript \
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

**Tool**: pyflow-test-automator

**前置步骤**: 读取合规文档
```python
constitution = Read("./pjflow/constitution.md")
requirements = Read("./pjflow/{{VERSION_DIR}}/requirements.md")
```

**调用**:
```
Task(
    subagent_type="pyflow-test-automator",
    subject="生成完整测试套件",
    description="""
    为 {{GOAL}} 生成单元测试、集成测试、性能测试、安全测试

    ## 🚨 强制约束（必须遵守）

    ### 项目宪法
    {constitution}

    ### 需求文档
    {requirements}

    **重要**: 违反上述约束的代码/测试将被拒绝！
    """,
    activeForm="生成测试套件"
)
```

**后置步骤**: 合规检查
```bash
python .claude/skills/projectflow-executor/scripts/check_compliance.py \
    --language typescript \
    --version-dir {{VERSION_DIR}} \
    --phase red
```

**CHECKLIST**:
- [ ] Unit tests generated
- [ ] Integration tests defined
- [ ] Performance tests defined
- [ ] Security tests defined
- [ ] Compliance: Tests cover Requirements and Constitution standards
- [ ] Compliance check passed
- [ ] Compliance report generated

---

#### Phase 4.2: GREEN - 基础实现

**Tool**: pyflow-typescript-pro (或 pyflow-frontend-developer，如果项目类型是 Next.js/React)

**Agent 选择逻辑**：
根据项目类型选择 agent：
- Next.js/React 项目 → pyflow-frontend-developer
- Express 项目 → pyflow-typescript-pro
- 其他 TypeScript 项目 → pyflow-typescript-pro

**前置步骤**: 读取合规文档
```python
constitution = Read("./pjflow/constitution.md")
requirements = Read("./pjflow/{{VERSION_DIR}}/requirements.md")
```

**调用**:
```
Task(
    subagent_type="pyflow-frontend-developer",  // ← Next.js/React 时使用
    subject="实现基础功能",
    description="""
    实现所有功能使测试通过

    ## 强制约束（必须遵守）

    ### 项目宪法
    {constitution}

    ### 需求文档
    {requirements}

    违反上述约束的代码将被拒绝！
    """,
    activeForm="实现基础功能"
)
```

**后置步骤**: 合规检查
```bash
python .claude/skills/projectflow-executor/scripts/check_compliance.py \
    --language typescript \
    --version-dir {{VERSION_DIR}} \
    --phase green
```

**CHECKLIST**:
- [ ] Basic implementation completed
- [ ] All unit tests pass
- [ ] Code follows constitution
- [ ] Compliance: Code within Requirements scope, follows Constitution standards
- [ ] Compliance check passed
- [ ] Compliance report generated

---

#### Phase 4.3: GREEN - 异步优化（如需要）

**Tool**: pyflow-typescript-pro

**前置步骤**: 读取合规文档
```python
constitution = Read("./pjflow/constitution.md")
requirements = Read("./pjflow/{{VERSION_DIR}}/requirements.md")
```

**执行**: 添加异步支持提高性能

**调用**:
```
Task(
    subagent_type="pyflow-typescript-pro",
    subject="添加异步支持以提高性能",
    description="""
    添加异步/并发支持提高性能

    ## 强制约束（必须遵守）

    ### 项目宪法
    {constitution}

    ### 需求文档
    {requirements}

    违反上述约束的代码将被拒绝！
    """,
    activeForm="优化异步性能"
)
```

**后置步骤**: 合规检查
```bash
python .claude/skills/projectflow-executor/scripts/check_compliance.py \
    --language typescript \
    --version-dir {{VERSION_DIR}} \
    --phase async
```

**CHECKLIST**:
- [ ] Async patterns implemented
- [ ] All tests still pass
- [ ] Performance improved
- [ ] Compliance: Async patterns follow Constitution requirements
- [ ] Compliance check passed
- [ ] Compliance report generated

**Skip if**: `{{PROJECT_STATUS}}` == new 或项目不需要异步

---

#### Phase 4.4: GREEN - 性能优化

**Tool**: pyflow-typescript-performance-engineer

**前置步骤**: 读取合规文档
```python
constitution = Read("./pjflow/constitution.md")
requirements = Read("./pjflow/{{VERSION_DIR}}/requirements.md")
```

**执行**: 分析并优化性能瓶颈

**调用**:
```
Task(
    subagent_type="pyflow-typescript-performance-engineer",
    subject="分析并优化性能瓶颈",
    description="""
    分析并优化性能瓶颈

    ## 强制约束（必须遵守）

    ### 项目宪法
    {constitution}

    ### 需求文档
    {requirements}

    违反上述约束的代码将被拒绝！
    """,
    activeForm="优化性能"
)
```

**后置步骤**: 合规检查
```bash
python .claude/skills/projectflow-executor/scripts/check_compliance.py \
    --language typescript \
    --version-dir {{VERSION_DIR}} \
    --phase performance
```

**CHECKLIST**:
- [ ] Performance profiled
- [ ] Bottlenecks identified
- [ ] Optimizations applied
- [ ] Performance targets met
- [ ] Compliance: Performance optimizations meet Requirements targets
- [ ] Compliance check passed
- [ ] Compliance report generated

**Skip if**: 项目没有性能要求

---

#### Phase 4.5: REFACTOR - 深度优化

**Tool**: pyflow-typescript-performance-engineer

**前置步骤**: 读取合规文档
```python
constitution = Read("./pjflow/constitution.md")
requirements = Read("./pjflow/{{VERSION_DIR}}/requirements.md")
```

**执行**: 应用高级优化技术

**调用**:
```
Task(
    subagent_type="pyflow-typescript-performance-engineer",
    subject="深度性能优化",
    description="""
    应用高级优化技术

    ## 强制约束（必须遵守）

    ### 项目宪法
    {constitution}

    ### 需求文档
    {requirements}

    违反上述约束的代码将被拒绝！
    """,
    activeForm="深度优化"
)
```

**后置步骤**: 合规检查
```bash
python .claude/skills/projectflow-executor/scripts/check_compliance.py \
    --language typescript \
    --version-dir {{VERSION_DIR}} \
    --phase deep-refactor
```

**CHECKLIST**:
- [ ] Advanced optimizations applied
- [ ] Code quality excellent
- [ ] All tests still pass
- [ ] Performance significantly improved
- [ ] Compliance: Refactor preserves Constitution compliance
- [ ] Compliance check passed
- [ ] Compliance report generated

---

#### Phase 4.6: REFACTOR - 最终清理

**Tool**: pyflow-typescript-pro

**前置步骤**: 读取合规文档
```python
constitution = Read("./pjflow/constitution.md")
requirements = Read("./pjflow/{{VERSION_DIR}}/requirements.md")
```

**执行**: 清理代码、更新文档

**调用**:
```
Task(
    subagent_type="pyflow-typescript-pro",
    subject="最终代码清理",
    description="""
    清理代码、更新文档、确保代码质量

    ## 强制约束（必须遵守）

    ### 项目宪法
    {constitution}

    ### 需求文档
    {requirements}

    违反上述约束的代码将被拒绝！
    """,
    activeForm="清理代码"
)
```

**后置步骤**: 合规检查
```bash
python .claude/skills/projectflow-executor/scripts/check_compliance.py \
    --language typescript \
    --version-dir {{VERSION_DIR}} \
    --phase final
```

**CHECKLIST**:
- [ ] Code cleaned up
- [ ] Documentation updated
- [ ] All tests pass
- [ ] Code quality excellent
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
npm test
npm run lint
npm run typecheck

# 运行完整合规检查
python .claude/skills/projectflow-executor/scripts/check_compliance.py \
    --language typescript \
    --version-dir {{VERSION_DIR}} \
    --phase review
```

**CHECKLIST**:
- [ ] All tests pass (100%)
- [ ] Code style checks pass (eslint)
- [ ] Type checks pass (tsc)
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

**Tool**: pyflow-code-reviewer

**Tool Type**: Task (subagent_type)

**调用**:
```
Task(
    subagent_type="pyflow-code-reviewer",
    subject="审核代码",
    description="""
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
| Phase 2.3 (系统文件) 完成后 | package.json 等系统文件 checkbox |
| Phase 2.4 (项目文件) 完成后 | 占位文件创建 checkbox |
| Phase 2.5 (虚拟环境) 完成后 | 依赖安装 checkbox |
| Phase 3.1 完成后 | 工作环境相关 checkbox |
| Phase 3.2 完成后 | 工作环境相关 checkbox |
| Phase 3.3 完成后 | 工作环境相关 checkbox |
| Phase 3.4 完成后 | 工作环境相关 checkbox |
| Phase 4 (Simple) 完成后 | TDD 执行相关 checkbox |
| Phase 4.1 (Medium) 完成后 | 测试套件生成 checkbox |
| Phase 4.2 (Medium) 完成后 | 基础实现 checkbox |
| Phase 4.3 (Medium) 完成后 | 异步优化 checkbox |
| Phase 4.4 (Medium) 完成后 | 性能优化 checkbox |
| Phase 4.5 (Medium) 完成后 | 深度优化 checkbox |
| Phase 4.6 (Medium) 完成后 | 最终清理 checkbox |
| Phase 4 (Complex) 完成后 | 完整测试套件生成 checkbox |
| Phase 4.2 (Complex) 完成后 | 基础实现 checkbox |
| Phase 4.3 (Complex) 完成后 | 异步优化 checkbox |
| Phase 4.4 (Complex) 完成后 | 性能优化 checkbox |
| Phase 4.5 (Complex) 完成后 | 深度优化 checkbox |
| Phase 4.6 (Complex) 完成后 | 最终清理 checkbox |
| Phase 5 (Simple) 完成后 | 质量检查通过 checkbox |
| Phase 5 (Simple) 完成后 | 代码审核完成 checkbox |
| Phase 5 (Medium/Complex) 完成后 | Git 提交完成 checkbox |

**使用示例**:

```typescript
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

**Phase 4 执行**: 单次 `pyflow-tdd-cycle --single-cycle`

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
- 扩展 TDD 循环（异步、性能）
- 深度审核
- 安全审核
- 完整 CI/CD

**Phase 4 执行**: RED → GREEN → 异步优化 → 性能优化 → 深度优化 → 最终清理

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

```typescript
// 调用 pyflow-brainstorming 探索需求
Skill(skill="pyflow-brainstorming", args="{{GOAL}}")

// 调用 pyflow-constitution 创建宪法
Skill(skill="pyflow-constitution", args="{{GOAL}}")

// 调用 pyflow-tdd-cycle 执行 TDD
Skill(skill="pyflow-tdd-cycle", args="{{GOAL}} --single-cycle")

// 调用 code-reviewer 审核代码
Task(
    subagent_type="pyflow-code-reviewer",
    subject="审核代码",
    description="审核整个代码库"
)
```

### Task 调用（Agent）

```typescript
// 调用 pyflow-test-automator 生成测试
Task(
    subagent_type="pyflow-test-automator",
    subject="生成测试套件",
    description="为 {{GOAL}} 生成完整测试套件"
)

// 调用 pyflow-typescript-pro 实现 TypeScript 功能
Task(
    subagent_type="pyflow-typescript-pro",
    subject="实现功能使测试通过",
    description="实现所有功能使测试通过"
)

// 调用 pyflow-frontend-developer 实现 React/Next.js 功能
Task(
    subagent_type="pyflow-frontend-developer",
    subject="实现前端功能",
    description="实现 React/Next.js 功能使测试通过"
)

// 调用 pyflow-typescript-performance-engineer 优化性能
Task(
    subagent_type="pyflow-typescript-performance-engineer",
    subject="优化性能",
    description="分析并优化性能瓶颈"
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

# 创建 .gitignore
cat > .gitignore << EOF
# Dependencies
node_modules/

# Testing
coverage/
.nyc_output/

# Build
dist/
build/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
EOF

# 安装依赖
npm install

# 检测环境
node scripts/detect_environment.js

# 创建目录
mkdir -p src/{api/v1,core,models}

# 运行测试
npm test

# 代码格式化
npm run format

# Git 提交
git add .
git commit -m "feat: implement feature"
```

---

## 合规性检查说明

**自动化合规检查**: 每个重要阶段完成后，系统会自动运行合规检查脚本

### 检查内容

1. **代码风格**: eslint 检查
2. **类型注解**: tsc 类型检查
3. **测试覆盖率**: vitest 覆盖率检查
4. **错误处理**: 空catch块检测
5. **宪法合规**: 代码是否遵循项目宪法规则
6. **需求合规**: 代码是否超出需求范围

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
**用途**: ProjectFlow Planner - TypeScript 完整计划模板
**适用语言**: TypeScript (package.json, tsconfig.json)
**更新内容**: 添加合规性检查集成

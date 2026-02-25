---
name: projectflow-executor
description: |
  读取 pjflow/{VERSION_DIR}/task_plan.md，逐阶段执行计划，更新 CHECKLIST.md 和 progress.md。
  触发条件: 由 projectflow-planner 调用，或用户说"继续执行"
  核心职责: 智能加载执行上下文（需求+宪法+模板），逐阶段执行计划，更新状态
  编排原则: ✅ 可创建脚手架 | ❌ 禁止编写业务逻辑 | ❌ 语言无关 | 🧠 充分利用 LLM 理解能力
---

# ProjectFlow Executor

## 🚨 CRITICAL: 编排者禁令（违反即失败）

### 三条铁律

1. **❌ 禁止手动编写业务逻辑**
   - 后果：TDD 流程失效，代码质量失控
   - 正确：调用 `pyflow-tdd-cycle` 或对应语言的 TDD 工具

2. **❌ 禁止在 tool 执行时自己操作**
   - 后果：状态混乱，无法追踪进度
   - 正确：等待 tool 返回，验证结果

3. **❌ 禁止跳过 CHECKLIST 更新**
   - 后果：进度丢失，无法追溯
   - 正确：每个 Phase 完成后立即更新

### 快速判断

```
这是脚手架吗？（所有项目都需要）
├─ 是 → Write/Bash 工具 ✅
└─ 否（含业务功能）→ TDD 工具 ❌
```

---

## 快速开始

```
读取 task_plan.md → 找下一个 Phase → 执行 → 验证 → 更新 → 循环
```

详见 [EXECUTION_STEPS.md](references/EXECUTION_STEPS.md)

## 核心概念

### 编排者 vs 执行者

| 编排者 (你) | 执行者 (Tool/Skill) |
|------------|-------------------|
| 调用工具 | 实现功能 |
| 验证结果 | 编写代码 |
| 更新状态 | 运行测试 |
| 协调流程 | 处理细节 |

### 脚手架 vs 业务逻辑

**脚手架** (你可以创建):
- 项目目录结构
- 配置文件 (pyproject.toml, package.json, go.mod)
- .gitignore
- README.md 模板

**业务逻辑** (必须用 TDD):
- 功能代码
- API 路由
- 数据模型
- 业务规则

## 执行流程

```
Step 1: 读取 task_plan.md，找下一个 pending Phase
Step 2: 智能加载执行上下文（三层信息源）
Step 3: 判断脚手架 vs 业务逻辑 → 选择工具
Step 4: 调用 Tool → 等待返回 ⏸️
Step 5: 验证结果
Step 6: 更新 CHECKLIST.md 和 progress.md
Step 7: 标记 Phase 完成 → 回到 Step 1
```

> ⚠️ **Step 2 是关键**: 根据当前 Phase 类型，智能选择信息来源（需求/宪法/模板）

### 三层信息源

| 信息源 | 内容 | 用途 |
|--------|------|------|
| **requirements.md** | 项目特定配置（依赖、目录结构、功能规格） | 要做什么 |
| **constitution.md** | 质量约束（类型安全、TDD、代码风格） | 怎么做 |
| **template.md** | 通用脚手架（中文镜像源、工具配置） | 语言特定配置 |

### Phase 4/5 特殊规则

> 🚨 **Phase 4 (TDD 执行) 和 Phase 5 (质量审核) 必须注入宪法和需求！**

**强制要求**:
- ✅ 每个 Phase 4/5 子阶段执行前，必须读取文档
- ✅ 必须将文档内容注入到 Tool/Agent 的调用参数中
- ✅ 不得跳过文档注入步骤
- ❌ 未注入文档的调用视为违规

**注入格式**:
```python
# 读取文档
constitution = Read("pjflow/constitution.md")
requirements = Read(f"pjflow/{VERSION_DIR}/requirements.md")

# 构建增强提示
enhanced_prompt = f"""
{original_prompt}

## 🚨 强制约束（必须遵守）

### 项目宪法 (Constitution)
{constitution}

### 需求文档 (Requirements)
{requirements}

**重要**: 违反上述约束的代码/测试将被拒绝！必须确保所有代码符合宪法要求和需求范围。
"""
```

详细步骤见 [EXECUTION_STEPS.md](references/EXECUTION_STEPS.md)

### Phase 执行策略

| Phase | 信息来源 | 执行方式 | 说明 |
|-------|---------|---------|------|
| 0, 1 | - | 直接执行 | 文档还不存在，生成文档 |
| 2.0, 2.1, 2.5 | 🔧 模板 | 直接执行 | 通用逻辑（Git、虚拟环境） |
| 2.2, 2.3, 2.4 | 📋 需求 + 🔧 模板 | LLM 理解并合并 | 核心脚手架（目录、配置、文件） |
| 3.1-3.4 | 📋 需求 | LLM 理解 | 添加功能（分支、依赖、新文件） |
| 4 | 📋 需求 + 📜 宪法 | 注入到 TDD | 不是自己执行，而是约束 TDD 工具 |
| 5 | - | 运行合规检查 | 验证代码是否符合文档 |

## CHECKLIST 更新

每个 Phase 完成后必须更新对应的 checkbox。

| Phase | 更新内容 |
|-------|---------|
| Phase 0 | 需求分析 checkbox |
| Phase 1 | 项目规则 checkbox |
| Phase 2 | 项目准备 checkbox |
| Phase 3 | 工作环境 checkbox |
| Phase 4 | TDD 执行 checkbox |
| Phase 5 | 质量审核 checkbox |

**方法**: `Edit(file_path, old_string="- [ ] ...", new_string="- [x] ...")`

详见 [CHECKLIST_GUIDE.md](references/CHECKLIST_GUIDE.md)

## 合规检查

Phase 4/5 后自动执行合规检查。

```bash
python .claude/skills/projectflow-executor/scripts/check_compliance.py \
    --version-dir {VERSION_DIR}
```

详见 [COMPLIANCE.md](references/COMPLIANCE.md)

## 目录结构

```
pjflow/
├── constitution.md              # 共享宪法
├── v0_initial/
│   ├── task_plan.md
│   ├── requirements.md
│   ├── CHECKLIST.md
│   ├── progress.md
│   ├── findings.md
│   └── compliance_report.md
├── v1_add_feature/
│   └── ...
└── vN_add_feature/
    └── ...
```

详见 [DIRECTORY_STRUCTURE.md](references/DIRECTORY_STRUCTURE.md)

## 语言无关性

Executor 适用于任何语言，通过对应的 TDD 工具执行业务逻辑。

| 语言 | TDD 工具 | 配置文件 |
|------|---------|---------|
| Python | pyflow-tdd-cycle | pyproject.toml |
| TypeScript | tdd-cycle | package.json |
| Go | go-tdd-cycle | go.mod |
| Rust | cargo-tdd-cycle | Cargo.toml |
| Java | junit-tdd-cycle | pom.xml |

---

## 参考资料

| 文档 | 内容 | 何时阅读 |
|------|------|---------|
| [EXECUTION_STEPS.md](references/EXECUTION_STEPS.md) | 详细的 7 步执行流程 | 首次使用或遇到问题 |
| [CHECKLIST_GUIDE.md](references/CHECKLIST_GUIDE.md) | CHECKLIST 更新详细指南 | Phase 完成后 |
| [COMPLIANCE.md](references/COMPLIANCE.md) | 合规检查完整说明 | Phase 4/5 执行前 |
| [DIRECTORY_STRUCTURE.md](references/DIRECTORY_STRUCTURE.md) | 目录结构和版本管理 | 项目结构变化时 |
| [REQUIREMENTS_COMPLIANCE.md](references/REQUIREMENTS_COMPLIANCE.md) | 需求文档合规指南 | Phase 0/5 执行前 |

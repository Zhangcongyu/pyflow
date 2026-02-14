---
name: projectflow-planner
description: 根据三维参数（新/老 + 简单/中等/复杂 + 语言类型）检测项目环境，读取综合模板，生成具体可执行的 plan.md
---

# ProjectFlow Planner

## 触发条件

由 `projectflow-router` 调用，传递三维参数和用户需求

接收参数: `--new/--add-feature` + `--simple/--medium/--complex` + `--python/--typescript/--go` + 用户原始需求 + 当前路径

## 核心职责

1. 检测环境 → 读取模板 → 生成 plan.md → 调用 executor
2. 确定版本目录（pjflow/v{N}_{feature}）
3. 根据 `{{PROJECT_STATUS}}` 和 `{{COMPLEXITY}}` 选择 Phase

## 核心流程

```
三维参数输入
   ↓
Step 1: 检测项目环境
   ↓
Step 2: 确定版本目录
   ↓
Step 3: 读取综合模板
   ↓
Step 4: 转化模板内容
   ↓
Step 5: 生成 task_plan.md
   ↓
Step 6: 调用 executor
```

## Step 1: 检测项目环境

```bash
python .claude/skills/projectflow-planner/scripts/detect_environment.py --json
```

**输出字段**: git, virtual_env, project_structure, project_age（详见 [ENVIRONMENT_FIELDS.md](references/ENVIRONMENT_FIELDS.md)）

## Step 2: 确定版本目录

- **new** → `pjflow/v0_initial`
- **add-feature** → `pjflow/v{N}_{feature_name}`（N 自动递增）

详见 [VERSION_NAMING.md](references/VERSION_NAMING.md)

## Step 3: 读取综合模板

| 语言 | 模板文件 | 复杂度支持 |
|------|---------|------------|
| Python | `python-complete-template.md` | ✅ simple/medium/complex |
| TypeScript | `typescript-complete-template.md` | ✅ simple/medium/complex |
| Go | `go-template.md` | ⚠️ 基础结构 |

## Step 4: 转化模板

### 变量替换

| 变量 | 替换为 | 来源 |
|--------|--------|------|
| `{{GOAL}}` | 用户原始需求 | router 传入 |
| `{{PROJECT_STATUS}}` | new / add-feature | router 传入 |
| `{{COMPLEXITY}}` | simple / medium / complex | router 传入 |
| `{{LANGUAGE}}` | python / typescript / go | router 传入 |
| `{{VERSION_DIR}}` | v0_initial / v{N}_{feature} | Step 2 计算 |

### Phase 选择

| Phase | new | add-feature |
|-------|-----|-------------|
| Phase 0: 需求互动 | medium/complex | medium/complex |
| Phase 1: 项目规则 | ✅ | ❌ |
| Phase 2: 项目构建 | ✅ | ❌ |
| Phase 3: 工作树准备 | ❌ | ✅ |
| Phase 4: TDD 执行 | ✅ | ✅ |
| Phase 5: 质量审核 | ✅ | ✅ |

## Step 5-6: 生成计划并调用的执行

详见 [EXECUTION_GUIDE.md](references/EXECUTION_GUIDE.md)

---

**版本**: 4.1.0
**更新**: 简洁化 SKILL.md，将详细内容移到 references/

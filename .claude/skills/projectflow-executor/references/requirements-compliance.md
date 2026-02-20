# 需求文档合规性指南

**用途**: 需求文档版本化的合规性检查指南

**适用范围**: Phase 0 (需求互动) + Phase 5 (质量审核)

---

## 核心原则

**需求文档是项目的唯一真实来源**，必须完整、准确、可追溯。

在每个版本中，**必须**：

1. **创建** 独立的需求文档 `pjflow/{VERSION_DIR}/requirements.md`
2. **维护** 需求文档与实际功能的一致性
3. **追溯** 每个版本的需求变更历史
4. **验证** 需求覆盖率

---

## 版本化需求文档结构

### 新项目 (v0_initial)

```markdown
# Requirements

**Project Type**: new
**Complexity**: simple/medium/complex
**Goal**: [用户原始需求]

---

## Project Overview

[项目整体描述]

## Core Features

### Feature 1
- Description:
- Acceptance Criteria:
- Priority:

## Technical Requirements

- Performance requirements:
- Security requirements:
- Compatibility requirements:

## Success Criteria

1. [成功标准 1]
2. [成功标准 2]
3. [成功标准 3]
```

### 增加功能 (v1_add_feature)

```markdown
# Requirements

**Project Type**: add-feature
**Complexity**: simple/medium/complex
**Goal**: [新增功能需求]

---

## Feature Overview

[新功能概述]

## Changes Required

### New Files
- [新文件列表]

### Modified Files
- [修改文件列表]

## Acceptance Criteria

1. [验收标准 1]
2. [验收标准 2]
3. [验收标准 3]

## Testing Requirements

- Unit tests:
- Integration tests:
```

---

## 合规检查清单

### 需求完整性检查

```
□ 需求文档存在于版本目录
□ 文档包含项目类型和复杂度
□ 文档包含明确的目标描述
□ 功能需求详细列出
□ 验收标准明确定义
□ 技术需求完整描述
□ 成功标准可测量
```

### 需求覆盖率验证

```
□ 所有功能需求都有对应测试
□ 所有验收标准都可验证
□ 技术需求都已在设计中考虑
□ 成功标准都有度量方式
```

### 功能蔓延检测

```
□ 实际功能与需求文档一致
□ 没有未经文档批准的额外功能
□ 需求变更已记录在 progress.md
□ 功能优先级得到遵守
```

### 技术方案符合度验证

```
□ 架构设计符合需求约束
□ 技术选型符合技术需求
□ 性能指标可达成
□ 安全需求已实现
```

---

## 需求文档与宪法的关系

| 文档 | 作用 | 位置 |
|------|------|------|
| constitution.md | 项目规则共享 | pjflow/constitution.md (所有版本共享) |
| requirements.md | 需求版本化 | pjflow/{VERSION_DIR}/requirements.md (每个版本独立) |

**设计原则**:
- Constitution 是项目的"游戏规则"，很少变化，因此共享
- Requirements 是每个版本的"需求清单"，经常变化，因此版本化

---

## 需求变更管理

### 变更流程

1. **记录变更**: 在 progress.md 中记录需求变更
2. **更新文档**: 更新对应版本的 requirements.md
3. **验证影响**: 评估变更对现有功能的影响
4. **重新测试**: 对变更部分重新执行测试

### 变更类型

| 变更类型 | 处理方式 | 文档更新 |
|----------|----------|----------|
| 新增功能 | 创建新版本目录 | 新 requirements.md |
| 修改需求 | 更新当前版本 | 更新 requirements.md |
| 删除功能 | 标记废弃 | 更新 requirements.md |
| Bug 修复 | 不修改需求 | 不更新 |

---

## 向后兼容性迁移

### 旧结构

```
pjflow/
├── constitution.md
├── requirements.md        # 共享，所有版本使用同一个
└── v0_initial/
    └── task_plan.md
```

### 新结构

```
pjflow/
├── constitution.md
├── requirements.md.bak    # 旧文件备份
└── v0_initial/
    ├── requirements.md    # 新：版本化需求
    └── task_plan.md
```

### 迁移脚本

```bash
python .claude/skills/projectflow-executor/scripts/migrate_requirements.py
```

**迁移过程**:
1. 检测当前结构类型
2. 复制共享 requirements.md 到各版本目录
3. 重命名旧文件为 requirements.md.bak
4. 验证迁移结果

---

## 常见违规类型

### 1. 需求缺失

- **症状**: 版本目录没有 requirements.md
- **影响**: 无法追溯需求，无法验证合规
- **修复**: 根据实际功能补充需求文档

### 2. 需求不完整

- **症状**: 需求文档内容少于 50 字
- **影响**: 需求不明确，开发方向模糊
- **修复**: 补充详细的需求描述

### 3. 功能蔓延

- **症状**: 实际功能超出需求文档范围
- **影响**: 范围失控，进度延误
- **修复**: 更新需求文档或删除未批准的功能

### 4. 验收标准模糊

- **症状**: 验收标准无法验证或测量
- **影响**: 无法判断完成状态
- **修复**: 使用可测量的验收标准

---

## 合规检查命令

### 检查单个版本

```bash
python .claude/skills/projectflow-executor/scripts/check_compliance.py \
    --version-dir v0_initial
```

### 检查所有版本

```bash
for version in pjflow/v*; do
    python .claude/skills/projectflow-executor/scripts/check_compliance.py \
        --version-dir $(basename $version)
done
```

### 查看合规报告

```bash
cat pjflow/v0_initial/compliance_report.md
```

---

**文档版本**: 1.0.0
**更新时间**: 2026-02-20
**用途**: 需求文档合规性检查指南
**适用阶段**: Phase 0 + Phase 5

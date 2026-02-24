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
- Performance:
- Security:
- Compatibility:

## Success Criteria
1. [可测量的成功标准]
```

### 增加功能 (vN_add_feature)

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
- [文件列表]

### Modified Files
- [文件列表]

## Acceptance Criteria
1. [可验证的标准]

## Testing Requirements
- Unit tests:
- Integration tests:
```

---

## 合规检查清单

| 检查项 | 说明 |
|-------|------|
| 文档存在性 | `pjflow/{VERSION_DIR}/requirements.md` 存在 |
| 元数据完整 | 包含项目类型、复杂度、目标 |
| 功能需求详细 | 核心功能列表完整 |
| 验收标准明确 | 可验证、可测量 |
| 技术需求完整 | 性能、安全、兼容性已定义 |
| 成功标准可测量 | 有明确的完成判断标准 |

---

## 需求文档与宪法的关系

| 文档 | 作用 | 位置 |
|------|------|------|
| constitution.md | 项目规则（共享） | `pjflow/constitution.md` |
| requirements.md | 需求版本化 | `pjflow/{VERSION_DIR}/requirements.md` |

- Constitution: 项目的"游戏规则"，很少变化，所有版本共享
- Requirements: 每个版本的"需求清单"，经常变化，版本化存储

---

## 需求变更管理

### 变更流程

1. **记录变更**: 在 `progress.md` 中记录
2. **更新文档**: 更新 `requirements.md`
3. **验证影响**: 评估对现有功能的影响
4. **重新测试**: 对变更部分重新测试

### 变更类型

| 类型 | 处理方式 | 文档更新 |
|------|---------|---------|
| 新增功能 | 创建新版本目录 | 新 `requirements.md` |
| 修改需求 | 更新当前版本 | 更新 `requirements.md` |
| 删除功能 | 标记废弃 | 更新 `requirements.md` |
| Bug 修复 | 不修改需求 | 不更新 |

---

## 常见违规类型

| 类型 | 症状 | 修复 |
|------|------|------|
| 需求缺失 | 版本目录没有 `requirements.md` | 补充需求文档 |
| 需求不完整 | 内容少于 50 字 | 补充详细描述 |
| 功能蔓延 | 实际功能超出需求范围 | 更新文档或删除功能 |
| 验收标准模糊 | 无法验证或测量 | 使用可测量标准 |

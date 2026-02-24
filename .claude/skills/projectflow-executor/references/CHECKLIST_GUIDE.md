# CHECKLIST 更新指南

## 更新时机

每个 Phase 完成后必须更新 CHECKLIST.md。

| Phase | 更新时机 | 更新内容 |
|-------|---------|---------|
| Phase 0 | brainstorming 完成后 | 需求分析相关 checkbox |
| Phase 1 | constitution 创建后 | 项目规则相关 checkbox |
| Phase 2 | 脚手架创建后 | 项目准备相关 checkbox |
| Phase 3 | worktree 创建后 | 工作环境相关 checkbox |
| Phase 4 | TDD 完成后 | TDD 执行相关 checkbox |
| Phase 5 | 质量审核完成后 | 质量审核和 Git 相关 checkbox |

## 更新方法

### 使用 Edit 工具

```python
Edit(
    file_path="pjflow/{VERSION_DIR}/CHECKLIST.md",
    old_string="- [ ] Checkbox 描述",
    new_string="- [x] Checkbox 描述"
)
```

### 验证 CHECKLIST 已更新

```bash
# 确认至少有一个 [x] 标记
grep -q "\[x\]" pjflow/{VERSION_DIR}/CHECKLIST.md && echo "✅ CHECKLIST 已更新" || echo "❌ CHECKLIST 未更新"

# 统计已完成的项
echo "已完成: $(grep '\[x\]' pjflow/{VERSION_DIR}/CHECKLIST.md | wc -l) 项"
```

## 常见错误

| 错误 | 后果 | 正确做法 |
|------|------|---------|
| 忘记更新 CHECKLIST | Phase 视为未完成 | 每个 Phase 完成后立即更新 |
| 更新错误的 checkbox | 进度追踪混乱 | 更新与当前 Phase 对应的 checkbox |
| 手动编辑文件 | 可能引入格式错误 | 使用 Edit 工具 |

**重要**: 未更新 CHECKLIST 视为 Phase 未完成！

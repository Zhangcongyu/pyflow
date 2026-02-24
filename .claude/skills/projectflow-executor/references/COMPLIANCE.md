# 合规检查指南

## 何时执行

Phase 4 (TDD 执行) 和 Phase 5 (质量审核) 完成后自动执行。

## 支持的语言

| 语言 | 检查器 | 工具 |
|------|--------|------|
| Python | `PythonComplianceChecker` | ruff, mypy, pytest |
| TypeScript | `TypeScriptComplianceChecker` | eslint, tsc, vitest |
| Go | `GoComplianceChecker` | gofmt, go vet, go test |

## 合规检查内容

### 1. 宪法合规 (constitution.md)
- 文件存在性检查
- Coding Standards 章节检查

### 2. 需求文档合规 (requirements.md)
- 文件存在性检查
- 内容完整性检查

### 3. 代码风格检查
- Python: ruff
- TypeScript: eslint
- Go: gofmt + go vet

### 4. 类型注解检查
- Python: mypy
- TypeScript: tsc
- Go: interface{} 过度使用

### 5. 测试覆盖率检查
- Python: pytest --cov
- TypeScript: vitest --coverage
- Go: go test -cover

### 6. 错误处理检查
- 裸 except/空 catch 块检测
- 忽略的错误返回值检测

## 执行命令

```bash
# 自动检测语言
python .claude/skills/projectflow-executor/scripts/check_compliance.py \
    --version-dir {VERSION_DIR}

# 指定语言
python .claude/skills/projectflow-executor/scripts/check_compliance.py \
    --language python \
    --version-dir {VERSION_DIR}

# 查看帮助
python .claude/skills/projectflow-executor/scripts/check_compliance.py --help
```

## 输出位置

`pjflow/{VERSION_DIR}/compliance_report.md`

## Phase 4/5 特殊合规检查

### 注入验证

**检查 executor 是否正确注入宪法和需求**:

```bash
# 检查 task_plan.md 中的 Phase 4/5
grep -A 20 "Phase 4:" pjflow/{VERSION_DIR}/task_plan.md | \
    grep -E "(constitution|requirements|强制约束)"
```

**预期结果**: 每个 Phase 4/5 子阶段应包含:
- 文档读取步骤
- 增强提示构建步骤
- 注入到 Tool 调用的参数

### 输出验证

**检查 agent 输出是否遵循约束**:

1. **宪法符合度**: 对照 constitution.md 中的规则
   - 类型注解要求
   - 代码风格标准
   - 测试覆盖率要求

2. **需求覆盖度**: 对照 requirements.md 中的功能列表
   - 所有功能已实现
   - 所有功能有测试覆盖

3. **功能蔓延检查**: 是否有超出需求的功能

---

## 违规处理

| 级别 | 处理方式 |
|------|---------|
| Critical | 必须修复才能继续 |
| High | 建议修复，可选择性继续 |
| Medium/Low | 记录但不阻止 |

## 可用脚本

| 脚本 | 用途 |
|------|------|
| `check_compliance.py` | 运行合规检查并生成报告 |
| `document_manager.py` | 管理版本化需求文档 |
| `base_checker.py` | 基础检查器抽象类 |
| `python_checker.py` | Python 合规检查器 |
| `typescript_checker.py` | TypeScript 合规检查器 |
| `go_checker.py` | Go 合规检查器 |
| `checker_factory.py` | 检查器工厂 |
| `compliance_reporter.py` | 报告生成器 |

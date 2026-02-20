# File Counter Constitution

**Version**: 1.0.0 | **Ratified**: 2026-02-20 | **Last Amended**: 2026-02-20

## Project Identity

**Description**: 文件计数器工具 - 统计指定目录下的文件数量，按扩展名分类

**Scope**: 命令行工具，递归扫描目录并输出文件统计结果

**Complexity Level**: Simple

---

## Core Principles

### TYPE_SAFETY_AND_CODE_QUALITY

**Name**: 类型安全与代码质量

**Rules**:
- 所有函数 MUST 使用类型注解 (type hints)
- 禁止使用 `Any` 类型，除非有明确注释说明原因
- 所有公共函数 MUST 包含 docstring
- 代码行长度限制 88 字符 (ruff 默认)
- 使用 ruff 进行代码格式化和 linting

**Rationale**: 类型安全提高代码可维护性，减少运行时错误。明确的类型注解使 IDE 支持更好，代码审查更高效。

### TEST_DRIVEN_DEVELOPMENT

**Name**: 测试驱动开发

**Rules**:
- 所有业务逻辑 MUST 先编写测试
- 测试覆盖率 MUST 达到 90% 以上
- 使用 pytest 作为测试框架
- 每个 test 文件 MUST 对应源码模块
- 禁止提交未通过测试的代码

**Rationale**: TDD 确保代码质量，测试作为文档和回归保护。高覆盖率意味着更少的 bug 和更高的重构信心。

### SIMPLICITY

**Name**: 简单性

**Rules**:
- 优先选择最简单的解决方案
- 避免过早优化
- 单个函数职责 MUST 单一
- 避免不必要的抽象
- 代码 SHOULD 自解释，复杂逻辑需要注释

**Rationale**: Simple code is easier to understand, maintain, and debug. Premature optimization adds complexity without measurable benefit.

---

## Technical Standards

### Coding Standards

**Code Style**:
- 使用 ruff format 格式化代码
- 遵循 PEP 8 规范
- 行长度限制 88 字符
- 使用 f-string 进行字符串格式化
- 使用 pathlib 处理文件路径，禁止使用 os.path

**Type Annotations**:
- 所有函数 MUST 包含参数和返回值类型注解
- 使用 `from __future__ import annotations` 启用延迟求值
- 复杂类型使用 `typing` 模块的别名
- 禁止使用类型注释 `# type: ignore` 除非有说明
- `__all__` MUST 包含类型注解: `__all__: list[str] = [...]`

**Error Handling**:
- 使用具体的异常类型，避免裸 `except:`
- 用户输入错误 SHOULD 抛出有意义的异常
- 文件操作使用 context managers (`with` 语句)
- 资源清理 MUST 使用 context managers

**Documentation**:
- 所有公共函数 MUST 包含 Google 风格的 docstring
- 复杂逻辑 SHOULD 添加中文注释说明
- README.md MUST 包含使用示例
- 变量命名 SHOULD 清晰表达意图

---

## Governance

### Amendment Procedure
1. 提出修改建议并说明理由
2. 更新 CONSTITUTION_VERSION (遵循语义化版本)
3. 更新 LAST_AMENDED_DATE 为当前日期
4. 确保 tests/ 中所有测试仍通过
5. 提交时使用前缀 `docs:` 或 `constitution:`

### Versioning
- MAJOR: 移除或重新定义核心原则
- MINOR: 新增原则或实质性扩展
- PATCH: 澄清、措辞改进

### Compliance Review
- 每次 Phase 4/5 完成后运行合规检查
- 使用 check_compliance.py 脚本
- Critical 问题 MUST 修复才能继续
- High 问题 SHOULD 修复

---

## Validation Checklist

Before marking any phase as complete, verify:

- [ ] All functions have type annotations
- [ ] All tests pass (pytest -v)
- [ ] Code formatted (ruff format .)
- [ ] No lint errors (ruff check .)
- [ ] Test coverage >= 90% (pytest --cov)
- [ ] Type checks pass (mypy src/)
- [ ] Docstrings present on public functions
- [ ] No commented-out code
- [ ] Resources use context managers

---

**End of Constitution 1.0.0**

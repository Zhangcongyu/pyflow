# Constitution 合规性指南

**用途**: TDD 开发各阶段的 Constitution 合规性检查指南

**适用范围**: Phase 4 (TDD 执行) + Phase 5 (质量审核)

---

## 🚨 核心原则

**Constitution 是项目宪法，必须无条件遵守！**

在执行 TDD 的每个阶段时，**必须**：

1. **阅读** `./pjflow/constitution.md`
2. **遵守** 所有编码标准
3. **遵守** 所有架构原则
4. **遵守** 所有命名约定
5. **遵守** 所有技术约束
6. **遵守** 所有自定义原则

**❌ 违反 Constitution 的代码不被接受！**
**❌ 不符合 Constitution 的测试不被接受！**
**❌ 违反 Constitution 的重构不被接受！**

---

## 📋 通用检查清单

**在每个 TDD 阶段开始前，必须确认**：

```
□ 已阅读 ./pjflow/constitution.md
□ 理解所有编码标准
□ 理解所有架构原则
□ 理解所有命名约定
□ 理解所有技术约束
□ 理解所有自定义原则
```

---

## Phase 4: TDD 执行阶段

### 🔴 RED Phase 合规性要求

**Phase**: 编写失败的测试

**合规性检查点**:

```
□ 测试命名遵循 Constitution 命名约定
□ 测试结构符合 Constitution 架构原则
□ 测试覆盖 Constitution 定义的质量标准
□ 测试用例包含边界情况
```

**传递给 Agent 的提示**:

```python
"""
🛑 Constitution 合规性要求:
- 必须阅读并遵循 ./pjflow/constitution.md
- 测试命名必须遵循 Constitution 命名约定
- 测试结构必须符合 Constitution 架构原则
- 测试覆盖 Constitution 定义的质量标准
"""
```

---

### 🟢 GREEN Phase 合规性要求

**Phase**: 实现功能使测试通过

**合规性检查点**:

```
□ 代码风格遵循 Constitution
□ 类型注解符合 Constitution 标准
□ 架构设计符合 Constitution 原则
□ 所有技术约束满足
□ API 设计符合 Constitution 规范
```

**传递给 Agent 的提示**:

```python
"""
🛑 Constitution 合规性要求:
- 必须阅读并遵循 ./pjflow/constitution.md
- 代码风格必须遵循 Constitution
- 类型注解必须符合 Constitution 标准
- 架构设计必须符合 Constitution 原则
- 所有技术约束必须满足
"""
```

---

### 🔄 REFACTOR Phase 合规性要求

**Phase**: 重构代码，提高质量

**合规性检查点**:

```
□ 重构未违反 Constitution 原则
□ 代码复杂度符合 Constitution 标准
□ 类型注解仍然完整
□ 架构设计仍然符合 Constitution
□ 性能优化未违反 Constitution 约束
```

**传递给 Agent 的提示**:

```python
"""
🛑 Constitution 合规性要求:
- 重构不能违反 Constitution 原则
- 代码复杂度必须符合 Constitution 标准
- 类型注解必须保持完整
- 架构设计必须仍然符合 Constitution
- 性能优化不能违反 Constitution 约束
"""
```

---

## Phase 5: 质量审核阶段

### 📊 Constitution 合规性检查（强制）

**所有代码审核必须包含以下检查**：

#### 1. 编码标准合规

```
□ 类型注解完整度符合 Constitution 要求
□ 命名约定完全遵循 Constitution
□ 代码风格符合 Constitution 标准
```

#### 2. 架构原则合规

```
□ 分层结构符合 Constitution 原则
□ 依赖方向符合 Architecture 原则
□ 模块划分符合 Design 原则
```

#### 3. 技术约束合规

```
□ Python 版本符合约束
□ 依赖版本符合约束
□ 安全性要求满足
```

#### 4. 自定义原则合规

```
□ Principle 1 符合
□ Principle 2 符合
□ ... （按 Constitution 定义）
```

---

### 检查方法

```bash
# 读取 Constitution
cat ./pjflow/constitution.md

# 逐一验证每条原则
# 对于不合规的代码：
#   1. 标记问题
#   2. 要求修复
#   3. 修复后重新审核
#   4. 仍不合规则拒绝合并
```

---

### 审核标准（强制执行）

```
✅ 所有 Constitution 规则必须遵守
❌ 违反 Constitution 的代码必须修复
❌ 修复后仍不合规，拒绝合并
```

---

## 🚨 常见违规类型

### 1. 编码标准违规

- **类型注解缺失**: 函数参数和返回值缺少类型注解
- **命名不符合约定**: 变量/函数命名不遵循 Constitution 定义的约定
- **代码风格不一致**: 缩进、空行、引号使用不一致

### 2. 架构原则违规

- **分层结构混乱**: 跨层直接调用，绕过中间层
- **依赖方向错误**: 上层依赖下层，或循环依赖
- **模块划分不清**: 职责不明确，耦合度高

### 3. 技术约束违规

- **Python 版本不匹配**: 使用了不兼容的 Python 特性
- **依赖版本冲突**: 使用了未在 pyproject.toml 中定义的依赖
- **安全性问题**: SQL 注入、XSS 等安全漏洞

### 4. 自定义原则违规

- **违反项目特定原则**: 如"必须使用 UUID v4"、"必须使用 async"等

---

## 🔧 修复流程

### 发现违规后的处理步骤

1. **标记问题**
   - 记录违规类型和位置
   - 引用 Constitution 具体条款

2. **要求修复**
   - 明确指出需要修改的内容
   - 提供修复建议（如果适用）

3. **修复后重新审核**
   - 验证所有问题已修复
   - 确认没有引入新的违规

4. **仍不合规则拒绝合并**
   - 记录拒绝原因
   - 提供进一步修复指导

---

**文档版本**: 1.0.0
**更新时间**: 2026-02-11
**用途**: Constitution 合规性检查指南
**适用阶段**: Phase 4 + Phase 5

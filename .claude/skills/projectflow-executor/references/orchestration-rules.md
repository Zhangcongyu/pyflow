# 编排者防错指南

## 🎯 核心概念：脚手架 vs 业务编码

**你是编排者（ORCHESTRATOR）**：
- ✅ **可以**创建脚手架（项目基础设施配置）
- ❌ **禁止**编写业务逻辑代码（必须使用 TDD 工具链）

### 脚手架 vs 业务编码判断

**Phase 2 脚手架** → 使用 `projectflow-scaffolder` skill ✅
**Phase 4 (TDD 执行)** → 业务逻辑 → 使用 `pyflow-tdd-cycle` skill ❌

**判断标准**：
- 这是脚手架吗？（所有项目都需要） → 使用 `projectflow-scaffolder`
- 这是业务逻辑吗？（包含具体功能） → 使用 `pyflow-tdd-cycle`

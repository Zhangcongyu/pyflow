# 路由决策表

## 参数组合

| 项目状态 | 复杂度 | 语言 | 参数组合 |
|---------|--------|------|------------------|
| 新项目 | 简单 | Python | `--new --simple --python` |
| 新项目 | 中等 | Python | `--new --medium --python` |
| 新项目 | 复杂 | Python | `--new --complex --python` |
| 新项目 | 简单 | TypeScript | `--new --simple --typescript` |
| 新项目 | 中等 | TypeScript | `--new --medium --typescript` |
| 新项目 | 复杂 | TypeScript | `--new --complex --typescript` |
| 新项目 | 简单 | Go | `--new --simple --go` |
| 新项目 | 中等 | Go | `--new --medium --go` |
| 新项目 | 复杂 | Go | `--new --complex --go` |
| 老项目 | 简单 | Python | `--add-feature --simple --python` |
| 老项目 | 中等 | Python | `--add-feature --medium --python` |
| 老项目 | 复杂 | Python | `--add-feature --complex --python` |
| 老项目 | 简单 | TypeScript | `--add-feature --simple --typescript` |
| 老项目 | 中等 | TypeScript | `--add-feature --medium --typescript` |
| 老项目 | 复杂 | TypeScript | `--add-feature --complex --typescript` |
| 老项目 | 简单 | Go | `--add-feature --simple --go` |
| 老项目 | 中等 | Go | `--add-feature --medium --go` |
| 老项目 | 复杂 | Go | `--add-feature --complex --go` |

## 调用示例

```
Skill(skill="projectflow-planner", args="--new --simple --python 创建 CLI 待办事项工具")
Skill(skill="projectflow-planner", args="--new --medium --typescript 创建 React Web 应用")
Skill(skill="projectflow-planner", args="--new --simple --go 创建 CLI 工具")
Skill(skill="projectflow-planner", args="--add-feature --medium --python 添加用户认证功能")
Skill(skill="projectflow-planner", args="--add-feature --complex --go 添加分布式支持")
```

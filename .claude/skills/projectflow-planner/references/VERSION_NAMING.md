# 版本目录命名规则

## pjflow 目录架构

```
项目根目录/pjflow/
├── constitution.md    # 共享宪法文档（项目级）
├── requirements.md      # 共享需求文档（可选）
│
├── v0_initial/        # 初始项目创建
│   ├── task_plan.md
│   ├── progress.md
│   └── findings.md
│
├── v1_add_feature/    # 第1次新增功能
│   ├── task_plan.md
│   ├── progress.md
│   └── findings.md
│
└── v{N}_feature/      # 第N次新增功能
    ├── task_plan.md
    ├── progress.md
    └── findings.md
```

## 命名规则

| 项目状态 | 版本目录名称 | 说明 |
|---------|-------------|------|
| **new** | `v0_initial` | 固定名称 |
| **add-feature** | `v{N}_{feature_name}` | N 为递增版本号 |

## 版本号递增逻辑

```bash
existing_versions=$(find ./pjflow -maxdepth 1 -type d -name "v*" 2>/dev/null | sort -V)
if [ -z "$existing_versions" ]; then
    next_version=1
else
    max_version=$(echo "$existing_versions" | tail -1 | sed 's/v//')
    next_version=$((max_version + 1))
fi
echo "下一个版本号: v${next_version}"
```

## feature_name 提取规则

- 从用户需求中提取关键词（最多 3 个单词）
- 转为小写，用下划线连接
- 示例: `add_user_authentication`, `implement_payment_gateway`

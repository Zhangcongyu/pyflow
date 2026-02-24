# 目录结构与版本管理

## 目录结构

```
pjflow/
├── constitution.md              # 共享宪法（所有版本共享）
│
├── v0_initial/                  # 新建项目
│   ├── task_plan.md
│   ├── requirements.md
│   ├── CHECKLIST.md
│   ├── progress.md
│   ├── findings.md
│   └── compliance_report.md
│
├── v1_add_feature/              # 第1次新增功能
│   ├── task_plan.md
│   ├── requirements.md
│   ├── CHECKLIST.md
│   ├── progress.md
│   ├── findings.md
│   └── compliance_report.md
│
└── vN_add_feature/              # 第N次新增功能
    └── ...
```

## 版本命名规则

| 项目类型 | 版本目录 | 说明 |
|---------|---------|------|
| 新项目 | `v0_initial` | 初始版本 |
| 添加功能 | `v{N}_{feature_name}` | N 自动递增，feature_name 简短描述 |

示例: `v1_user_auth`, `v2_api_cache`, `v3_export_feature`

## 文档关系

| 文档 | 作用 | 作用域 |
|------|------|--------|
| constitution.md | 项目规则 | 所有版本共享 |
| requirements.md | 需求清单 | 每个版本独立 |
| task_plan.md | 执行计划 | 每个版本独立 |
| CHECKLIST.md | 进度追踪 | 每个版本独立 |
| progress.md | 执行日志 | 每个版本独立 |
| findings.md | 知识积累 | 每个版本独立 |

## 检测最新版本

```bash
# 找到最新版本目录
latest_version_dir=$(find ./pjflow -type d -name "v*" | sort -V | tail -1)
```

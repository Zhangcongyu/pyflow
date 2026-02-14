# 环境检测字段说明

## Git 字段

| 字段 | 类型 | 说明 |
|--------|------|------|
| `git.exists` | boolean | Git 仓库是否存在 |
| `git.branch` | string\|null | 当前分支名 |
| `git.has_remote` | boolean | 是否有远程仓库 |

## 虚拟环境字段

| 字段 | 类型 | 说明 |
|--------|------|------|
| `virtual_env.has_env` | boolean | 是否有虚拟环境 |
| `virtual_env.env_type` | string\|null | 环境类型（python-venv, python-uv, python-poetry, nodejs, go-modules, rust-cargo, java-gradle） |
| `virtual_env.language` | string\|null | 检测到的语言（python, typescript, go, rust, java） |

## 项目架构字段

| 字段 | 类型 | 说明 |
|--------|------|------|
| `project_structure.has_src_dir` | boolean | 是否有 src/ 目录 |
| `project_structure.has_tests_dir` | boolean | 是否有 tests/ 或 test/ 目录 |
| `project_structure.language` | string\|null | 检测到的语言（python, typescript, go, rust, java） |
| `project_structure.project_type` | string\|null | 项目类型（cli, library, fastapi, django, flask, express, nextjs, react, vue, nestjs 等） |
| `project_structure.framework` | string\|null | 检测到的框架（fastapi, django, flask, express, react, nextjs 等） |

## 项目年龄字段

| 字段 | 类型 | 说明 |
|--------|------|------|
| `project_age.is_new_project` | boolean | 是否为新项目 |
| `project_age.is_old_project` | boolean | 是否为老项目 |
| `project_age.confidence` | string | 判断置信度（high, medium, low） |
| `project_age.reasoning` | string[] | 判断依据列表 |

## 支持的语言

`detect_environment.py` 支持以下语言的完整检测：

- **Python**: venv, uv.lock, poetry.lock, pyproject.toml, setup.py, requirements.txt
- **TypeScript/JavaScript**: node_modules, package.json, tsconfig.json, package-lock.json, yarn.lock, pnpm-lock.yaml
- **Go**: go.mod, go.sum
- **Rust**: Cargo.toml, Cargo.lock
- **Java**: pom.xml, build.gradle, gradle.lock

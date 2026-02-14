# Python 项目架构类型参考

本文档定义了常见 Python 项目类型的目录结构和必要文件。

---

## 🏗️ 架构原则

### 文件分类

**系统文件**（必须完整填写）：
- ✅ `pyproject.toml` - 项目配置和依赖
- ✅ `.gitignore` - Git 忽略规则
- ✅ `Makefile` - 常用命令快捷方式
- ✅ `README.md` - 项目说明
- ✅ `.env.example` - 环境变量示例
- ✅ `pytest.ini` / `pyproject.toml` 测试配置 - 测试配置
- ✅ `ruff.toml` / `.ruff.toml` - 代码检查配置

**编码文件**（只创建空文件）：
- ⚪ `main.py` - 应用入口（空文件）
- ⚪ `config.py` - 配置类（空文件）
- ⚪ `models/` - 数据模型（空 __init__.py）
- ⚪ `api/` - API 路由（空 __init__.py）
- ⚪ `services/` - 业务服务（空 __init__.py）
- ⚪ `core/` - 核心模块（空 __init__.py）

---

## 1. FastAPI 项目（推荐）

### 适用场景
- RESTful API 服务
- 微服务架构
- Web 后端服务

### 目录结构
```
project-name/
├── pyproject.toml              # 系统文件（完整）
├── .gitignore                  # 系统文件（完整）
├── .env.example                # 系统文件（完整）
├── Makefile                    # 系统文件（完整）
├── README.md                   # 系统文件（完整）
├── src/
│   └── project_name/
│       ├── __init__.py         # 编码文件（空）
│       ├── main.py             # 编码文件（空）
│       ├── config.py           # 编码文件（空）
│       ├── api/
│       │   ├── __init__.py     # 编码文件（空）
│       │   └── v1/
│       │       ├── __init__.py # 编码文件（空）
│       │       └── router.py   # 编码文件（空）
│       ├── core/
│       │   ├── __init__.py     # 编码文件（空）
│       │   ├── database.py     # 编码文件（空）
│       │   └── security.py     # 编码文件（空）
│       ├── models/
│       │   ├── __init__.py     # 编码文件（空）
│       │   └── user.py         # 编码文件（空）
│       ├── schemas/
│       │   ├── __init__.py     # 编码文件（空）
│       │   └── user.py         # 编码文件（空）
│       └── services/
│           ├── __init__.py     # 编码文件（空）
│           └── user_service.py # 编码文件（空）
└── tests/
    ├── __init__.py             # 编码文件（空）
    ├── conftest.py             # 编码文件（空）
    └── api/
        └── __init__.py         # 编码文件（空）
```

### pyproject.toml（系统文件 - 完整填写）
```toml
[project]
name = "project-name"
version = "0.1.0"
description = "Project description"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "fastapi>=0.110.0",
    "uvicorn[standard]>=0.27.0",
    "pydantic>=2.6.0",
    "pydantic-settings>=2.1.0",
    "sqlalchemy>=2.0.0",
    "aiosqlite>=0.19.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.23.0",
    "pytest-cov>=4.1.0",
    "httpx>=0.26.0",
    "ruff>=0.2.0",
    "mypy>=1.8.0",
]

[tool.ruff]
line-length = 100
target-version = "py312"

[tool.mypy]
python_version = "3.12"
strict = true

[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

# 中国国内镜像源
[[tool.uv.index]]
name = "tsinghua"
url = "https://pypi.tuna.tsinghua.edu.cn/simple"
default = true

[tool.uv.pip]
index-url = "https://repo.huaweicloud.com/repository/pypi/simple"
```

---

## 2. Django 项目

### 适用场景
- 全栈 Web 应用
- 内容管理系统
- 企业级应用

### 目录结构
```
project-name/
├── pyproject.toml              # 系统文件（完整）
├── .gitignore                  # 系统文件（完整）
├── .env.example                # 系统文件（完整）
├── Makefile                    # 系统文件（完整）
├── README.md                   # 系统文件（完整）
├── manage.py                   # Django 生成（完整）
├── src/
│   ├── project_name/
│   │   ├── __init__.py         # Django 生成
│   │   ├── settings.py         # 编码文件（空）
│   │   ├── urls.py             # 编码文件（空）
│   │   └── wsgi.py             # Django 生成
│   └── apps/
│       └── __init__.py         # 编码文件（空）
└── tests/
    ├── __init__.py             # 编码文件（空）
    └── conftest.py             # 编码文件（空）
```

### pyproject.toml（系统文件 - 完整填写）
```toml
[project]
name = "project-name"
version = "0.1.0"
description = "Django project"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "django>=5.0.0",
    "djangorestframework>=3.14.0",
    "psycopg2-binary>=2.9.0",
    "celery>=5.3.0",
    "redis>=5.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-django>=4.7.0",
    "pytest-cov>=4.1.0",
    "ruff>=0.2.0",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
django_settings = "project_name.settings"
python_files = ["test_*.py"]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

# 中国国内镜像源
[[tool.uv.index]]
name = "tsinghua"
url = "https://pypi.tuna.tsinghua.edu.cn/simple"
default = true
```

---

## 3. CLI 工具项目

### 适用场景
- 命令行工具
- 脚本工具集
- DevOps 工具

### 目录结构
```
project-name/
├── pyproject.toml              # 系统文件（完整）
├── .gitignore                  # 系统文件（完整）
├── Makefile                    # 系统文件（完整）
├── README.md                   # 系统文件（完整）
├── src/
│   └── project_name/
│       ├── __init__.py         # 编码文件（空）
│       ├── __main__.py         # 编码文件（空）
│       ├── cli.py              # 编码文件（空）
│       └── commands/
│           ├── __init__.py     # 编码文件（空）
│           └── command1.py     # 编码文件（空）
└── tests/
    ├── __init__.py             # 编码文件（空）
    └── test_commands.py        # 编码文件（空）
```

### pyproject.toml（系统文件 - 完整填写）
```toml
[project]
name = "project-name"
version = "0.1.0"
description = "CLI tool"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "click>=8.1.0",
    "rich>=13.7.0",
    "typer>=0.9.0",
]

[project.scripts]
cli-name = "project_name.cli:main"

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-cov>=4.1.0",
    "ruff>=0.2.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/project_name"]

# 中国国内镜像源
[[tool.uv.index]]
name = "tsinghua"
url = "https://pypi.tuna.tsinghua.edu.cn/simple"
default = true
```

---

## 4. Python 包（Library）

### 适用场景
- 发布到 PyPI 的库
- 供其他项目使用的模块
- SDK/工具包

### 目录结构
```
project-name/
├── pyproject.toml              # 系统文件（完整）
├── .gitignore                  # 系统文件（完整）
├── Makefile                    # 系统文件（完整）
├── README.md                   # 系统文件（完整）
├── LICENSE                     # 系统文件（完整）
├── src/
│   └── project_name/
│       ├── __init__.py         # 编码文件（空，只写版本号）
│       ├── core.py             # 编码文件（空）
│       └── utils.py            # 编码文件（空）
└── tests/
    ├── __init__.py             # 编码文件（空）
    └── test_core.py            # 编码文件（空）
```

### pyproject.toml（系统文件 - 完整填写）
```toml
[project]
name = "project-name"
version = "0.1.0"
description = "Python library"
readme = "README.md"
requires-python = ">=3.12"
license = { text = "MIT" }
dependencies = [
    "requests>=2.31.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-cov>=4.1.0",
    "ruff>=0.2.0",
    "mypy>=1.8.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/project_name"]

# 中国国内镜像源
[[tool.uv.index]]
name = "tsinghua"
url = "https://pypi.tuna.tsinghua.edu.cn/simple"
default = true
```

---

## 5. 数据处理项目

### 适用场景
- 数据分析脚本
- ETL 流程
- 机器学习项目

### 目录结构
```
project-name/
├── pyproject.toml              # 系统文件（完整）
├── .gitignore                  # 系统文件（完整）
├── .env.example                # 系统文件（完整）
├── Makefile                    # 系统文件（完整）
├── README.md                   # 系统文件（完整）
├── data/
│   ├── raw/                    # 原始数据
│   ├── processed/              # 处理后数据
│   └── .gitkeep                # 空文件占位
├── notebooks/
│   └── .gitkeep                # 空文件占位
├── src/
│   └── project_name/
│       ├── __init__.py         # 编码文件（空）
│       ├── pipeline.py         # 编码文件（空）
│       ├── transform.py        # 编码文件（空）
│       └── load.py             # 编码文件（空）
└── tests/
    ├── __init__.py             # 编码文件（空）
    └── test_pipeline.py        # 编码文件（空）
```

### pyproject.toml（系统文件 - 完整填写）
```toml
[project]
name = "project-name"
version = "0.1.0"
description = "Data processing project"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "pandas>=2.1.0",
    "numpy>=1.26.0",
    "sqlalchemy>=2.0.0",
    "psycopg2-binary>=2.9.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-cov>=4.1.0",
    "jupyter>=1.0.0",
    "ruff>=0.2.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

# 中国国内镜像源
[[tool.uv.index]]
name = "tsinghua"
url = "https://pypi.tuna.tsinghua.edu.cn/simple"
default = true
```

---

## 6. 机器学习项目

### 适用场景
- 深度学习模型
- 数据科学项目
- AI/ML 实验项目

### 目录结构
```
project-name/
├── pyproject.toml              # 系统文件（完整）
├── .gitignore                  # 系统文件（完整）
├── .env.example                # 系统文件（完整）
├── Makefile                    # 系统文件（完整）
├── README.md                   # 系统文件（完整）
├── data/
│   ├── raw/                    # 原始数据
│   ├── processed/              # 处理后数据
│   └── .gitkeep                # 空文件占位
├── notebooks/
│   └── .gitkeep                # 空文件占位
├── models/
│   └── .gitkeep                # 空文件占位
├── src/
│   └── project_name/
│       ├── __init__.py         # 编码文件（空）
│       ├── model.py            # 编码文件（空）
│       ├── train.py            # 编码文件（空）
│       ├── evaluate.py         # 编码文件（空）
│       └── data/
│           ├── __init__.py     # 编码文件（空）
│           └── dataset.py      # 编码文件（空）
└── tests/
    ├── __init__.py             # 编码文件（空）
    └── test_model.py           # 编码文件（空）
```

### pyproject.toml（系统文件 - 完整填写）
```toml
[project]
name = "project-name"
version = "0.1.0"
description = "ML project"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "torch>=2.1.0",
    "torchvision>=0.16.0",
    "pandas>=2.1.0",
    "numpy>=1.26.0",
    "scikit-learn>=1.3.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "jupyter>=1.0.0",
    "ruff>=0.2.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

# 中国国内镜像源
[[tool.uv.index]]
name = "tsinghua"
url = "https://pypi.tuna.tsinghua.edu.cn/simple"
default = true
```

---

## 📋 通用系统文件模板

### .gitignore（完整）
```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environment
.venv/
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Testing
.pytest_cache/
.coverage
htmlcov/
*.cover
.hypothesis/

# Type Checking
.mypy_cache/
.dmypy.json
dmypy.json
.ruff_cache/

# Database
*.db
*.db-journal
*.sqlite
*.sqlite3

# Environment
.env
.env.local
*.log

# OS
.DS_Store
Thumbs.db

# Project specific
data/raw/*
!data/raw/.gitkeep
models/*
!models/.gitkeep
```

### Makefile（完整）
```makefile
.PHONY: install dev test lint format clean check

install:
	uv sync

dev:
	uv run uvicorn src.project_name.main:app --reload

test:
	uv run pytest -v

test-cov:
	uv run pytest -v --cov=src/project_name --cov-report=html

lint:
	uv run ruff check .

format:
	uv run ruff format .

check:
	uv run ruff check .
	uv run mypy src/project_name
	uv run pytest

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .ruff_cache .coverage htmlcov
```

### .env.example（完整）
```bash
# Application
PROJECT_NAME=project-name
VERSION=0.1.0
DEBUG=true

# Database
DATABASE_URL=sqlite+aiosqlite:///./app.db

# API
API_V1_PREFIX=/api/v1
ALLOWED_ORIGINS=["http://localhost:3000"]

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### README.md（完整模板）
```markdown
# Project Name

Description of the project.

## Installation

```bash
uv sync
```

## Usage

```bash
uv run uvicorn src.project_name.main:app --reload
```

## Development

```bash
make install  # Install dependencies
make test     # Run tests
make lint     # Check code quality
make format   # Format code
```

## License

MIT
```

---

**文档版本**: 1.0.0
**更新时间**: 2026-02-09
**用途**: Python 项目架构类型参考

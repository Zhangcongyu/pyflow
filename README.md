# File Counter

文件计数器工具 - 统计目录下的文件数量，按扩展名分类

## 功能

- 递归扫描指定目录
- 按文件扩展名分类统计
- 友好的命令行接口
- 支持控制递归和隐藏文件

## 安装

```bash
# 使用 uv (推荐)
uv venv
source .venv/bin/activate
uv pip install -e .

# 或使用 venv
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## 使用

```bash
# 基本用法
file-counter /path/to/directory

# 非递归
file-counter /path/to/directory --no-recursive

# 包含隐藏文件
file-counter /path/to/directory --hidden
```

## 开发

```bash
# 运行测试
pytest

# 格式化代码
ruff format .

# 检查代码
ruff check .

# 运行覆盖率测试
pytest --cov=src --cov-report=term-missing

# 类型检查
mypy src/
```

## 项目结构

```
file-counter/
├── src/
│   └── file_counter/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py
│       └── counter.py
└── tests/
    └── test_counter.py
```

## License

MIT

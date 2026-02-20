# Requirements

**Project Type**: new
**Complexity**: simple
**Goal**: 帮我创建一个文件计数器工具，统计目录下的文件数量

---

## Project Overview

创建一个文件计数器工具，统计指定目录下的文件数量。该工具将递归扫描目录，按文件扩展名分类统计，并以友好的格式输出结果。

## Core Features

### Feature 1: 文件计数与分类
- Description: 统计指定目录下的文件数量，按文件扩展名分类统计
- Acceptance Criteria:
  - 接受目录路径作为命令行参数
  - 递归扫描所有子目录
  - 按扩展名分类统计文件数量
  - 输出总计和各类型数量
  - 处理无扩展名的文件
  - 处理隐藏文件（可选）
- Priority: 高

### Feature 2: 命令行接口
- Description: 提供友好的 CLI 接口
- Acceptance Criteria:
  - 支持 `--help` 显示帮助信息
  - 支持 `--directory` 或位置参数指定目录
  - 支持 `--recursive` 控制是否递归（默认递归）
  - 支持 `--hidden` 控制是否包含隐藏文件（默认不包含）
- Priority: 中

## Technical Requirements

- Performance requirements: 支持包含数千文件的目录，响应时间 < 5 秒
- Security requirements: 只读操作，不修改任何文件
- Compatibility requirements: Python 3.10+

## Success Criteria

1. 能正确统计指定目录下的文件数量
2. 按扩展名正确分类（包括无扩展名文件）
3. 支持递归扫描子目录
4. 命令行接口友好，参数清晰
5. 输出格式易读

## Usage Example

```bash
# 基本用法
file-counter /path/to/directory

# 非递归
file-counter /path/to/directory --no-recursive

# 包含隐藏文件
file-counter /path/to/directory --hidden
```

## Expected Output Format

```
File Counter Results
====================
Directory: /path/to/directory
Total files: 150

By extension:
  .py:    45 files
  .md:    12 files
  .txt:    8 files
  .json:   5 files
  (none): 15 files
  other:  65 files
```

---
*Created: new - simple*
*Date: 2026-02-20*

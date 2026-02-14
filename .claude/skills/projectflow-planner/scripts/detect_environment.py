#!/usr/bin/env python3
"""
环境检测脚本 - 检测项目当前状态
支持多语言：Python, TypeScript/JavaScript, Go, Rust, Java, etc.

检测内容包括：
1. Git仓库状态（是否存在、当前分支）
2. 虚拟环境/包管理器（Python: venv/uv, Node.js: node_modules, Go: go.mod等）
3. 现有项目架构（src/、tests/、配置文件等）
4. 项目语言和类型检测
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional


def detect_git_repo(cwd: Path) -> Dict[str, any]:
    """检测Git仓库状态"""
    git_dir = cwd / ".git"

    result = {
        "exists": git_dir.exists(),
        "initialized": False,
        "branch": None,
        "has_remote": False,
        "remotes": []
    }

    if not result["exists"]:
        return result

    result["initialized"] = True

    # 检测当前分支
    head_file = git_dir / "HEAD"
    if head_file.exists():
        content = head_file.read_text().strip()
        if content.startswith("ref: refs/heads/"):
            result["branch"] = content.replace("ref: refs/heads/", "")

    # 检测远程仓库
    config_file = git_dir / "config"
    if config_file.exists():
        content = config_file.read_text()
        if '[remote "' in content:
            result["has_remote"] = True
            # 提取remote名称
            import re
            remotes = re.findall(r'\[remote "([^"]+)"\]', content)
            result["remotes"] = remotes

    return result


def detect_virtual_env(cwd: Path) -> Dict[str, any]:
    """检测虚拟环境/包管理器（支持多语言）"""
    result = {
        "has_env": False,
        "env_type": None,
        "env_location": None,
        "language": None,
        "details": {}
    }

    # Python 虚拟环境检测
    venv_dirs = [".venv", "venv", ".virtualenv", "env"]
    for venv_dir in venv_dirs:
        venv_path = cwd / venv_dir
        if venv_path.exists() and venv_path.is_dir():
            result["has_env"] = True
            result["env_type"] = "python-venv"
            result["env_location"] = venv_dir
            result["language"] = "python"
            result["details"]["venv_dir"] = venv_dir
            break

    # UV 锁文件检测
    uv_lock = cwd / "uv.lock"
    if uv_lock.exists():
        result["has_env"] = True
        if not result["env_type"]:
            result["env_type"] = "python-uv"
            result["language"] = "python"
        result["details"]["has_uv_lock"] = True

    # Poetry 检测
    poetry_lock = cwd / "poetry.lock"
    if poetry_lock.exists():
        result["has_env"] = True
        if not result["env_type"]:
            result["env_type"] = "python-poetry"
            result["language"] = "python"
        result["details"]["has_poetry_lock"] = True

    # Node.js/npm/yarn/pnpm 检测
    node_modules = cwd / "node_modules"
    package_lock = cwd / "package-lock.json"
    yarn_lock = cwd / "yarn.lock"
    pnpm_lock = cwd / "pnpm-lock.yaml"

    if node_modules.exists() or package_lock.exists() or yarn_lock.exists() or pnpm_lock.exists():
        result["has_env"] = True
        result["env_type"] = "nodejs"
        result["env_location"] = "node_modules"
        result["language"] = "typescript"

        if yarn_lock.exists():
            result["details"]["package_manager"] = "yarn"
        elif pnpm_lock.exists():
            result["details"]["package_manager"] = "pnpm"
        elif package_lock.exists():
            result["details"]["package_manager"] = "npm"
        else:
            result["details"]["package_manager"] = "unknown"

    # Go modules 检测
    go_sum = cwd / "go.sum"
    if go_sum.exists():
        result["has_env"] = True
        result["env_type"] = "go-modules"
        result["language"] = "go"
        result["details"]["has_go_sum"] = True

    # Rust Cargo 检测
    cargo_lock = cwd / "Cargo.lock"
    if cargo_lock.exists():
        result["has_env"] = True
        result["env_type"] = "rust-cargo"
        result["language"] = "rust"
        result["details"]["has_cargo_lock"] = True

    # Java Maven/Gradle 检测
    target_dir = cwd / "target"
    build_gradle = cwd / "build.gradle"
    gradle_lock = cwd / "gradle.lock"

    if target_dir.exists() or build_gradle.exists() or gradle_lock.exists():
        result["has_env"] = True
        result["env_type"] = "java-gradle"
        result["language"] = "java"
        if build_gradle.exists():
            result["details"]["build_tool"] = "gradle"
        else:
            result["details"]["build_tool"] = "maven"

    return result


def detect_project_structure(cwd: Path) -> Dict[str, any]:
    """检测项目架构（支持多语言）"""
    result = {
        # 通用文件
        "has_readme": False,
        "has_gitignore": False,
        "has_src_dir": False,
        "has_tests_dir": False,
        "has_lib_dir": False,
        # Python 配置文件
        "has_pyproject_toml": False,
        "has_setup_py": False,
        "has_requirements_txt": False,
        # TypeScript/Node.js 配置文件
        "has_package_json": False,
        "has_tsconfig_json": False,
        "has_npmrc": False,
        # Go 配置文件
        "has_go_mod": False,
        "has_go_sum": False,
        # Rust 配置文件
        "has_cargo_toml": False,
        # Java 配置文件
        "has_pom_xml": False,
        "has_build_gradle": False,
        # 项目类型和语言
        "project_type": None,
        "language": None,
        "framework": None
    }

    # 检测通用文件
    result["has_readme"] = any(
        (cwd / f"README{ext}").exists()
        for ext in ["", ".md", ".rst", ".txt"]
    )
    result["has_gitignore"] = (cwd / ".gitignore").exists()

    # 检测目录结构
    src_dir = cwd / "src"
    tests_dir = cwd / "tests"
    test_dir = cwd / "test"
    lib_dir = cwd / "lib"

    result["has_src_dir"] = src_dir.exists() and src_dir.is_dir()
    result["has_tests_dir"] = (tests_dir.exists() and tests_dir.is_dir()) or (
        test_dir.exists() and test_dir.is_dir()
    )
    result["has_lib_dir"] = lib_dir.exists() and lib_dir.is_dir()

    # 检测 Python 配置文件
    result["has_pyproject_toml"] = (cwd / "pyproject.toml").exists()
    result["has_setup_py"] = (cwd / "setup.py").exists()
    result["has_requirements_txt"] = (cwd / "requirements.txt").exists()

    # 检测 TypeScript/Node.js 配置文件
    result["has_package_json"] = (cwd / "package.json").exists()
    result["has_tsconfig_json"] = (cwd / "tsconfig.json").exists()
    result["has_npmrc"] = (cwd / ".npmrc").exists()

    # 检测 Go 配置文件
    result["has_go_mod"] = (cwd / "go.mod").exists()
    result["has_go_sum"] = (cwd / "go.sum").exists()

    # 检测 Rust 配置文件
    result["has_cargo_toml"] = (cwd / "Cargo.toml").exists()

    # 检测 Java 配置文件
    result["has_pom_xml"] = (cwd / "pom.xml").exists()
    result["has_build_gradle"] = (cwd / "build.gradle").exists() or (cwd / "build.gradle.kts").exists()

    # 检测项目语言
    if result["has_pyproject_toml"] or result["has_setup_py"]:
        result["language"] = "python"
    elif result["has_package_json"]:
        result["language"] = "typescript"
    elif result["has_go_mod"]:
        result["language"] = "go"
    elif result["has_cargo_toml"]:
        result["language"] = "rust"
    elif result["has_pom_xml"] or result["has_build_gradle"]:
        result["language"] = "java"

    # 检测 Python 项目类型和框架
    if result["language"] == "python" and result["has_pyproject_toml"]:
        try:
            import toml
            pyproject = toml.loads((cwd / "pyproject.toml").read_text())

            # 检查 dependencies
            deps = pyproject.get("project", {}).get("dependencies", [])
            deps_str = " ".join(deps).lower()

            if "fastapi" in deps_str or "starlette" in deps_str:
                result["project_type"] = "fastapi"
                result["framework"] = "fastapi"
            elif "django" in deps_str:
                result["project_type"] = "django"
                result["framework"] = "django"
            elif "flask" in deps_str:
                result["project_type"] = "flask"
                result["framework"] = "flask"
            elif "click" in deps_str or "typer" in deps_str:
                result["project_type"] = "cli"
            elif "pandas" in deps_str or "numpy" in deps_str:
                result["project_type"] = "data"
            elif "torch" in deps_str or "tensorflow" in deps_str:
                result["project_type"] = "ml"
            else:
                result["project_type"] = "library"
        except Exception:
            result["project_type"] = None

    # 检测 TypeScript/Node.js 项目类型和框架
    elif result["language"] == "typescript" and result["has_package_json"]:
        try:
            import json
            package_json = json.loads((cwd / "package.json").read_text())

            deps = package_json.get("dependencies", {})
            dev_deps = package_json.get("devDependencies", {})
            all_deps = {**deps, **dev_deps}
            deps_str = " ".join(all_deps.keys()).lower()

            if "next" in deps_str:
                result["project_type"] = "nextjs"
                result["framework"] = "nextjs"
            elif "react" in deps_str and "vite" in deps_str:
                result["project_type"] = "react-vite"
                result["framework"] = "react"
            elif "react" in deps_str:
                result["project_type"] = "react"
                result["framework"] = "react"
            elif "vue" in deps_str:
                result["project_type"] = "vue"
                result["framework"] = "vue"
            elif "nestjs" in deps_str:
                result["project_type"] = "nestjs"
                result["framework"] = "nestjs"
            elif "express" in deps_str:
                result["project_type"] = "express"
                result["framework"] = "express"
            elif "astro" in deps_str:
                result["project_type"] = "astro"
                result["framework"] = "astro"
            else:
                result["project_type"] = "nodejs-library"
        except Exception:
            result["project_type"] = None

    # 检测 Go 项目类型
    elif result["language"] == "go" and result["has_go_mod"]:
        result["project_type"] = "go-service"
        result["framework"] = "go-stdlib"

    # 检测 Rust 项目类型
    elif result["language"] == "rust" and result["has_cargo_toml"]:
        result["project_type"] = "rust-crate"
        result["framework"] = "cargo"

    # 检测 Java 项目类型
    elif result["language"] == "java":
        if result["has_build_gradle"]:
            result["project_type"] = "java-gradle"
            result["framework"] = "gradle"
        else:
            result["project_type"] = "java-maven"
            result["framework"] = "maven"

    return result


def detect_project_age(cwd: Path) -> Dict[str, any]:
    """检测项目年龄（新项目 vs 老项目）"""
    git_info = detect_git_repo(cwd)
    structure = detect_project_structure(cwd)

    result = {
        "is_new_project": False,
        "is_old_project": False,
        "confidence": "low",
        "reasoning": []
    }

    # 判断依据
    reasons = []

    # 如果没有Git仓库，很可能是新项目
    if not git_info["exists"]:
        reasons.append("No .git directory found")
        result["is_new_project"] = True
        result["confidence"] = "high"
    # 如果有Git但没有提交，也是新项目
    elif not git_info["initialized"]:
        reasons.append("Git not initialized")
        result["is_new_project"] = True
        result["confidence"] = "high"
    # 如果没有项目配置文件，可能是新项目
    elif not structure["has_pyproject_toml"] and not structure["has_setup_py"]:
        reasons.append("No project configuration found (pyproject.toml/setup.py)")
        result["is_new_project"] = True
        result["confidence"] = "medium"
    # 如果有完整的项目结构，肯定是老项目
    elif structure["has_src_dir"] and structure["has_tests_dir"]:
        reasons.append("Complete project structure found (src/ and tests/)")
        result["is_old_project"] = True
        result["confidence"] = "high"
    # 如果有配置文件和Git，大概率是老项目
    elif structure["has_pyproject_toml"] and git_info["exists"]:
        reasons.append("Project configuration and Git repository found")
        result["is_old_project"] = True
        result["confidence"] = "high"

    result["reasoning"] = reasons

    return result


def detect_all(cwd: Optional[Path] = None) -> Dict[str, any]:
    """执行所有检测"""
    if cwd is None:
        cwd = Path.cwd()

    return {
        "working_directory": str(cwd),
        "git": detect_git_repo(cwd),
        "virtual_env": detect_virtual_env(cwd),
        "project_structure": detect_project_structure(cwd),
        "project_age": detect_project_age(cwd),
        "timestamp": {
            "detected_at": None  # TODO: 添加时间戳
        }
    }


def main():
    parser = argparse.ArgumentParser(
        description="检测项目环境状态",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 检测当前目录
  python detect_environment.py

  # 检测指定目录
  python detect_environment.py --dir /path/to/project

  # 输出JSON格式
  python detect_environment.py --json

  # 检测特定方面
  python detect_environment.py --check git
  python detect_environment.py --check venv
  python detect_environment.py --check structure
  python detect_environment.py --check age
        """
    )

    parser.add_argument(
        "--dir",
        type=Path,
        default=None,
        help="要检测的项目目录（默认为当前目录）"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="以JSON格式输出结果"
    )
    parser.add_argument(
        "--check",
        choices=["git", "venv", "structure", "age", "all"],
        default="all",
        help="检测特定方面（默认：全部）"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="安静模式，只输出检测结果"
    )

    args = parser.parse_args()

    # 确定工作目录
    cwd = args.dir if args.dir else Path.cwd()

    if not cwd.exists():
        print(f"Error: Directory does not exist: {cwd}", file=sys.stderr)
        sys.exit(1)

    # 执行检测
    if args.check == "all":
        result = detect_all(cwd)
    elif args.check == "git":
        result = {"git": detect_git_repo(cwd)}
    elif args.check == "venv":
        result = {"virtual_env": detect_virtual_env(cwd)}
    elif args.check == "structure":
        result = {"project_structure": detect_project_structure(cwd)}
    elif args.check == "age":
        result = {"project_age": detect_project_age(cwd)}

    # 输出结果
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        if not args.quiet:
            print(f"# Environment Detection Results")
            print(f"# Directory: {cwd}")
            print()

        # 人性化输出
        if "git" in result:
            git = result["git"]
            print(f"Git Repository: {'Yes' if git['exists'] else 'No'}")
            if git["exists"]:
                print(f"  - Branch: {git['branch'] or 'not initialized'}")
                print(f"  - Remote: {'Yes' if git['has_remote'] else 'No'}")
                if git["remotes"]:
                    print(f"  - Remotes: {', '.join(git['remotes'])}")
            print()

        if "virtual_env" in result:
            venv = result["virtual_env"]
            print(f"Virtual Environment: {'Yes' if venv['has_env'] else 'No'}")
            if venv["has_env"]:
                print(f"  - Type: {venv['env_type'] or 'unknown'}")
                print(f"  - Location: {venv['env_location'] or 'unknown'}")
                if venv.get('details', {}).get('has_uv_lock'):
                    print(f"  - UV Lock: Yes")
            print()

        if "project_structure" in result:
            struct = result["project_structure"]
            print(f"Project Structure:")
            print(f"  - pyproject.toml: {'Yes' if struct['has_pyproject_toml'] else 'No'}")
            print(f"  - src/ directory: {'Yes' if struct['has_src_dir'] else 'No'}")
            print(f"  - tests/ directory: {'Yes' if struct['has_tests_dir'] else 'No'}")
            print(f"  - Language: {struct['language'] or 'unknown'}")
            print(f"  - Project Type: {struct['project_type'] or 'unknown'}")
            print()

        if "project_age" in result:
            age = result["project_age"]
            print(f"Project Status: {'New Project' if age['is_new_project'] else 'Old Project'}")
            print(f"  - Confidence: {age['confidence']}")
            if age["reasoning"]:
                print(f"  - Reasons:")
                for reason in age["reasoning"]:
                    print(f"    • {reason}")


if __name__ == "__main__":
    main()

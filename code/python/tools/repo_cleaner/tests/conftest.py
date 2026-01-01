"""Pytest fixtures for Repo Cleaner tests."""

import json
import os
import shutil
import tempfile
from pathlib import Path
from typing import Generator

import pytest


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for tests.
    
    Yields:
        Path to temporary directory
    """
    temp_path = Path(tempfile.mkdtemp(prefix="repo_cleaner_test_"))
    try:
        yield temp_path
    finally:
        shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def python_project(temp_dir: Path) -> Path:
    """Create a minimal Python project fixture.
    
    Args:
        temp_dir: Temporary directory
        
    Returns:
        Path to project directory
    """
    project_dir = temp_dir / "python_project"
    project_dir.mkdir()
    
    # Create pyproject.toml
    pyproject = project_dir / "pyproject.toml"
    pyproject.write_text("""[project]
name = "test-project"
version = "0.1.0"
""")
    
    # Create requirements.txt
    requirements = project_dir / "requirements.txt"
    requirements.write_text("requests>=2.28.0\npytest>=7.0.0\n")
    
    # Create source files
    src_dir = project_dir / "src"
    src_dir.mkdir()
    (src_dir / "__init__.py").write_text("")
    (src_dir / "main.py").write_text("def main():\n    pass\n")
    
    # Create __pycache__ directories
    pycache = src_dir / "__pycache__"
    pycache.mkdir()
    (pycache / "main.cpython-310.pyc").write_bytes(b"\x00" * 100)
    
    # Create .pytest_cache
    pytest_cache = project_dir / ".pytest_cache"
    pytest_cache.mkdir()
    (pytest_cache / "v" / "cache").mkdir(parents=True)
    (pytest_cache / ".gitignore").write_text("*\n")
    
    # Create .mypy_cache
    mypy_cache = project_dir / ".mypy_cache"
    mypy_cache.mkdir()
    (mypy_cache / "3.10").mkdir()
    
    # Create venv (for confirmation testing)
    venv = project_dir / "venv"
    venv.mkdir()
    (venv / "pyvenv.cfg").write_text("home = /usr/bin\n")
    (venv / "lib").mkdir()
    
    return project_dir


@pytest.fixture
def node_project(temp_dir: Path) -> Path:
    """Create a minimal Node.js project fixture.
    
    Args:
        temp_dir: Temporary directory
        
    Returns:
        Path to project directory
    """
    project_dir = temp_dir / "node_project"
    project_dir.mkdir()
    
    # Create package.json
    package_json = project_dir / "package.json"
    package_json.write_text(json.dumps({
        "name": "test-project",
        "version": "1.0.0",
        "dependencies": {
            "express": "^4.18.0"
        },
        "devDependencies": {
            "jest": "^29.0.0"
        }
    }, indent=2))
    
    # Create package-lock.json
    (project_dir / "package-lock.json").write_text(json.dumps({
        "name": "test-project",
        "lockfileVersion": 2
    }))
    
    # Create node_modules
    node_modules = project_dir / "node_modules"
    node_modules.mkdir()
    express_dir = node_modules / "express"
    express_dir.mkdir()
    (express_dir / "package.json").write_text(json.dumps({"name": "express"}))
    (express_dir / "index.js").write_text("module.exports = {};")
    
    # Create dist directory
    dist = project_dir / "dist"
    dist.mkdir()
    (dist / "bundle.js").write_bytes(b"0" * 1000)
    
    # Create .cache
    cache = project_dir / ".cache"
    cache.mkdir()
    (cache / "data.json").write_text("{}")
    
    # Create source files
    src = project_dir / "src"
    src.mkdir()
    (src / "index.js").write_text("console.log('hello');")
    
    return project_dir


@pytest.fixture
def java_project(temp_dir: Path) -> Path:
    """Create a minimal Java project fixture (Maven).
    
    Args:
        temp_dir: Temporary directory
        
    Returns:
        Path to project directory
    """
    project_dir = temp_dir / "java_project"
    project_dir.mkdir()
    
    # Create pom.xml
    pom = project_dir / "pom.xml"
    pom.write_text("""<?xml version="1.0" encoding="UTF-8"?>
<project>
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>test-project</artifactId>
    <version>1.0.0</version>
</project>
""")
    
    # Create source structure
    src_main = project_dir / "src" / "main" / "java" / "com" / "example"
    src_main.mkdir(parents=True)
    (src_main / "Main.java").write_text("""package com.example;
public class Main {
    public static void main(String[] args) {}
}
""")
    
    # Create target directory
    target = project_dir / "target"
    target.mkdir()
    classes = target / "classes" / "com" / "example"
    classes.mkdir(parents=True)
    (classes / "Main.class").write_bytes(b"\xca\xfe\xba\xbe" + b"\x00" * 100)
    (target / "test-project-1.0.0.jar").write_bytes(b"PK" + b"\x00" * 200)
    
    # Create .gradle directory
    gradle = project_dir / ".gradle"
    gradle.mkdir()
    (gradle / "config.properties").write_text("version=8.0\n")
    
    return project_dir


@pytest.fixture
def cpp_project(temp_dir: Path) -> Path:
    """Create a minimal C++ project fixture (CMake).
    
    Args:
        temp_dir: Temporary directory
        
    Returns:
        Path to project directory
    """
    project_dir = temp_dir / "cpp_project"
    project_dir.mkdir()
    
    # Create CMakeLists.txt
    cmake = project_dir / "CMakeLists.txt"
    cmake.write_text("""cmake_minimum_required(VERSION 3.16)
project(TestProject)
add_executable(main main.cpp)
""")
    
    # Create source files
    (project_dir / "main.cpp").write_text("""#include <iostream>
int main() { return 0; }
""")
    (project_dir / "utils.h").write_text("#pragma once\n")
    (project_dir / "utils.cpp").write_text("#include \"utils.h\"\n")
    
    # Create build directory
    build = project_dir / "build"
    build.mkdir()
    (build / "CMakeCache.txt").write_text("CMAKE_VERSION=3.20\n")
    cmake_files = build / "CMakeFiles"
    cmake_files.mkdir()
    (cmake_files / "cmake.check_cache").write_text("# CMake check cache\n")
    
    # Create object files
    (build / "main.o").write_bytes(b"\x7fELF" + b"\x00" * 100)
    (build / "utils.o").write_bytes(b"\x7fELF" + b"\x00" * 50)
    
    # Create static library
    (build / "libutils.a").write_bytes(b"!<arch>\n" + b"\x00" * 100)
    
    return project_dir


@pytest.fixture
def react_project(temp_dir: Path) -> Path:
    """Create a minimal React project fixture (Next.js).
    
    Args:
        temp_dir: Temporary directory
        
    Returns:
        Path to project directory
    """
    project_dir = temp_dir / "react_project"
    project_dir.mkdir()
    
    # Create package.json with React
    package_json = project_dir / "package.json"
    package_json.write_text(json.dumps({
        "name": "react-project",
        "version": "1.0.0",
        "dependencies": {
            "react": "^18.0.0",
            "react-dom": "^18.0.0",
            "next": "^13.0.0"
        }
    }, indent=2))
    
    # Create next.config.js
    (project_dir / "next.config.js").write_text("module.exports = {};\n")
    
    # Create .next directory
    next_dir = project_dir / ".next"
    next_dir.mkdir()
    (next_dir / "BUILD_ID").write_text("test-build-id")
    static = next_dir / "static"
    static.mkdir()
    (static / "chunks").mkdir()
    
    # Create source files
    src = project_dir / "src"
    src.mkdir()
    (src / "index.tsx").write_text("export default function Home() { return <div>Hello</div>; }")
    
    return project_dir


@pytest.fixture
def mixed_project(temp_dir: Path) -> Path:
    """Create a project with multiple languages.
    
    Args:
        temp_dir: Temporary directory
        
    Returns:
        Path to project directory
    """
    project_dir = temp_dir / "mixed_project"
    project_dir.mkdir()
    
    # Python backend
    backend = project_dir / "backend"
    backend.mkdir()
    (backend / "requirements.txt").write_text("flask>=2.0\n")
    (backend / "app.py").write_text("from flask import Flask\napp = Flask(__name__)\n")
    pycache = backend / "__pycache__"
    pycache.mkdir()
    (pycache / "app.cpython-310.pyc").write_bytes(b"\x00" * 50)
    
    # Node frontend
    frontend = project_dir / "frontend"
    frontend.mkdir()
    (frontend / "package.json").write_text(json.dumps({
        "name": "frontend",
        "dependencies": {"react": "^18.0.0"}
    }))
    node_modules = frontend / "node_modules"
    node_modules.mkdir()
    (node_modules / ".package-lock.json").write_text("{}")
    
    return project_dir


@pytest.fixture
def empty_dir(temp_dir: Path) -> Path:
    """Create an empty directory fixture.
    
    Args:
        temp_dir: Temporary directory
        
    Returns:
        Path to empty directory
    """
    empty = temp_dir / "empty_project"
    empty.mkdir()
    return empty


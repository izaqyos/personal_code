"""Default patterns for each language/framework."""

from typing import Dict, List, Any

# Default patterns organized by language/framework
DEFAULT_PATTERNS: Dict[str, List[Dict[str, Any]]] = {
    "python": [
        {
            "name": "Python Cache",
            "patterns": ["**/__pycache__", "**/__pycache__/**"],
            "type": "directory",
            "description": "Python bytecode cache directories",
            "safe": True,
        },
        {
            "name": "Compiled Python",
            "patterns": ["**/*.pyc", "**/*.pyo", "**/*.pyd"],
            "type": "file",
            "description": "Compiled Python files",
            "safe": True,
        },
        {
            "name": "Pytest Cache",
            "patterns": ["**/.pytest_cache", "**/.pytest_cache/**"],
            "type": "directory",
            "description": "Pytest cache directories",
            "safe": True,
        },
        {
            "name": "MyPy Cache",
            "patterns": ["**/.mypy_cache", "**/.mypy_cache/**"],
            "type": "directory",
            "description": "MyPy type checking cache",
            "safe": True,
        },
        {
            "name": "Ruff Cache",
            "patterns": ["**/.ruff_cache", "**/.ruff_cache/**"],
            "type": "directory",
            "description": "Ruff linter cache",
            "safe": True,
        },
        {
            "name": "Egg Info",
            "patterns": ["**/*.egg-info", "**/*.egg-info/**"],
            "type": "directory",
            "description": "Python egg metadata",
            "safe": True,
        },
        {
            "name": "Distribution",
            "patterns": ["dist/**", "build/**"],
            "type": "directory",
            "description": "Python distribution and build directories",
            "safe": True,
        },
        {
            "name": "Eggs",
            "patterns": ["**/*.egg"],
            "type": "file",
            "description": "Python egg packages",
            "safe": True,
        },
        {
            "name": "Tox",
            "patterns": [".tox/**"],
            "type": "directory",
            "description": "Tox testing environments",
            "safe": True,
        },
        {
            "name": "Coverage",
            "patterns": [".coverage", "htmlcov/**", "coverage.xml"],
            "type": "both",
            "description": "Code coverage data and reports",
            "safe": True,
        },
        {
            "name": "Virtual Environments",
            "patterns": ["venv/**", "env/**", ".venv/**", ".env/**"],
            "type": "directory",
            "description": "Python virtual environments",
            "safe": False,
            "requires_confirmation": True,
        },
    ],
    
    "node": [
        {
            "name": "Node Modules",
            "patterns": ["**/node_modules", "**/node_modules/**"],
            "type": "directory",
            "description": "NPM/Yarn dependency directories",
            "safe": True,
            "requires_confirmation": True,
        },
        {
            "name": "Distribution",
            "patterns": ["dist/**"],
            "type": "directory",
            "description": "Built distribution files",
            "safe": True,
        },
        {
            "name": "Build Output",
            "patterns": ["build/**", "out/**"],
            "type": "directory",
            "description": "Build output directories",
            "safe": True,
        },
        {
            "name": "Cache Directories",
            "patterns": [".cache/**", ".parcel-cache/**"],
            "type": "directory",
            "description": "Various cache directories",
            "safe": True,
        },
        {
            "name": "NPM Logs",
            "patterns": ["npm-debug.log*", "yarn-debug.log*", "yarn-error.log*", "lerna-debug.log*"],
            "type": "file",
            "description": "Package manager debug logs",
            "safe": True,
        },
        {
            "name": "Yarn Cache",
            "patterns": [".yarn/cache/**", ".pnp/**", ".pnp.js"],
            "type": "both",
            "description": "Yarn 2+ cache and PnP files",
            "safe": True,
        },
        {
            "name": "Coverage",
            "patterns": ["coverage/**", ".nyc_output/**"],
            "type": "directory",
            "description": "Test coverage reports",
            "safe": True,
        },
        {
            "name": "TypeScript Build",
            "patterns": ["*.tsbuildinfo"],
            "type": "file",
            "description": "TypeScript incremental build info",
            "safe": True,
        },
    ],
    
    "java": [
        {
            "name": "Maven Target",
            "patterns": ["target/**"],
            "type": "directory",
            "description": "Maven build output directory",
            "safe": True,
        },
        {
            "name": "Gradle Build",
            "patterns": ["build/**", "out/**"],
            "type": "directory",
            "description": "Gradle build output directories",
            "safe": True,
        },
        {
            "name": "Class Files",
            "patterns": ["**/*.class"],
            "type": "file",
            "description": "Compiled Java class files",
            "safe": True,
        },
        {
            "name": "JAR Files",
            "patterns": ["**/*.jar"],
            "type": "file",
            "description": "Java archive files",
            "safe": False,
            "requires_confirmation": True,
        },
        {
            "name": "Gradle Cache",
            "patterns": [".gradle/**"],
            "type": "directory",
            "description": "Gradle cache directory",
            "safe": True,
        },
        {
            "name": "IntelliJ Output",
            "patterns": [".idea/**/*.xml"],
            "type": "file",
            "description": "IntelliJ IDEA configuration files",
            "safe": False,
            "requires_confirmation": True,
        },
    ],
    
    "c_cpp": [
        {
            "name": "Object Files",
            "patterns": ["**/*.o", "**/*.obj"],
            "type": "file",
            "description": "Compiled object files",
            "safe": True,
        },
        {
            "name": "Static Libraries",
            "patterns": ["**/*.a", "**/*.lib"],
            "type": "file",
            "description": "Static library files",
            "safe": True,
        },
        {
            "name": "Shared Libraries",
            "patterns": ["**/*.so", "**/*.so.*", "**/*.dylib", "**/*.dll"],
            "type": "file",
            "description": "Shared/dynamic library files",
            "safe": False,
            "requires_confirmation": True,
        },
        {
            "name": "Executables",
            "patterns": ["**/*.exe", "**/*.out"],
            "type": "file",
            "description": "Executable files",
            "safe": False,
            "requires_confirmation": True,
        },
        {
            "name": "CMake Build",
            "patterns": ["build/**", "cmake-build-*/**", "build-*/**"],
            "type": "directory",
            "description": "CMake build directories",
            "safe": True,
        },
        {
            "name": "Debug Symbols",
            "patterns": ["**/*.dSYM/**", "**/*.pdb"],
            "type": "both",
            "description": "Debug symbol files",
            "safe": True,
        },
        {
            "name": "Precompiled Headers",
            "patterns": ["**/*.gch", "**/*.pch"],
            "type": "file",
            "description": "Precompiled header files",
            "safe": True,
        },
        {
            "name": "CMake Cache",
            "patterns": ["CMakeCache.txt", "CMakeFiles/**"],
            "type": "both",
            "description": "CMake cache files",
            "safe": True,
        },
    ],
    
    "react": [
        {
            "name": "Next.js Build",
            "patterns": [".next/**"],
            "type": "directory",
            "description": "Next.js build output",
            "safe": True,
        },
        {
            "name": "CRA Build",
            "patterns": ["build/**"],
            "type": "directory",
            "description": "Create React App build output",
            "safe": True,
        },
        {
            "name": "React Cache",
            "patterns": [".cache/**"],
            "type": "directory",
            "description": "React/Gatsby cache",
            "safe": True,
        },
    ],
    
    "angular": [
        {
            "name": "Angular Build",
            "patterns": ["dist/**"],
            "type": "directory",
            "description": "Angular build output",
            "safe": True,
        },
        {
            "name": "Angular Cache",
            "patterns": [".angular/**"],
            "type": "directory",
            "description": "Angular CLI cache",
            "safe": True,
        },
    ],
    
    "vue": [
        {
            "name": "Vue Build",
            "patterns": ["dist/**"],
            "type": "directory",
            "description": "Vue build output",
            "safe": True,
        },
        {
            "name": "Vite Cache",
            "patterns": [".vite/**"],
            "type": "directory",
            "description": "Vite build cache",
            "safe": True,
        },
        {
            "name": "Nuxt Build",
            "patterns": [".nuxt/**", ".output/**"],
            "type": "directory",
            "description": "Nuxt.js build output",
            "safe": True,
        },
    ],
}

# Default safety settings
DEFAULT_SAFETY = {
    "require_git": False,
    "min_free_space_mb": 100,
    "max_delete_size_mb": 0,  # 0 = no limit
}

# Default global exclude patterns
DEFAULT_EXCLUDES = [
    "**/vendor/**",
    "**/.git/**",
]


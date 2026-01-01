"""C/C++ project cleaner."""

from typing import List

from repo_cleaner.cleaners.base import BaseCleaner, Pattern, PatternType


class CCppCleaner(BaseCleaner):
    """Cleaner for C/C++ project artifacts.
    
    Cleans:
    - Object files (*.o, *.obj)
    - Static libraries (*.a, *.lib)
    - Shared libraries (*.so, *.dylib, *.dll)
    - Build directories
    - CMake cache
    - Debug symbols
    """
    
    @property
    def name(self) -> str:
        """Return cleaner name."""
        return "c_cpp"
    
    @property
    def display_name(self) -> str:
        """Return display name."""
        return "C/C++"
    
    def get_patterns(self) -> List[Pattern]:
        """Return list of patterns to clean."""
        return [
            Pattern(
                name="Object Files",
                patterns=["**/*.o", "**/*.obj"],
                type=PatternType.FILE,
                description="Compiled object files",
                safe=True,
            ),
            Pattern(
                name="Static Libraries",
                patterns=["**/*.a", "**/*.lib"],
                type=PatternType.FILE,
                description="Static library files",
                safe=True,
            ),
            Pattern(
                name="Unix Shared Libraries",
                patterns=["**/*.so", "**/*.so.*"],
                type=PatternType.FILE,
                description="Unix shared library files",
                safe=False,
                requires_confirmation=True,
            ),
            Pattern(
                name="macOS Shared Libraries",
                patterns=["**/*.dylib"],
                type=PatternType.FILE,
                description="macOS dynamic library files",
                safe=False,
                requires_confirmation=True,
            ),
            Pattern(
                name="Windows Shared Libraries",
                patterns=["**/*.dll"],
                type=PatternType.FILE,
                description="Windows DLL files",
                safe=False,
                requires_confirmation=True,
            ),
            Pattern(
                name="Windows Executables",
                patterns=["**/*.exe"],
                type=PatternType.FILE,
                description="Windows executable files",
                safe=False,
                requires_confirmation=True,
            ),
            Pattern(
                name="Build Directory",
                patterns=["build"],
                type=PatternType.DIRECTORY,
                description="Build output directory",
                safe=True,
            ),
            Pattern(
                name="CMake Build Directories",
                patterns=["cmake-build-*"],
                type=PatternType.DIRECTORY,
                description="CMake IDE build directories",
                safe=True,
            ),
            Pattern(
                name="CMake Cache",
                patterns=["CMakeCache.txt"],
                type=PatternType.FILE,
                description="CMake cache file",
                safe=True,
            ),
            Pattern(
                name="CMake Files",
                patterns=["CMakeFiles"],
                type=PatternType.DIRECTORY,
                description="CMake generated files",
                safe=True,
            ),
            Pattern(
                name="macOS Debug Symbols",
                patterns=["**/*.dSYM"],
                type=PatternType.DIRECTORY,
                description="macOS debug symbol bundles",
                safe=True,
            ),
            Pattern(
                name="Windows Debug Symbols",
                patterns=["**/*.pdb"],
                type=PatternType.FILE,
                description="Windows program database files",
                safe=True,
            ),
            Pattern(
                name="Precompiled Headers",
                patterns=["**/*.gch", "**/*.pch"],
                type=PatternType.FILE,
                description="Precompiled header files",
                safe=True,
            ),
            Pattern(
                name="Dependency Files",
                patterns=["**/*.d"],
                type=PatternType.FILE,
                description="Make dependency files",
                safe=True,
            ),
            Pattern(
                name="Core Dumps",
                patterns=["core", "core.*"],
                type=PatternType.FILE,
                description="Core dump files",
                safe=True,
            ),
        ]


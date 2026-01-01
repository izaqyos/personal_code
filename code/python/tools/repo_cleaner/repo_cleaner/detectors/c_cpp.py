"""C/C++ project detector."""

from pathlib import Path
from typing import List

from repo_cleaner.detectors.base import BaseDetector


class CCppDetector(BaseDetector):
    """Detector for C/C++ projects.
    
    Identifies C/C++ projects by looking for:
    - CMakeLists.txt
    - Makefile
    - configure.ac (autotools)
    - *.c, *.cpp, *.h, *.hpp files
    - build directories
    """
    
    INDICATORS = {
        "CMakeLists.txt": 0.95,
        "Makefile": 0.8,
        "makefile": 0.8,
        "GNUmakefile": 0.8,
        "configure.ac": 0.85,
        "configure": 0.7,
        "meson.build": 0.9,
        "conanfile.txt": 0.8,
        "conanfile.py": 0.8,
        "vcpkg.json": 0.8,
        ".clang-format": 0.5,
        ".clang-tidy": 0.5,
        "compile_commands.json": 0.6,
    }
    
    # Source file extensions
    SOURCE_EXTENSIONS = [".c", ".cpp", ".cc", ".cxx", ".c++"]
    HEADER_EXTENSIONS = [".h", ".hpp", ".hh", ".hxx", ".h++"]
    
    @property
    def name(self) -> str:
        """Return detector name."""
        return "c_cpp"
    
    @property
    def display_name(self) -> str:
        """Return display name."""
        return "C/C++"
    
    def detect(self, path: Path) -> bool:
        """Check if this is a C/C++ project.
        
        Args:
            path: Path to check
            
        Returns:
            True if C/C++ project detected
        """
        path = Path(path)
        
        # Check for indicator files
        for indicator in self.INDICATORS.keys():
            if self._has_file(path, indicator):
                return True
        
        # Check for source files
        for ext in self.SOURCE_EXTENSIONS:
            if self._has_files_with_extension(path, ext, recursive=False):
                return True
        
        # Check for header files
        for ext in self.HEADER_EXTENSIONS:
            if self._has_files_with_extension(path, ext, recursive=False):
                return True
        
        # Check for build directories with typical names
        for build_dir in ["build", "cmake-build-debug", "cmake-build-release"]:
            if self._has_directory(path, build_dir):
                return True
        
        return False
    
    def get_confidence(self, path: Path) -> float:
        """Calculate confidence score.
        
        Args:
            path: Path to project
            
        Returns:
            Confidence score 0.0 to 1.0
        """
        path = Path(path)
        max_confidence = 0.0
        
        # Check indicator files
        for indicator, weight in self.INDICATORS.items():
            if self._has_file(path, indicator):
                max_confidence = max(max_confidence, weight)
        
        # Count source files
        source_count = sum(
            self._count_files_with_extension(path, ext, recursive=True)
            for ext in self.SOURCE_EXTENSIONS
        )
        header_count = sum(
            self._count_files_with_extension(path, ext, recursive=True)
            for ext in self.HEADER_EXTENSIONS
        )
        
        total_files = source_count + header_count
        
        if total_files > 20:
            max_confidence = max(max_confidence, 0.9)
        elif total_files > 5:
            max_confidence = max(max_confidence, 0.7)
        elif total_files > 0:
            max_confidence = max(max_confidence, 0.5)
        
        return max_confidence
    
    def get_indicators(self, path: Path) -> List[str]:
        """Get list of detected indicators.
        
        Args:
            path: Path to project
            
        Returns:
            List of indicator descriptions
        """
        path = Path(path)
        indicators = []
        
        # Check build system
        if self._has_file(path, "CMakeLists.txt"):
            indicators.append("Found CMakeLists.txt (CMake project)")
        if self._has_file(path, "Makefile") or self._has_file(path, "makefile"):
            indicators.append("Found Makefile")
        if self._has_file(path, "meson.build"):
            indicators.append("Found meson.build (Meson project)")
        if self._has_file(path, "configure.ac"):
            indicators.append("Found configure.ac (Autotools project)")
        
        for indicator in self.INDICATORS.keys():
            if indicator not in ["CMakeLists.txt", "Makefile", "makefile", "meson.build", "configure.ac"]:
                if self._has_file(path, indicator):
                    indicators.append(f"Found {indicator}")
        
        # Count source files
        source_count = sum(
            self._count_files_with_extension(path, ext, recursive=True)
            for ext in self.SOURCE_EXTENSIONS
        )
        header_count = sum(
            self._count_files_with_extension(path, ext, recursive=True)
            for ext in self.HEADER_EXTENSIONS
        )
        
        if source_count > 0:
            indicators.append(f"Found {source_count} source files")
        if header_count > 0:
            indicators.append(f"Found {header_count} header files")
        
        # Check for build directories
        for build_dir in ["build", "cmake-build-debug", "cmake-build-release"]:
            if self._has_directory(path, build_dir):
                indicators.append(f"Found {build_dir} directory")
        
        return indicators
    
    def get_build_system(self, path: Path) -> str:
        """Detect which build system is used.
        
        Args:
            path: Path to project
            
        Returns:
            Build system name ('cmake', 'make', 'meson', 'autotools', or 'unknown')
        """
        path = Path(path)
        
        if self._has_file(path, "CMakeLists.txt"):
            return "cmake"
        if self._has_file(path, "meson.build"):
            return "meson"
        if self._has_file(path, "configure.ac"):
            return "autotools"
        if self._has_file(path, "Makefile") or self._has_file(path, "makefile"):
            return "make"
        
        return "unknown"


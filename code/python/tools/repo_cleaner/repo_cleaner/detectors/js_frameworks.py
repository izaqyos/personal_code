"""JavaScript framework detectors (React, Angular, Vue)."""

from pathlib import Path
from typing import List, Optional
import json

from repo_cleaner.detectors.base import BaseDetector


class JSFrameworkDetector(BaseDetector):
    """Base class for JS framework detectors.
    
    Provides common functionality for detecting JS frameworks
    by analyzing package.json dependencies.
    """
    
    FRAMEWORK_PACKAGES: List[str] = []
    INDICATOR_FILES: List[str] = []
    
    def _has_package_dependency(self, path: Path, packages: List[str]) -> bool:
        """Check if package.json has any of the specified dependencies.
        
        Args:
            path: Path to project
            packages: List of package names to check
            
        Returns:
            True if any package is found in dependencies
        """
        package_json = path / "package.json"
        if not package_json.is_file():
            return False
        
        try:
            with open(package_json, "r", encoding="utf-8") as f:
                pkg = json.load(f)
            
            deps = set(pkg.get("dependencies", {}).keys())
            dev_deps = set(pkg.get("devDependencies", {}).keys())
            all_deps = deps | dev_deps
            
            return any(p in all_deps for p in packages)
        except (json.JSONDecodeError, OSError):
            return False
    
    def _get_package_version(self, path: Path, package: str) -> Optional[str]:
        """Get version of a package from package.json.
        
        Args:
            path: Path to project
            package: Package name
            
        Returns:
            Version string or None
        """
        package_json = path / "package.json"
        if not package_json.is_file():
            return None
        
        try:
            with open(package_json, "r", encoding="utf-8") as f:
                pkg = json.load(f)
            
            deps = pkg.get("dependencies", {})
            dev_deps = pkg.get("devDependencies", {})
            
            return deps.get(package) or dev_deps.get(package)
        except (json.JSONDecodeError, OSError):
            return None


class ReactDetector(JSFrameworkDetector):
    """Detector for React projects.
    
    Identifies React projects by looking for:
    - react/react-dom in package.json
    - next.config.js (Next.js)
    - .next directory
    - JSX/TSX files
    """
    
    FRAMEWORK_PACKAGES = ["react", "react-dom", "next", "gatsby", "remix"]
    INDICATOR_FILES = [
        "next.config.js",
        "next.config.mjs",
        "next.config.ts",
        "gatsby-config.js",
        "gatsby-config.ts",
        "remix.config.js",
    ]
    
    @property
    def name(self) -> str:
        """Return detector name."""
        return "react"
    
    @property
    def display_name(self) -> str:
        """Return display name."""
        return "React"
    
    def detect(self, path: Path) -> bool:
        """Check if this is a React project.
        
        Args:
            path: Path to check
            
        Returns:
            True if React project detected
        """
        path = Path(path)
        
        # Check for React packages
        if self._has_package_dependency(path, self.FRAMEWORK_PACKAGES):
            return True
        
        # Check for framework-specific files
        for indicator in self.INDICATOR_FILES:
            if self._has_file(path, indicator):
                return True
        
        # Check for .next directory
        if self._has_directory(path, ".next"):
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
        confidence = 0.0
        
        # Check for React core packages
        if self._has_package_dependency(path, ["react", "react-dom"]):
            confidence = 0.95
        
        # Check for framework-specific files
        for indicator in self.INDICATOR_FILES:
            if self._has_file(path, indicator):
                confidence = max(confidence, 0.9)
        
        # Check for .next directory
        if self._has_directory(path, ".next"):
            confidence = max(confidence, 0.85)
        
        # Check for JSX/TSX files
        jsx_count = self._count_files_with_extension(path, ".jsx", recursive=True)
        tsx_count = self._count_files_with_extension(path, ".tsx", recursive=True)
        
        if jsx_count + tsx_count > 5:
            confidence = max(confidence, 0.8)
        
        return confidence
    
    def get_indicators(self, path: Path) -> List[str]:
        """Get list of detected indicators."""
        path = Path(path)
        indicators = []
        
        # Check packages
        for pkg in self.FRAMEWORK_PACKAGES:
            version = self._get_package_version(path, pkg)
            if version:
                indicators.append(f"Found {pkg}@{version}")
        
        # Check files
        for indicator in self.INDICATOR_FILES:
            if self._has_file(path, indicator):
                indicators.append(f"Found {indicator}")
        
        if self._has_directory(path, ".next"):
            indicators.append("Found .next build directory")
        
        jsx_count = self._count_files_with_extension(path, ".jsx", recursive=True)
        tsx_count = self._count_files_with_extension(path, ".tsx", recursive=True)
        if jsx_count > 0:
            indicators.append(f"Found {jsx_count} JSX files")
        if tsx_count > 0:
            indicators.append(f"Found {tsx_count} TSX files")
        
        return indicators


class AngularDetector(JSFrameworkDetector):
    """Detector for Angular projects.
    
    Identifies Angular projects by looking for:
    - @angular/core in package.json
    - angular.json
    - .angular directory
    """
    
    FRAMEWORK_PACKAGES = ["@angular/core", "@angular/cli"]
    INDICATOR_FILES = [
        "angular.json",
        ".angular-cli.json",  # Legacy
    ]
    
    @property
    def name(self) -> str:
        """Return detector name."""
        return "angular"
    
    @property
    def display_name(self) -> str:
        """Return display name."""
        return "Angular"
    
    def detect(self, path: Path) -> bool:
        """Check if this is an Angular project."""
        path = Path(path)
        
        # Check for Angular packages
        if self._has_package_dependency(path, self.FRAMEWORK_PACKAGES):
            return True
        
        # Check for angular.json
        for indicator in self.INDICATOR_FILES:
            if self._has_file(path, indicator):
                return True
        
        # Check for .angular directory
        if self._has_directory(path, ".angular"):
            return True
        
        return False
    
    def get_confidence(self, path: Path) -> float:
        """Calculate confidence score."""
        path = Path(path)
        confidence = 0.0
        
        # Check for Angular packages
        if self._has_package_dependency(path, ["@angular/core"]):
            confidence = 0.95
        
        # Check for angular.json
        if self._has_file(path, "angular.json"):
            confidence = max(confidence, 0.95)
        
        # Check for .angular directory
        if self._has_directory(path, ".angular"):
            confidence = max(confidence, 0.85)
        
        return confidence
    
    def get_indicators(self, path: Path) -> List[str]:
        """Get list of detected indicators."""
        path = Path(path)
        indicators = []
        
        for pkg in self.FRAMEWORK_PACKAGES:
            version = self._get_package_version(path, pkg)
            if version:
                indicators.append(f"Found {pkg}@{version}")
        
        for indicator in self.INDICATOR_FILES:
            if self._has_file(path, indicator):
                indicators.append(f"Found {indicator}")
        
        if self._has_directory(path, ".angular"):
            indicators.append("Found .angular cache directory")
        
        return indicators


class VueDetector(JSFrameworkDetector):
    """Detector for Vue.js projects.
    
    Identifies Vue.js projects by looking for:
    - vue in package.json
    - vue.config.js
    - vite.config.js (with Vue plugin)
    - nuxt.config.js (Nuxt.js)
    """
    
    FRAMEWORK_PACKAGES = ["vue", "nuxt", "@nuxt/core", "vite"]
    INDICATOR_FILES = [
        "vue.config.js",
        "nuxt.config.js",
        "nuxt.config.ts",
        "vite.config.js",
        "vite.config.ts",
    ]
    
    @property
    def name(self) -> str:
        """Return detector name."""
        return "vue"
    
    @property
    def display_name(self) -> str:
        """Return display name."""
        return "Vue.js"
    
    def detect(self, path: Path) -> bool:
        """Check if this is a Vue.js project."""
        path = Path(path)
        
        # Check for Vue packages
        if self._has_package_dependency(path, ["vue"]):
            return True
        
        # Check for Nuxt
        if self._has_package_dependency(path, ["nuxt", "@nuxt/core"]):
            return True
        
        # Check for indicator files
        for indicator in self.INDICATOR_FILES:
            if self._has_file(path, indicator):
                return True
        
        # Check for .nuxt or .vite directories
        if self._has_directory(path, ".nuxt") or self._has_directory(path, ".vite"):
            return True
        
        return False
    
    def get_confidence(self, path: Path) -> float:
        """Calculate confidence score."""
        path = Path(path)
        confidence = 0.0
        
        # Check for Vue package
        if self._has_package_dependency(path, ["vue"]):
            confidence = 0.95
        
        # Check for Nuxt
        if self._has_package_dependency(path, ["nuxt", "@nuxt/core"]):
            confidence = max(confidence, 0.95)
        
        # Check for indicator files
        if self._has_file(path, "vue.config.js"):
            confidence = max(confidence, 0.9)
        if self._has_file(path, "nuxt.config.js") or self._has_file(path, "nuxt.config.ts"):
            confidence = max(confidence, 0.95)
        
        # Check for .vue files
        vue_count = self._count_files_with_extension(path, ".vue", recursive=True)
        if vue_count > 5:
            confidence = max(confidence, 0.85)
        elif vue_count > 0:
            confidence = max(confidence, 0.7)
        
        return confidence
    
    def get_indicators(self, path: Path) -> List[str]:
        """Get list of detected indicators."""
        path = Path(path)
        indicators = []
        
        for pkg in ["vue", "nuxt", "@nuxt/core"]:
            version = self._get_package_version(path, pkg)
            if version:
                indicators.append(f"Found {pkg}@{version}")
        
        for indicator in self.INDICATOR_FILES:
            if self._has_file(path, indicator):
                indicators.append(f"Found {indicator}")
        
        if self._has_directory(path, ".nuxt"):
            indicators.append("Found .nuxt build directory")
        if self._has_directory(path, ".vite"):
            indicators.append("Found .vite cache directory")
        
        vue_count = self._count_files_with_extension(path, ".vue", recursive=True)
        if vue_count > 0:
            indicators.append(f"Found {vue_count} Vue files")
        
        return indicators


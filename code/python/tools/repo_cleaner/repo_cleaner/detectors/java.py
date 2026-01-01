"""Java project detector."""

from pathlib import Path
from typing import List

from repo_cleaner.detectors.base import BaseDetector


class JavaDetector(BaseDetector):
    """Detector for Java projects.
    
    Identifies Java projects by looking for:
    - pom.xml (Maven)
    - build.gradle or build.gradle.kts (Gradle)
    - .java files
    - src/main/java structure
    - .class files
    """
    
    INDICATORS = {
        "pom.xml": 0.95,
        "build.gradle": 0.95,
        "build.gradle.kts": 0.95,
        "settings.gradle": 0.8,
        "settings.gradle.kts": 0.8,
        "gradlew": 0.7,
        "mvnw": 0.7,
        ".mvn": 0.6,
    }
    
    @property
    def name(self) -> str:
        """Return detector name."""
        return "java"
    
    @property
    def display_name(self) -> str:
        """Return display name."""
        return "Java"
    
    def detect(self, path: Path) -> bool:
        """Check if this is a Java project.
        
        Args:
            path: Path to check
            
        Returns:
            True if Java project detected
        """
        path = Path(path)
        
        # Check for build tool files
        for indicator in self.INDICATORS.keys():
            if indicator.startswith("."):
                if self._has_directory(path, indicator):
                    return True
            elif self._has_file(path, indicator):
                return True
        
        # Check for Java source structure
        if (path / "src" / "main" / "java").is_dir():
            return True
        
        # Check for .java files
        if self._has_files_with_extension(path, ".java", recursive=False):
            return True
        
        # Check for target or build directories with class files
        for build_dir in ["target", "build", "out"]:
            if self._has_directory(path, build_dir):
                build_path = path / build_dir
                if self._has_files_with_extension(build_path, ".class", recursive=True):
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
            if indicator.startswith("."):
                if self._has_directory(path, indicator):
                    max_confidence = max(max_confidence, weight)
            elif self._has_file(path, indicator):
                max_confidence = max(max_confidence, weight)
        
        # Check for standard Maven/Gradle structure
        if (path / "src" / "main" / "java").is_dir():
            max_confidence = max(max_confidence, 0.9)
        
        # Check for Java files
        java_count = self._count_files_with_extension(path, ".java", recursive=True)
        if java_count > 10:
            max_confidence = max(max_confidence, 0.85)
        elif java_count > 0:
            max_confidence = max(max_confidence, 0.6)
        
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
        
        # Check build tools
        if self._has_file(path, "pom.xml"):
            indicators.append("Found pom.xml (Maven project)")
        if self._has_file(path, "build.gradle") or self._has_file(path, "build.gradle.kts"):
            indicators.append("Found build.gradle (Gradle project)")
        
        for indicator in self.INDICATORS.keys():
            if indicator not in ["pom.xml", "build.gradle", "build.gradle.kts"]:
                if indicator.startswith("."):
                    if self._has_directory(path, indicator):
                        indicators.append(f"Found {indicator}")
                elif self._has_file(path, indicator):
                    indicators.append(f"Found {indicator}")
        
        # Check structure
        if (path / "src" / "main" / "java").is_dir():
            indicators.append("Found src/main/java structure")
        
        # Count Java files
        java_count = self._count_files_with_extension(path, ".java", recursive=True)
        if java_count > 0:
            indicators.append(f"Found {java_count} Java files")
        
        # Check for build output
        for build_dir in ["target", "build", "out"]:
            if self._has_directory(path, build_dir):
                indicators.append(f"Found {build_dir} directory")
        
        return indicators
    
    def get_build_tool(self, path: Path) -> str:
        """Detect which build tool is used.
        
        Args:
            path: Path to project
            
        Returns:
            Build tool name ('maven', 'gradle', or 'unknown')
        """
        path = Path(path)
        
        if self._has_file(path, "pom.xml"):
            return "maven"
        if self._has_file(path, "build.gradle") or self._has_file(path, "build.gradle.kts"):
            return "gradle"
        
        return "unknown"


"""Node.js project detector."""

from pathlib import Path
from typing import List
import json

from repo_cleaner.detectors.base import BaseDetector


class NodeDetector(BaseDetector):
    """Detector for Node.js projects.
    
    Identifies Node.js projects by looking for:
    - package.json
    - package-lock.json
    - yarn.lock
    - pnpm-lock.yaml
    - node_modules directory
    """
    
    INDICATORS = {
        "package.json": 0.95,
        "package-lock.json": 0.9,
        "yarn.lock": 0.9,
        "pnpm-lock.yaml": 0.9,
        ".npmrc": 0.6,
        ".yarnrc": 0.6,
        ".nvmrc": 0.5,
        ".node-version": 0.5,
    }
    
    @property
    def name(self) -> str:
        """Return detector name."""
        return "node"
    
    @property
    def display_name(self) -> str:
        """Return display name."""
        return "Node.js"
    
    def detect(self, path: Path) -> bool:
        """Check if this is a Node.js project.
        
        Args:
            path: Path to check
            
        Returns:
            True if Node.js project detected
        """
        path = Path(path)
        
        # Primary indicator
        if self._has_file(path, "package.json"):
            return True
        
        # Secondary indicators
        for indicator in self.INDICATORS.keys():
            if self._has_file(path, indicator):
                return True
        
        # Check for node_modules directory
        if self._has_directory(path, "node_modules"):
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
        
        # Check node_modules
        if self._has_directory(path, "node_modules"):
            max_confidence = max(max_confidence, 0.9)
        
        # Analyze package.json if present
        package_json = path / "package.json"
        if package_json.is_file():
            try:
                with open(package_json, "r", encoding="utf-8") as f:
                    pkg = json.load(f)
                
                # Higher confidence if it has dependencies
                if pkg.get("dependencies") or pkg.get("devDependencies"):
                    max_confidence = min(1.0, max_confidence + 0.05)
                
                # Check for scripts
                if pkg.get("scripts"):
                    max_confidence = min(1.0, max_confidence + 0.02)
            except (json.JSONDecodeError, OSError):
                pass
        
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
        
        for indicator in self.INDICATORS.keys():
            if self._has_file(path, indicator):
                indicators.append(f"Found {indicator}")
        
        if self._has_directory(path, "node_modules"):
            indicators.append("Found node_modules directory")
        
        # Get package info
        package_json = path / "package.json"
        if package_json.is_file():
            try:
                with open(package_json, "r", encoding="utf-8") as f:
                    pkg = json.load(f)
                
                if "name" in pkg:
                    indicators.append(f"Package name: {pkg['name']}")
                
                dep_count = len(pkg.get("dependencies", {}))
                dev_dep_count = len(pkg.get("devDependencies", {}))
                
                if dep_count > 0:
                    indicators.append(f"Found {dep_count} dependencies")
                if dev_dep_count > 0:
                    indicators.append(f"Found {dev_dep_count} dev dependencies")
            except (json.JSONDecodeError, OSError):
                pass
        
        return indicators
    
    def get_package_manager(self, path: Path) -> str:
        """Detect which package manager is used.
        
        Args:
            path: Path to project
            
        Returns:
            Package manager name ('npm', 'yarn', 'pnpm', or 'unknown')
        """
        path = Path(path)
        
        if self._has_file(path, "pnpm-lock.yaml"):
            return "pnpm"
        if self._has_file(path, "yarn.lock"):
            return "yarn"
        if self._has_file(path, "package-lock.json"):
            return "npm"
        
        return "unknown"


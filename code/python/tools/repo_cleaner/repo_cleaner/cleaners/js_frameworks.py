"""JavaScript framework cleaners (React, Angular, Vue)."""

from typing import List

from repo_cleaner.cleaners.base import BaseCleaner, Pattern, PatternType


class ReactCleaner(BaseCleaner):
    """Cleaner for React project artifacts.
    
    Cleans:
    - .next directory (Next.js)
    - build directory (Create React App)
    - .cache (Gatsby)
    """
    
    @property
    def name(self) -> str:
        """Return cleaner name."""
        return "react"
    
    @property
    def display_name(self) -> str:
        """Return display name."""
        return "React"
    
    def get_patterns(self) -> List[Pattern]:
        """Return list of patterns to clean."""
        return [
            Pattern(
                name="Next.js Build",
                patterns=[".next"],
                type=PatternType.DIRECTORY,
                description="Next.js build output",
                safe=True,
            ),
            Pattern(
                name="CRA Build",
                patterns=["build"],
                type=PatternType.DIRECTORY,
                description="Create React App build output",
                safe=True,
            ),
            Pattern(
                name="Gatsby Cache",
                patterns=[".cache"],
                type=PatternType.DIRECTORY,
                description="Gatsby cache directory",
                safe=True,
            ),
            Pattern(
                name="Gatsby Public",
                patterns=["public"],
                type=PatternType.DIRECTORY,
                description="Gatsby generated public directory",
                safe=False,
                requires_confirmation=True,
            ),
            Pattern(
                name="Storybook Static",
                patterns=["storybook-static"],
                type=PatternType.DIRECTORY,
                description="Storybook static build",
                safe=True,
            ),
            Pattern(
                name="Next.js Static Export",
                patterns=["out"],
                type=PatternType.DIRECTORY,
                description="Next.js static export output",
                safe=True,
            ),
        ]


class AngularCleaner(BaseCleaner):
    """Cleaner for Angular project artifacts.
    
    Cleans:
    - dist directory
    - .angular cache
    """
    
    @property
    def name(self) -> str:
        """Return cleaner name."""
        return "angular"
    
    @property
    def display_name(self) -> str:
        """Return display name."""
        return "Angular"
    
    def get_patterns(self) -> List[Pattern]:
        """Return list of patterns to clean."""
        return [
            Pattern(
                name="Angular Distribution",
                patterns=["dist"],
                type=PatternType.DIRECTORY,
                description="Angular build output",
                safe=True,
            ),
            Pattern(
                name="Angular Cache",
                patterns=[".angular"],
                type=PatternType.DIRECTORY,
                description="Angular CLI cache",
                safe=True,
            ),
            Pattern(
                name="Angular Coverage",
                patterns=["coverage"],
                type=PatternType.DIRECTORY,
                description="Angular test coverage",
                safe=True,
            ),
        ]


class VueCleaner(BaseCleaner):
    """Cleaner for Vue.js project artifacts.
    
    Cleans:
    - dist directory
    - .nuxt directory (Nuxt.js)
    - .vite cache
    - .output (Nuxt 3)
    """
    
    @property
    def name(self) -> str:
        """Return cleaner name."""
        return "vue"
    
    @property
    def display_name(self) -> str:
        """Return display name."""
        return "Vue.js"
    
    def get_patterns(self) -> List[Pattern]:
        """Return list of patterns to clean."""
        return [
            Pattern(
                name="Vue Distribution",
                patterns=["dist"],
                type=PatternType.DIRECTORY,
                description="Vue build output",
                safe=True,
            ),
            Pattern(
                name="Nuxt Build",
                patterns=[".nuxt"],
                type=PatternType.DIRECTORY,
                description="Nuxt.js build directory",
                safe=True,
            ),
            Pattern(
                name="Nuxt 3 Output",
                patterns=[".output"],
                type=PatternType.DIRECTORY,
                description="Nuxt 3 output directory",
                safe=True,
            ),
            Pattern(
                name="Vite Cache",
                patterns=[".vite"],
                type=PatternType.DIRECTORY,
                description="Vite build cache",
                safe=True,
            ),
            Pattern(
                name="Vue Coverage",
                patterns=["coverage"],
                type=PatternType.DIRECTORY,
                description="Vue test coverage",
                safe=True,
            ),
        ]


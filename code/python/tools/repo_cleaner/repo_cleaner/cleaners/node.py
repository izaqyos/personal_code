"""Node.js project cleaner."""

from typing import List

from repo_cleaner.cleaners.base import BaseCleaner, Pattern, PatternType


class NodeCleaner(BaseCleaner):
    """Cleaner for Node.js project artifacts.
    
    Cleans:
    - node_modules directories
    - dist/, build/, out/ directories
    - Various cache directories
    - Log files
    - Coverage data
    """
    
    @property
    def name(self) -> str:
        """Return cleaner name."""
        return "node"
    
    @property
    def display_name(self) -> str:
        """Return display name."""
        return "Node.js"
    
    def get_patterns(self) -> List[Pattern]:
        """Return list of patterns to clean."""
        return [
            Pattern(
                name="Node Modules",
                patterns=["**/node_modules"],
                type=PatternType.DIRECTORY,
                description="NPM/Yarn dependency directories",
                safe=True,
                requires_confirmation=True,
            ),
            Pattern(
                name="Distribution Directory",
                patterns=["dist"],
                type=PatternType.DIRECTORY,
                description="Built distribution files",
                safe=True,
            ),
            Pattern(
                name="Build Output",
                patterns=["build", "out"],
                type=PatternType.DIRECTORY,
                description="Build output directories",
                safe=True,
            ),
            Pattern(
                name="Cache Directory",
                patterns=[".cache"],
                type=PatternType.DIRECTORY,
                description="General cache directory",
                safe=True,
            ),
            Pattern(
                name="Parcel Cache",
                patterns=[".parcel-cache"],
                type=PatternType.DIRECTORY,
                description="Parcel bundler cache",
                safe=True,
            ),
            Pattern(
                name="NPM Debug Logs",
                patterns=["npm-debug.log*"],
                type=PatternType.FILE,
                description="NPM debug log files",
                safe=True,
            ),
            Pattern(
                name="Yarn Debug Logs",
                patterns=["yarn-debug.log*", "yarn-error.log*"],
                type=PatternType.FILE,
                description="Yarn debug log files",
                safe=True,
            ),
            Pattern(
                name="Lerna Debug Logs",
                patterns=["lerna-debug.log*"],
                type=PatternType.FILE,
                description="Lerna debug log files",
                safe=True,
            ),
            Pattern(
                name="Yarn Cache",
                patterns=[".yarn/cache", ".pnp"],
                type=PatternType.DIRECTORY,
                description="Yarn 2+ cache and PnP",
                safe=True,
            ),
            Pattern(
                name="PnP Files",
                patterns=[".pnp.js", ".pnp.cjs"],
                type=PatternType.FILE,
                description="Yarn PnP loader files",
                safe=True,
            ),
            Pattern(
                name="Coverage Reports",
                patterns=["coverage"],
                type=PatternType.DIRECTORY,
                description="Test coverage reports",
                safe=True,
            ),
            Pattern(
                name="NYC Output",
                patterns=[".nyc_output"],
                type=PatternType.DIRECTORY,
                description="NYC coverage output",
                safe=True,
            ),
            Pattern(
                name="TypeScript Build Info",
                patterns=["**/*.tsbuildinfo"],
                type=PatternType.FILE,
                description="TypeScript incremental build info",
                safe=True,
            ),
            Pattern(
                name="ESLint Cache",
                patterns=[".eslintcache"],
                type=PatternType.FILE,
                description="ESLint cache file",
                safe=True,
            ),
            Pattern(
                name="Turbo Cache",
                patterns=[".turbo"],
                type=PatternType.DIRECTORY,
                description="Turborepo cache",
                safe=True,
            ),
        ]


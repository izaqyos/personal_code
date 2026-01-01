"""Java project cleaner."""

from typing import List

from repo_cleaner.cleaners.base import BaseCleaner, Pattern, PatternType


class JavaCleaner(BaseCleaner):
    """Cleaner for Java project artifacts.
    
    Cleans:
    - target/ directory (Maven)
    - build/, out/ directories (Gradle)
    - .class files
    - .gradle cache
    """
    
    @property
    def name(self) -> str:
        """Return cleaner name."""
        return "java"
    
    @property
    def display_name(self) -> str:
        """Return display name."""
        return "Java"
    
    def get_patterns(self) -> List[Pattern]:
        """Return list of patterns to clean."""
        return [
            Pattern(
                name="Maven Target",
                patterns=["target", "**/target"],
                type=PatternType.DIRECTORY,
                description="Maven build output directory",
                safe=True,
            ),
            Pattern(
                name="Gradle Build",
                patterns=["build"],
                type=PatternType.DIRECTORY,
                description="Gradle build output directory",
                safe=True,
            ),
            Pattern(
                name="IntelliJ Output",
                patterns=["out"],
                type=PatternType.DIRECTORY,
                description="IntelliJ IDEA output directory",
                safe=True,
            ),
            Pattern(
                name="Class Files",
                patterns=["**/*.class"],
                type=PatternType.FILE,
                description="Compiled Java class files",
                safe=True,
            ),
            Pattern(
                name="Gradle Cache",
                patterns=[".gradle"],
                type=PatternType.DIRECTORY,
                description="Gradle cache directory",
                safe=True,
            ),
            Pattern(
                name="Gradle Wrapper JAR",
                patterns=["gradle/wrapper/gradle-wrapper.jar"],
                type=PatternType.FILE,
                description="Gradle wrapper JAR file",
                safe=False,
                requires_confirmation=True,
            ),
            Pattern(
                name="Maven Wrapper JAR",
                patterns=[".mvn/wrapper/maven-wrapper.jar"],
                type=PatternType.FILE,
                description="Maven wrapper JAR file",
                safe=False,
                requires_confirmation=True,
            ),
            Pattern(
                name="JAR Files in Target",
                patterns=["target/**/*.jar"],
                type=PatternType.FILE,
                description="JAR files in target directory",
                safe=True,
            ),
            Pattern(
                name="Log Files",
                patterns=["**/*.log"],
                type=PatternType.FILE,
                description="Log files",
                safe=True,
            ),
            Pattern(
                name="Heap Dumps",
                patterns=["**/*.hprof"],
                type=PatternType.FILE,
                description="Java heap dump files",
                safe=True,
            ),
        ]


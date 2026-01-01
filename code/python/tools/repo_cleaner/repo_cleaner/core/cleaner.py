"""Core cleaner orchestrator for Repo Cleaner."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Type

from repo_cleaner.cleaners import CLEANER_REGISTRY
from repo_cleaner.cleaners.base import BaseCleaner, CleanResult
from repo_cleaner.config.manager import ConfigManager
from repo_cleaner.core.exceptions import (
    CleanError,
    DetectionError,
    RepoCleanerError,
    SafetyCheckError,
)
from repo_cleaner.core.logger import get_logger
from repo_cleaner.detectors import ALL_DETECTORS
from repo_cleaner.detectors.base import BaseDetector, DetectionResult
from repo_cleaner.utils.filesystem import format_size, get_free_space
from repo_cleaner.utils.git import get_git_status_summary, is_git_repository
from repo_cleaner.utils.prompts import (
    confirm_action,
    display_summary,
    print_error,
    print_info,
    print_success,
    print_warning,
)

logger = get_logger()


@dataclass
class CleanSummary:
    """Summary of a complete cleaning operation.
    
    Attributes:
        target_path: Path that was cleaned
        detected_types: List of detected project types
        results: Cleaning results per language
        total_size_found: Total size of items found
        total_size_cleaned: Total size of items cleaned
        dry_run: Whether this was a dry run
        errors: List of errors encountered
    """
    
    target_path: Path
    detected_types: List[str] = field(default_factory=list)
    results: Dict[str, CleanResult] = field(default_factory=dict)
    total_size_found: int = 0
    total_size_cleaned: int = 0
    dry_run: bool = False
    errors: List[str] = field(default_factory=list)
    
    @property
    def success(self) -> bool:
        """Return True if operation was successful."""
        return len(self.errors) == 0


class RepoCleaner:
    """Main orchestrator for repository cleaning operations.
    
    Coordinates:
    - Project type detection
    - Cleaner selection and execution
    - Dry-run and interactive modes
    - Safety checks
    - Result aggregation
    """
    
    def __init__(
        self,
        config: Optional[ConfigManager] = None,
        dry_run: bool = False,
        interactive: bool = True,
        verbose: bool = False,
    ) -> None:
        """Initialize the RepoCleaner.
        
        Args:
            config: Configuration manager (creates default if None)
            dry_run: If True, only report what would be cleaned
            interactive: If True, prompt for confirmations
            verbose: If True, show detailed output
        """
        self.config = config or ConfigManager()
        self.dry_run = dry_run
        self.interactive = interactive
        self.verbose = verbose
        
        # Ensure config is loaded
        self.config.load()
    
    def detect_project_types(self, path: Path) -> Dict[str, DetectionResult]:
        """Detect project types in the given directory.
        
        Args:
            path: Path to scan
            
        Returns:
            Dictionary mapping detector names to detection results
            
        Raises:
            DetectionError: If detection fails
        """
        path = Path(path).resolve()
        
        if not path.is_dir():
            raise DetectionError(
                f"Target path is not a directory: {path}"
            )
        
        results: Dict[str, DetectionResult] = {}
        
        for detector in ALL_DETECTORS:
            try:
                result = detector.full_detect(path)
                if result.detected:
                    # Check if this language is enabled in config
                    if self.config.is_language_enabled(detector.name):
                        results[detector.name] = result
                    elif self.verbose:
                        print_info(f"Skipping disabled detector: {detector.display_name}")
            except Exception as e:
                if self.verbose:
                    print_warning(f"Detector {detector.name} failed: {e}")
        
        return results
    
    def validate_safety_checks(self, path: Path) -> None:
        """Validate all safety checks pass.
        
        Args:
            path: Target path to validate
            
        Raises:
            SafetyCheckError: If any safety check fails
        """
        path = Path(path).resolve()
        safety_config = self.config.get_safety_config()
        
        # Check if git repository is required
        if safety_config.require_git:
            if not is_git_repository(path):
                raise SafetyCheckError(
                    "Target directory is not a git repository",
                    details="Use --no-require-git to override or run inside a git repository",
                )
        
        # Check free disk space
        if safety_config.min_free_space_mb > 0:
            free_space = get_free_space(path)
            min_space_bytes = safety_config.min_free_space_mb * 1024 * 1024
            
            if free_space < min_space_bytes:
                raise SafetyCheckError(
                    f"Insufficient free disk space: {format_size(free_space)}",
                    details=f"Minimum required: {safety_config.min_free_space_mb} MB",
                )
    
    def get_cleaner_for_type(self, project_type: str) -> Optional[BaseCleaner]:
        """Get the appropriate cleaner for a project type.
        
        Args:
            project_type: Project type name
            
        Returns:
            Cleaner instance or None if not found
        """
        cleaner_class = CLEANER_REGISTRY.get(project_type)
        if cleaner_class:
            return cleaner_class()
        return None
    
    def clean(
        self,
        path: Path,
        languages: Optional[List[str]] = None,
        exclude_patterns: Optional[List[str]] = None,
    ) -> CleanSummary:
        """Execute the cleaning operation.
        
        Args:
            path: Root path to clean
            languages: Optional list of languages to clean (None = auto-detect)
            exclude_patterns: Optional additional exclude patterns
            
        Returns:
            CleanSummary with operation results
            
        Raises:
            RepoCleanerError: If cleaning fails
        """
        path = Path(path).resolve()
        summary = CleanSummary(target_path=path, dry_run=self.dry_run)
        
        # Validate safety checks
        try:
            self.validate_safety_checks(path)
        except SafetyCheckError as e:
            summary.errors.append(str(e))
            return summary
        
        # Detect project types or use specified languages
        if languages:
            # Use specified languages
            detected_types = {
                lang: DetectionResult(
                    detected=True,
                    confidence=1.0,
                    detector_name=lang,
                    indicators=["Specified by user"],
                )
                for lang in languages
                if self.config.is_language_enabled(lang)
            }
        else:
            # Auto-detect
            detected_types = self.detect_project_types(path)
        
        if not detected_types:
            print_info("No project types detected.")
            return summary
        
        summary.detected_types = list(detected_types.keys())
        
        # Show detection results
        if self.verbose or self.interactive:
            print_info(f"Detected project types: {', '.join(summary.detected_types)}")
            for name, result in detected_types.items():
                if self.verbose and result.indicators:
                    for indicator in result.indicators:
                        print(f"  - {indicator}")
        
        # Merge exclude patterns
        all_exclude_patterns = list(self.config.config.exclude)
        if exclude_patterns:
            all_exclude_patterns.extend(exclude_patterns)
        
        # Process each detected type
        for project_type, detection in detected_types.items():
            cleaner = self.get_cleaner_for_type(project_type)
            if not cleaner:
                if self.verbose:
                    print_warning(f"No cleaner available for: {project_type}")
                continue
            
            # Get language-specific exclude patterns
            lang_excludes = all_exclude_patterns + self.config.get_exclude_patterns(project_type)
            
            # Execute cleaning
            try:
                result = self._execute_cleaner(
                    cleaner, path, lang_excludes
                )
                summary.results[project_type] = result
                summary.total_size_found += result.total_size_found
                summary.total_size_cleaned += result.total_size_cleaned
                
                if result.errors:
                    summary.errors.extend(result.errors)
            except Exception as e:
                error_msg = f"Failed to clean {project_type}: {e}"
                summary.errors.append(error_msg)
                print_error(error_msg)
        
        # Display summary
        self._display_summary(summary)
        
        return summary
    
    def _execute_cleaner(
        self,
        cleaner: BaseCleaner,
        path: Path,
        exclude_patterns: List[str],
    ) -> CleanResult:
        """Execute a single cleaner.
        
        Args:
            cleaner: Cleaner instance to execute
            path: Target path
            exclude_patterns: Patterns to exclude
            
        Returns:
            CleanResult from the cleaner
        """
        if self.verbose:
            print_info(f"Running {cleaner.display_name} cleaner...")
        
        # Find items first
        items = cleaner.find_items(path, exclude_patterns)
        
        if not items:
            if self.verbose:
                print_info(f"No items found for {cleaner.display_name}")
            return CleanResult(cleaner_name=cleaner.name, dry_run=self.dry_run)
        
        # Calculate total size
        total_size = sum(item.size for item in items)
        
        # Show items
        if self.verbose or self.interactive:
            print(f"\n{cleaner.display_name} items to clean:")
            for item in items[:10]:  # Show first 10
                size_str = format_size(item.size)
                item_type = "DIR " if item.is_directory else "FILE"
                print(f"  [{item_type}] {item.path.relative_to(path)} ({size_str})")
            if len(items) > 10:
                print(f"  ... and {len(items) - 10} more items")
            print(f"  Total: {len(items)} items, {format_size(total_size)}")
        
        # Interactive confirmation
        if self.interactive and not self.dry_run:
            # Check if any items require confirmation
            patterns = cleaner.get_patterns()
            requires_confirm = any(
                p.requires_confirmation
                for p in patterns
                if any(i.pattern_name == p.name for i in items)
            )
            
            if requires_confirm:
                print_warning("Some items require confirmation before deletion.")
            
            if not confirm_action(
                f"Clean {len(items)} {cleaner.display_name} items ({format_size(total_size)})?",
                default=False,
                non_interactive=not self.interactive,
            ):
                print_info(f"Skipped {cleaner.display_name} cleaning")
                return CleanResult(
                    cleaner_name=cleaner.name,
                    items_found=items,
                    items_skipped=items,
                    total_size_found=total_size,
                    dry_run=self.dry_run,
                )
        
        # Execute clean
        return cleaner.clean(path, dry_run=self.dry_run, exclude_patterns=exclude_patterns)
    
    def _display_summary(self, summary: CleanSummary) -> None:
        """Display cleaning summary.
        
        Args:
            summary: CleanSummary to display
        """
        print("\n" + "=" * 60)
        
        if summary.dry_run:
            print_warning("DRY RUN - No files were actually deleted")
        
        if summary.success:
            print_success(
                f"Cleaning complete! "
                f"Freed {format_size(summary.total_size_cleaned)} "
                f"from {sum(r.cleaned_count for r in summary.results.values())} items"
            )
        else:
            print_error(f"Cleaning completed with {len(summary.errors)} errors")
        
        # Per-language breakdown
        if self.verbose and summary.results:
            items = [
                (f"{name} ({result.cleaned_count} items)", result.total_size_cleaned)
                for name, result in summary.results.items()
            ]
            if items:
                display_summary(
                    "Breakdown by language:",
                    items,
                    summary.total_size_cleaned,
                )
        
        print("=" * 60 + "\n")


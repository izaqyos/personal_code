"""Monorepo cleaner that handles multi-project repositories."""

import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from repo_cleaner.cleaners import CLEANER_REGISTRY
from repo_cleaner.cleaners.base import BaseCleaner, CleanResult
from repo_cleaner.config.manager import ConfigManager
from repo_cleaner.core.history import (
    CleanupReport,
    CleanedItem,
    HistoryManager,
    ProjectCleanReport,
    generate_report_id,
)
from repo_cleaner.core.layout import LayoutManager
from repo_cleaner.core.logger import get_logger
from repo_cleaner.core.scanner import DetectedProject, MonorepoScanner, ScanLayout
from repo_cleaner.utils.filesystem import format_size
from repo_cleaner.utils.prompts import (
    confirm_action,
    print_error,
    print_info,
    print_success,
    print_warning,
)

logger = get_logger()


class MonorepoCleaner:
    """Cleaner for monorepos with multiple projects.
    
    Handles:
    - Recursive scanning for projects
    - Layout caching (24h expiry)
    - Per-project confirmation
    - Iterative cleaning
    - Report generation and history
    """
    
    def __init__(
        self,
        config: Optional[ConfigManager] = None,
        dry_run: bool = False,
        force: bool = False,
        verbose: bool = False,
        rescan: bool = False,
        detailed_report: bool = False,
    ) -> None:
        """Initialize the monorepo cleaner.
        
        Args:
            config: Configuration manager
            dry_run: If True, only report what would be cleaned
            force: If True, skip all confirmations
            verbose: If True, show detailed output
            rescan: If True, force a fresh scan (ignore cache)
            detailed_report: If True, include item details in report
        """
        self.config = config or ConfigManager()
        self.dry_run = dry_run
        self.force = force
        self.verbose = verbose
        self.rescan = rescan
        self.detailed_report = detailed_report
        
        # Ensure config is loaded
        self.config.load()
        
        # Initialize managers
        self.layout_manager = LayoutManager()
        self.history_manager = HistoryManager()
        self.scanner = MonorepoScanner()
    
    def clean(
        self,
        path: Path,
        languages: Optional[List[str]] = None,
        exclude_patterns: Optional[List[str]] = None,
    ) -> CleanupReport:
        """Clean a monorepo.
        
        Args:
            path: Root path to clean
            languages: Optional list of languages to clean
            exclude_patterns: Optional additional exclude patterns
            
        Returns:
            CleanupReport with results
        """
        start_time = time.time()
        path = Path(path).resolve()
        
        # Initialize report
        report = CleanupReport(
            id=generate_report_id(),
            timestamp=datetime.now().isoformat(),
            root_path=str(path),
            dry_run=self.dry_run,
        )
        
        # Step 1: Get or create layout
        layout = self._get_layout(path, languages)
        
        if not layout.projects:
            print_info("No projects detected in the repository.")
            return report
        
        # Show layout
        if self.verbose:
            self.scanner.print_layout(layout)
        else:
            self._print_summary(layout)
        
        # Step 2: Confirm if not force mode
        if not self.force and not self.dry_run:
            if not confirm_action(
                f"\nProceed to clean {layout.total_projects} projects?",
                default=False,
            ):
                print_info("Operation cancelled.")
                return report
        
        # Step 3: Clean each project
        exclude_patterns = exclude_patterns or []
        exclude_patterns.extend(self.config.config.exclude)
        
        for project in layout.projects:
            project_report = self._clean_project(
                project, exclude_patterns, languages
            )
            report.project_reports.append(project_report)
            report.total_items += project_report.items_cleaned
            report.total_size += project_report.size_cleaned
        
        report.total_projects = len([
            p for p in report.project_reports if p.items_cleaned > 0
        ])
        report.duration_seconds = time.time() - start_time
        
        # Step 4: Save report to history
        self.history_manager.add_report(report, detailed=self.detailed_report)
        
        # Step 5: Display final summary
        self._print_final_summary(report)
        
        return report
    
    def _get_layout(
        self,
        path: Path,
        languages: Optional[List[str]] = None,
    ) -> ScanLayout:
        """Get layout from cache or scan fresh.
        
        Args:
            path: Root path to scan
            languages: Optional language filter
            
        Returns:
            ScanLayout
        """
        # Check cache unless rescan requested
        if not self.rescan:
            cached = self.layout_manager.load_layout(path)
            if cached:
                cache_age = self.layout_manager.get_cache_age(path)
                age_str = f"{cache_age.total_seconds() / 3600:.1f}h" if cache_age else "unknown"
                print_info(f"Using cached layout (age: {age_str}). Use --rescan to refresh.")
                return cached
        
        # Scan fresh
        print_info("Scanning for projects...")
        
        # Filter by enabled languages
        enabled_languages = languages
        if not enabled_languages:
            # Get enabled languages from config
            enabled_languages = [
                lang for lang in CLEANER_REGISTRY.keys()
                if self.config.is_language_enabled(lang)
            ]
        
        scanner = MonorepoScanner(enabled_languages=enabled_languages)
        layout = scanner.scan(path)
        
        # Save to cache
        self.layout_manager.save_layout(layout)
        
        return layout
    
    def _clean_project(
        self,
        project: DetectedProject,
        exclude_patterns: List[str],
        languages: Optional[List[str]] = None,
    ) -> ProjectCleanReport:
        """Clean a single project.
        
        Args:
            project: Project to clean
            exclude_patterns: Patterns to exclude
            languages: Optional language filter
            
        Returns:
            ProjectCleanReport
        """
        project_path = Path(project.path)
        
        report = ProjectCleanReport(
            path=project.path,
            relative_path=project.relative_path,
            project_types=project.project_types,
        )
        
        # Determine which languages to clean
        types_to_clean = project.project_types
        if languages:
            types_to_clean = [t for t in types_to_clean if t in languages]
        
        if not types_to_clean:
            return report
        
        # Per-project confirmation (if not force and not dry-run)
        if not self.force and not self.dry_run:
            path_display = project.relative_path if project.relative_path != "." else "(root)"
            types_display = ", ".join(types_to_clean)
            
            if not confirm_action(
                f"Clean {path_display} ({types_display})?",
                default=True,  # Default to yes for per-project
            ):
                print_info(f"  Skipped: {path_display}")
                return report
        
        # Clean each type
        for project_type in types_to_clean:
            cleaner = self._get_cleaner(project_type)
            if not cleaner:
                continue
            
            # Get language-specific excludes
            lang_excludes = list(exclude_patterns)
            lang_excludes.extend(self.config.get_exclude_patterns(project_type))
            
            try:
                result = cleaner.clean(
                    project_path,
                    dry_run=self.dry_run,
                    exclude_patterns=lang_excludes,
                )
                
                # Aggregate results
                report.items_cleaned += result.cleaned_count
                report.size_cleaned += result.total_size_cleaned
                
                # Add detailed items if requested
                if self.detailed_report:
                    for item in result.items_cleaned:
                        report.items.append(CleanedItem(
                            path=str(item.path),
                            size=item.size,
                            is_directory=item.is_directory,
                            pattern_name=item.pattern_name,
                        ))
                
                # Add errors
                report.errors.extend(result.errors)
                
            except Exception as e:
                error_msg = f"Error cleaning {project_type}: {e}"
                report.errors.append(error_msg)
                logger.error(error_msg)
        
        # Print progress
        if report.items_cleaned > 0 or self.verbose:
            path_display = project.relative_path if project.relative_path != "." else "(root)"
            size_str = format_size(report.size_cleaned)
            mode = "[DRY RUN] " if self.dry_run else ""
            print(f"  {mode}{path_display}: {report.items_cleaned} items, {size_str}")
        
        return report
    
    def _get_cleaner(self, project_type: str) -> Optional[BaseCleaner]:
        """Get a cleaner for a project type.
        
        Args:
            project_type: Type of project
            
        Returns:
            Cleaner instance or None
        """
        cleaner_class = CLEANER_REGISTRY.get(project_type)
        if cleaner_class:
            return cleaner_class()
        return None
    
    def _print_summary(self, layout: ScanLayout) -> None:
        """Print a brief layout summary.
        
        Args:
            layout: Layout to summarize
        """
        summary = layout.get_summary()
        
        print()
        print("=" * 60)
        print(f"  Monorepo: {layout.root_path}")
        print(f"  Found {layout.total_projects} projects")
        print("=" * 60)
        
        for lang, count in sorted(summary.items()):
            print(f"  - {lang}: {count} project(s)")
        
        print()
    
    def _print_final_summary(self, report: CleanupReport) -> None:
        """Print final cleanup summary.
        
        Args:
            report: Cleanup report
        """
        from repo_cleaner.utils.prompts import display_summary
        
        print()
        print("=" * 60)
        
        if report.dry_run:
            print_warning("DRY RUN - No files were actually deleted")
        
        total_size = format_size(report.total_size)
        duration = f"{report.duration_seconds:.1f}s"
        
        if report.success:
            print_success(
                f"Cleanup complete! "
                f"Cleaned {report.total_items} items ({total_size}) "
                f"from {report.total_projects} projects in {duration}"
            )
        else:
            error_count = len(report.errors) + sum(
                len(p.errors) for p in report.project_reports
            )
            print_error(f"Cleanup completed with {error_count} errors")
        
        # Summary by language
        if self.verbose:
            lang_summary = report.get_summary_by_language()
            if lang_summary:
                print()
                print("By language:")
                for lang, stats in sorted(lang_summary.items()):
                    size_str = format_size(stats["size"])
                    print(f"  - {lang}: {stats['projects']} projects, {stats['items']} items, {size_str}")
        
        print("=" * 60)
        print(f"Report ID: {report.id}")
        print()


#!/usr/bin/env python3
"""
Code Collection Script for Fine-Tuning Dataset Preparation

Collects and processes source code from specified repositories,
filtering out sensitive files, binaries, and generated code.

Usage:
    python collect_code.py --repos /path/to/repo1 /path/to/repo2 --output ../data/raw/
    python collect_code.py --config repos.yaml --output ../data/raw/
"""

import argparse
import hashlib
import json
import os
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class CollectionConfig:
    """Configuration for code collection."""

    # File extensions to include
    include_extensions: list[str] = field(default_factory=lambda: [
        # JavaScript/TypeScript
        '.js', '.jsx', '.ts', '.tsx', '.mjs', '.cjs',
        # Python
        '.py', '.pyi',
        # Config files (selective)
        '.json', '.yaml', '.yml',
    ])

    # Directories to always exclude
    exclude_dirs: list[str] = field(default_factory=lambda: [
        'node_modules',
        '.git',
        '.svn',
        'dist',
        'build',
        'coverage',
        '__pycache__',
        '.pytest_cache',
        '.mypy_cache',
        '.next',
        '.nuxt',
        'vendor',
        'venv',
        '.venv',
        'env',
        '.env',
        'target',
        'out',
        '.idea',
        '.vscode',
    ])

    # File patterns to exclude (regex)
    exclude_patterns: list[str] = field(default_factory=lambda: [
        r'\.min\.js$',           # Minified JS
        r'\.min\.css$',          # Minified CSS
        r'\.bundle\.js$',        # Bundled files
        r'\.map$',               # Source maps
        r'\.lock$',              # Lock files
        r'package-lock\.json$',  # NPM lock
        r'yarn\.lock$',          # Yarn lock
        r'\.d\.ts$',             # TypeScript declarations (optional)
        r'__snapshots__',        # Jest snapshots
        r'\.test\.',             # Test files (optional - may want to include)
        r'\.spec\.',             # Spec files
    ])

    # Sensitive file patterns to ALWAYS exclude
    sensitive_patterns: list[str] = field(default_factory=lambda: [
        r'\.env',
        r'credentials',
        r'secrets?\.',
        r'\.pem$',
        r'\.key$',
        r'\.crt$',
        r'password',
        r'api[_-]?key',
        r'private[_-]?key',
    ])

    # Max file size in bytes (skip large files)
    max_file_size: int = 100_000  # 100KB

    # Min file size in bytes (skip trivial files)
    min_file_size: int = 50  # 50 bytes

    # Max lines per file
    max_lines: int = 2000


@dataclass
class CollectedFile:
    """Represents a collected source file."""
    path: str
    relative_path: str
    repo: str
    language: str
    content: str
    size: int
    lines: int
    hash: str
    collected_at: str


class CodeCollector:
    """Collects source code from repositories."""

    def __init__(self, config: Optional[CollectionConfig] = None):
        self.config = config or CollectionConfig()
        self.stats = {
            'total_files': 0,
            'collected_files': 0,
            'skipped_files': 0,
            'total_lines': 0,
            'by_language': {},
            'by_repo': {},
            'skip_reasons': {}
        }
        self._compiled_patterns = None
        self._compiled_sensitive = None

    @property
    def exclude_patterns(self):
        if self._compiled_patterns is None:
            self._compiled_patterns = [
                re.compile(p, re.IGNORECASE)
                for p in self.config.exclude_patterns
            ]
        return self._compiled_patterns

    @property
    def sensitive_patterns(self):
        if self._compiled_sensitive is None:
            self._compiled_sensitive = [
                re.compile(p, re.IGNORECASE)
                for p in self.config.sensitive_patterns
            ]
        return self._compiled_sensitive

    def _record_skip(self, reason: str):
        """Record why a file was skipped."""
        self.stats['skipped_files'] += 1
        self.stats['skip_reasons'][reason] = self.stats['skip_reasons'].get(reason, 0) + 1

    def _get_language(self, filepath: str) -> str:
        """Determine programming language from file extension."""
        ext_map = {
            '.js': 'javascript',
            '.jsx': 'javascript',
            '.mjs': 'javascript',
            '.cjs': 'javascript',
            '.ts': 'typescript',
            '.tsx': 'typescript',
            '.py': 'python',
            '.pyi': 'python',
            '.json': 'json',
            '.yaml': 'yaml',
            '.yml': 'yaml',
        }
        ext = Path(filepath).suffix.lower()
        return ext_map.get(ext, 'unknown')

    def _should_exclude_dir(self, dirpath: str) -> bool:
        """Check if directory should be excluded."""
        dir_name = os.path.basename(dirpath)
        return dir_name in self.config.exclude_dirs

    def _should_exclude_file(self, filepath: str) -> tuple[bool, str]:
        """Check if file should be excluded. Returns (should_exclude, reason)."""
        filename = os.path.basename(filepath)

        # Check extension
        ext = Path(filepath).suffix.lower()
        if ext not in self.config.include_extensions:
            return True, 'extension_not_included'

        # Check sensitive patterns
        for pattern in self.sensitive_patterns:
            if pattern.search(filepath):
                return True, 'sensitive_file'

        # Check exclude patterns
        for pattern in self.exclude_patterns:
            if pattern.search(filepath):
                return True, 'pattern_excluded'

        return False, ''

    def _is_binary(self, content: bytes) -> bool:
        """Check if content appears to be binary."""
        # Check for null bytes (common in binary files)
        if b'\x00' in content[:1024]:
            return True
        return False

    def _contains_secrets(self, content: str) -> bool:
        """Check if content might contain secrets (basic check)."""
        secret_indicators = [
            r'api[_-]?key\s*[=:]\s*["\'][^"\']{20,}',
            r'password\s*[=:]\s*["\'][^"\']+',
            r'secret\s*[=:]\s*["\'][^"\']{10,}',
            r'token\s*[=:]\s*["\'][^"\']{20,}',
            r'-----BEGIN (RSA |EC |DSA )?PRIVATE KEY-----',
        ]
        for pattern in secret_indicators:
            if re.search(pattern, content, re.IGNORECASE):
                return True
        return False

    def collect_file(self, filepath: str, repo_root: str, repo_name: str) -> Optional[CollectedFile]:
        """Collect a single file if it passes all filters."""
        self.stats['total_files'] += 1

        # Check file exclusion
        should_exclude, reason = self._should_exclude_file(filepath)
        if should_exclude:
            self._record_skip(reason)
            return None

        # Check file size
        try:
            file_size = os.path.getsize(filepath)
        except OSError:
            self._record_skip('cannot_read')
            return None

        if file_size > self.config.max_file_size:
            self._record_skip('too_large')
            return None

        if file_size < self.config.min_file_size:
            self._record_skip('too_small')
            return None

        # Read file content
        try:
            with open(filepath, 'rb') as f:
                raw_content = f.read()
        except (OSError, IOError):
            self._record_skip('read_error')
            return None

        # Check for binary
        if self._is_binary(raw_content):
            self._record_skip('binary_file')
            return None

        # Decode content
        try:
            content = raw_content.decode('utf-8')
        except UnicodeDecodeError:
            self._record_skip('encoding_error')
            return None

        # Check line count
        lines = content.count('\n') + 1
        if lines > self.config.max_lines:
            self._record_skip('too_many_lines')
            return None

        # Check for secrets in content
        if self._contains_secrets(content):
            self._record_skip('contains_secrets')
            return None

        # Calculate relative path and hash
        relative_path = os.path.relpath(filepath, repo_root)
        content_hash = hashlib.sha256(raw_content).hexdigest()[:16]
        language = self._get_language(filepath)

        # Update stats
        self.stats['collected_files'] += 1
        self.stats['total_lines'] += lines
        self.stats['by_language'][language] = self.stats['by_language'].get(language, 0) + 1
        self.stats['by_repo'][repo_name] = self.stats['by_repo'].get(repo_name, 0) + 1

        return CollectedFile(
            path=filepath,
            relative_path=relative_path,
            repo=repo_name,
            language=language,
            content=content,
            size=file_size,
            lines=lines,
            hash=content_hash,
            collected_at=datetime.now().isoformat()
        )

    def collect_repo(self, repo_path: str, repo_name: Optional[str] = None) -> list[CollectedFile]:
        """Collect all eligible files from a repository."""
        repo_path = os.path.abspath(repo_path)

        if not os.path.isdir(repo_path):
            raise ValueError(f"Repository path does not exist: {repo_path}")

        if repo_name is None:
            repo_name = os.path.basename(repo_path)

        collected = []

        for root, dirs, files in os.walk(repo_path):
            # Filter out excluded directories (modifies dirs in-place)
            dirs[:] = [d for d in dirs if not self._should_exclude_dir(os.path.join(root, d))]

            for filename in files:
                filepath = os.path.join(root, filename)
                file_data = self.collect_file(filepath, repo_path, repo_name)
                if file_data:
                    collected.append(file_data)

        return collected

    def collect_repos(self, repo_paths: list[str]) -> list[CollectedFile]:
        """Collect files from multiple repositories."""
        all_collected = []

        for repo_path in repo_paths:
            print(f"Collecting from: {repo_path}")
            collected = self.collect_repo(repo_path)
            all_collected.extend(collected)
            print(f"  Collected {len(collected)} files")

        return all_collected

    def save_collected(self, collected: list[CollectedFile], output_dir: str):
        """Save collected files to output directory."""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Save as JSON for easy processing
        data = {
            'metadata': {
                'collected_at': datetime.now().isoformat(),
                'stats': self.stats
            },
            'files': [
                {
                    'relative_path': f.relative_path,
                    'repo': f.repo,
                    'language': f.language,
                    'content': f.content,
                    'size': f.size,
                    'lines': f.lines,
                    'hash': f.hash
                }
                for f in collected
            ]
        }

        output_file = output_path / 'collected_code.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"\nSaved {len(collected)} files to {output_file}")

        # Also save a manifest for quick reference
        manifest = {
            'collected_at': datetime.now().isoformat(),
            'stats': self.stats,
            'files': [
                {
                    'path': f.relative_path,
                    'repo': f.repo,
                    'language': f.language,
                    'lines': f.lines
                }
                for f in collected
            ]
        }

        manifest_file = output_path / 'manifest.json'
        with open(manifest_file, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2)

        print(f"Saved manifest to {manifest_file}")

    def print_stats(self):
        """Print collection statistics."""
        print("\n" + "=" * 50)
        print("COLLECTION STATISTICS")
        print("=" * 50)
        print(f"Total files scanned: {self.stats['total_files']}")
        print(f"Files collected: {self.stats['collected_files']}")
        print(f"Files skipped: {self.stats['skipped_files']}")
        print(f"Total lines: {self.stats['total_lines']:,}")

        print("\nBy Language:")
        for lang, count in sorted(self.stats['by_language'].items(), key=lambda x: -x[1]):
            print(f"  {lang}: {count}")

        print("\nBy Repository:")
        for repo, count in sorted(self.stats['by_repo'].items(), key=lambda x: -x[1]):
            print(f"  {repo}: {count}")

        print("\nSkip Reasons:")
        for reason, count in sorted(self.stats['skip_reasons'].items(), key=lambda x: -x[1]):
            print(f"  {reason}: {count}")


def main():
    parser = argparse.ArgumentParser(
        description='Collect source code from repositories for fine-tuning'
    )
    parser.add_argument(
        '--repos',
        nargs='+',
        help='Paths to repositories to collect from'
    )
    parser.add_argument(
        '--output',
        default='../data/raw/',
        help='Output directory for collected code'
    )
    parser.add_argument(
        '--include-tests',
        action='store_true',
        help='Include test files (excluded by default)'
    )
    parser.add_argument(
        '--max-size',
        type=int,
        default=100_000,
        help='Maximum file size in bytes (default: 100KB)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be collected without saving'
    )

    args = parser.parse_args()

    if not args.repos:
        print("Error: No repositories specified. Use --repos /path/to/repo1 /path/to/repo2")
        print("\nExample usage:")
        print("  python collect_code.py --repos ~/projects/my-app --output ../data/raw/")
        return 1

    # Configure collection
    config = CollectionConfig(max_file_size=args.max_size)

    if args.include_tests:
        # Remove test file patterns from exclusion
        config.exclude_patterns = [
            p for p in config.exclude_patterns
            if 'test' not in p and 'spec' not in p
        ]

    # Collect code
    collector = CodeCollector(config)
    collected = collector.collect_repos(args.repos)

    # Print stats
    collector.print_stats()

    # Save results
    if not args.dry_run:
        collector.save_collected(collected, args.output)
    else:
        print("\n[DRY RUN] No files saved")

    return 0


if __name__ == '__main__':
    exit(main())

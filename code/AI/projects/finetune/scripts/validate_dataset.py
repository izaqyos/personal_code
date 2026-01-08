#!/usr/bin/env python3
"""
Dataset Validation Script

Validates training datasets for format, quality, and consistency.
Run this before training to catch issues early.

Usage:
    python validate_dataset.py --input ../data/training/cursor_generated.json
    python validate_dataset.py --input ../data/training/ --all
"""

import argparse
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path


class DatasetValidator:
    """Validates training datasets for LLM fine-tuning."""

    REQUIRED_FIELDS = ["instruction", "output"]
    OPTIONAL_FIELDS = ["id", "input", "category", "language", "source", "quality", "metadata"]
    VALID_CATEGORIES = [
        "code_review", "explain_code", "suggest_improvements",
        "debugging", "architecture", "best_practices", "testing", "other"
    ]
    VALID_LANGUAGES = ["javascript", "python", "typescript", "go", "rust", "unknown"]

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.errors = []
        self.warnings = []
        self.stats = Counter()

    def _log_error(self, msg: str):
        self.errors.append(msg)
        self.stats["errors"] += 1

    def _log_warning(self, msg: str):
        self.warnings.append(msg)
        self.stats["warnings"] += 1

    def validate_example(self, example: dict, index: int) -> bool:
        """Validate a single training example."""
        example_id = example.get("id", f"index_{index}")
        valid = True

        # Check required fields
        for field in self.REQUIRED_FIELDS:
            if field not in example or not example[field]:
                self._log_error(f"[{example_id}] Missing required field: {field}")
                valid = False

        # Check instruction length
        instruction = example.get("instruction", "")
        if len(instruction) < 10:
            self._log_error(f"[{example_id}] Instruction too short ({len(instruction)} chars)")
            valid = False
        elif len(instruction) > 500:
            self._log_warning(f"[{example_id}] Instruction very long ({len(instruction)} chars)")

        # Check output length
        output = example.get("output", "")
        if len(output) < 50:
            self._log_warning(f"[{example_id}] Output short ({len(output)} chars) - may be low quality")
        elif len(output) > 5000:
            self._log_warning(f"[{example_id}] Output very long ({len(output)} chars) - may cause issues")

        # Check category if present
        category = example.get("category")
        if category and category not in self.VALID_CATEGORIES:
            self._log_warning(f"[{example_id}] Unknown category: {category}")

        # Check language if present
        language = example.get("language")
        if language and language.lower() not in self.VALID_LANGUAGES:
            self._log_warning(f"[{example_id}] Unknown language: {language}")

        # Check for potential sensitive data
        combined_text = f"{instruction} {example.get('input', '')} {output}"
        if self._contains_sensitive_data(combined_text):
            self._log_error(f"[{example_id}] May contain sensitive data (API key, password, etc.)")
            valid = False

        # Track stats
        if category:
            self.stats[f"category_{category}"] += 1
        if language:
            self.stats[f"language_{language.lower()}"] += 1
        self.stats["total_examples"] += 1

        return valid

    def _contains_sensitive_data(self, text: str) -> bool:
        """Check for potential sensitive data patterns."""
        patterns = [
            r'["\']?api[_-]?key["\']?\s*[:=]\s*["\'][^"\']{20,}',
            r'["\']?password["\']?\s*[:=]\s*["\'][^"\']+',
            r'["\']?secret["\']?\s*[:=]\s*["\'][^"\']{10,}',
            r'["\']?token["\']?\s*[:=]\s*["\'][^"\']{20,}',
            r'-----BEGIN (RSA |EC |DSA )?PRIVATE KEY-----',
            r'sk-[a-zA-Z0-9]{20,}',  # OpenAI API key pattern
            r'ghp_[a-zA-Z0-9]{36}',   # GitHub token pattern
        ]

        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False

    def validate_file(self, filepath: str) -> bool:
        """Validate a single dataset file."""
        print(f"\nValidating: {filepath}")

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            self._log_error(f"Invalid JSON: {e}")
            return False
        except Exception as e:
            self._log_error(f"Cannot read file: {e}")
            return False

        # Handle different formats
        if isinstance(data, list):
            examples = data
        elif isinstance(data, dict):
            if "data" in data:
                examples = data["data"]
            else:
                examples = [data]
        else:
            self._log_error("Unknown data format - expected list or object with 'data' key")
            return False

        # Validate each example
        all_valid = True
        seen_ids = set()

        for i, example in enumerate(examples):
            if not self.validate_example(example, i):
                all_valid = False

            # Check for duplicate IDs
            example_id = example.get("id")
            if example_id:
                if example_id in seen_ids:
                    self._log_warning(f"Duplicate ID: {example_id}")
                seen_ids.add(example_id)

        return all_valid

    def validate_directory(self, dirpath: str) -> bool:
        """Validate all JSON files in a directory."""
        json_files = list(Path(dirpath).glob("*.json"))

        if not json_files:
            print(f"No JSON files found in {dirpath}")
            return True

        all_valid = True
        for filepath in json_files:
            if not self.validate_file(str(filepath)):
                all_valid = False

        return all_valid

    def print_report(self):
        """Print validation report."""
        print("\n" + "=" * 60)
        print("VALIDATION REPORT")
        print("=" * 60)

        print(f"\nTotal examples: {self.stats.get('total_examples', 0)}")

        # Print category distribution
        categories = {k: v for k, v in self.stats.items() if k.startswith("category_")}
        if categories:
            print("\nCategory Distribution:")
            for cat, count in sorted(categories.items()):
                cat_name = cat.replace("category_", "")
                pct = (count / self.stats["total_examples"]) * 100
                print(f"  {cat_name}: {count} ({pct:.1f}%)")

        # Print language distribution
        languages = {k: v for k, v in self.stats.items() if k.startswith("language_")}
        if languages:
            print("\nLanguage Distribution:")
            for lang, count in sorted(languages.items()):
                lang_name = lang.replace("language_", "")
                pct = (count / self.stats["total_examples"]) * 100
                print(f"  {lang_name}: {count} ({pct:.1f}%)")

        # Print errors
        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for error in self.errors[:20]:
                print(f"  - {error}")
            if len(self.errors) > 20:
                print(f"  ... and {len(self.errors) - 20} more errors")
        else:
            print("\n✅ No errors found!")

        # Print warnings
        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings[:10]:
                print(f"  - {warning}")
            if len(self.warnings) > 10:
                print(f"  ... and {len(self.warnings) - 10} more warnings")

        # Summary
        print("\n" + "-" * 60)
        if self.errors:
            print("❌ Validation FAILED - fix errors before training")
            return False
        elif self.warnings:
            print("⚠️  Validation PASSED with warnings - review before training")
            return True
        else:
            print("✅ Validation PASSED - dataset ready for training!")
            return True


def main():
    parser = argparse.ArgumentParser(description="Validate training datasets")
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Input file or directory to validate"
    )
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="Validate all JSON files in directory"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )

    args = parser.parse_args()

    validator = DatasetValidator(verbose=args.verbose)

    input_path = args.input
    if os.path.isdir(input_path):
        validator.validate_directory(input_path)
    else:
        validator.validate_file(input_path)

    success = validator.print_report()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())

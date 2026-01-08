#!/usr/bin/env python3
"""
Compile Cursor-Generated Training Data

Combines multiple JSON files into a single training dataset.
Use this if you save examples to separate files during generation.

Usage:
    python compile_cursor_data.py --input ../data/cursor_raw/ --output ../data/training/cursor_generated.json
    python compile_cursor_data.py --input file1.json file2.json --output combined.json
"""

import argparse
import glob
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Union


def load_json_file(filepath: str) -> list[dict]:
    """Load examples from a JSON file, handling various formats."""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Handle different formats
    if isinstance(data, list):
        return data
    elif isinstance(data, dict):
        if "data" in data:
            return data["data"]
        else:
            # Single example
            return [data]
    else:
        print(f"Warning: Unknown format in {filepath}, skipping")
        return []


def compile_dataset(
    input_paths: list[str],
    output_path: str,
    dedupe: bool = True
) -> dict:
    """Compile multiple JSON files into a single dataset."""

    all_examples = []
    source_files = []

    for path in input_paths:
        if os.path.isdir(path):
            # Find all JSON files in directory
            json_files = glob.glob(os.path.join(path, "*.json"))
            json_files.extend(glob.glob(os.path.join(path, "**/*.json"), recursive=True))
        else:
            json_files = [path]

        for filepath in json_files:
            if not os.path.exists(filepath):
                print(f"Warning: File not found: {filepath}")
                continue

            try:
                examples = load_json_file(filepath)
                all_examples.extend(examples)
                source_files.append(filepath)
                print(f"Loaded {len(examples)} examples from {filepath}")
            except json.JSONDecodeError as e:
                print(f"Warning: Invalid JSON in {filepath}: {e}")
            except Exception as e:
                print(f"Warning: Error reading {filepath}: {e}")

    # Deduplicate by ID if requested
    if dedupe:
        seen_ids = set()
        unique_examples = []
        duplicates = 0

        for example in all_examples:
            example_id = example.get("id")
            if example_id:
                if example_id in seen_ids:
                    duplicates += 1
                    continue
                seen_ids.add(example_id)
            unique_examples.append(example)

        if duplicates > 0:
            print(f"Removed {duplicates} duplicate examples")
        all_examples = unique_examples

    # Assign IDs to examples without them
    for i, example in enumerate(all_examples):
        if "id" not in example:
            example["id"] = f"example_{i:04d}"

    # Count categories
    categories = {}
    languages = {}
    for example in all_examples:
        cat = example.get("category", "unknown")
        lang = example.get("language", "unknown")
        categories[cat] = categories.get(cat, 0) + 1
        languages[lang] = languages.get(lang, 0) + 1

    # Create final dataset
    dataset = {
        "version": "1.0.0",
        "metadata": {
            "created_at": datetime.now().isoformat(),
            "source": "cursor",
            "total_examples": len(all_examples),
            "source_files": source_files,
            "categories": categories,
            "languages": languages
        },
        "data": all_examples
    }

    # Save
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

    return dataset


def print_summary(dataset: dict):
    """Print compilation summary."""
    metadata = dataset.get("metadata", {})

    print("\n" + "=" * 50)
    print("COMPILATION SUMMARY")
    print("=" * 50)
    print(f"Total examples: {metadata.get('total_examples', 0)}")

    categories = metadata.get("categories", {})
    if categories:
        print("\nBy Category:")
        for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
            print(f"  {cat}: {count}")

    languages = metadata.get("languages", {})
    if languages:
        print("\nBy Language:")
        for lang, count in sorted(languages.items(), key=lambda x: -x[1]):
            print(f"  {lang}: {count}")

    print("\n✅ Dataset compiled successfully!")


def main():
    parser = argparse.ArgumentParser(
        description="Compile Cursor-generated training data"
    )
    parser.add_argument(
        "--input", "-i",
        nargs="+",
        required=True,
        help="Input files or directories"
    )
    parser.add_argument(
        "--output", "-o",
        default="../data/training/cursor_generated.json",
        help="Output file path"
    )
    parser.add_argument(
        "--no-dedupe",
        action="store_true",
        help="Don't remove duplicate examples"
    )

    args = parser.parse_args()

    dataset = compile_dataset(
        input_paths=args.input,
        output_path=args.output,
        dedupe=not args.no_dedupe
    )

    print_summary(dataset)
    print(f"\nSaved to: {args.output}")

    return 0


if __name__ == "__main__":
    sys.exit(main())

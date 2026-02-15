"""
Emoji Registry -- loads emoji entries from YAML.

Each entry in emojis.yaml becomes an EmojiEntry dataclass.
The 'searchable_text' field concatenates description + aliases,
which is what the TF-IDF engine vectorizes for matching.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import List

import yaml


@dataclass
class EmojiEntry:
    """A single emoji mapping: emoji combo + metadata for search."""

    emoji: str
    name: str
    description: str
    aliases: List[str] = field(default_factory=list)

    @property
    def searchable_text(self) -> str:
        """Combine description and aliases into one searchable string.

        This is what gets fed into the TF-IDF vectorizer.
        More text = more vocabulary for the engine to match against.
        """
        parts = [self.description] + self.aliases
        return " . ".join(parts)


def get_default_yaml_path() -> Path:
    """Return the path to the bundled emojis.yaml."""
    return Path(__file__).parent / "data" / "emojis.yaml"


def load_registry(yaml_path: Path | None = None) -> List[EmojiEntry]:
    """Load emoji entries from a YAML file.

    Args:
        yaml_path: Path to the YAML file. Defaults to the bundled emojis.yaml.

    Returns:
        List of EmojiEntry objects, ready for the matching engine.
    """
    if yaml_path is None:
        yaml_path = get_default_yaml_path()

    with open(yaml_path, "r", encoding="utf-8") as f:
        raw_entries = yaml.safe_load(f)

    if not raw_entries:
        return []

    entries = []
    for item in raw_entries:
        entry = EmojiEntry(
            emoji=item["emoji"],
            name=item["name"],
            description=item["description"],
            aliases=item.get("aliases", []),
        )
        entries.append(entry)

    return entries


def generate_yaml_snippet(query: str) -> str:
    """Generate a ready-to-paste YAML snippet for a new emoji entry.

    Used by the 'no match' flow so the user can easily add missing entries.

    Args:
        query: The user's original query text.

    Returns:
        A YAML string snippet that can be appended to emojis.yaml.
    """
    # Convert query to a snake_case name
    safe_name = query.lower().strip()
    safe_name = safe_name.replace(" ", "_")
    safe_name = "".join(c for c in safe_name if c.isalnum() or c == "_")

    snippet = f"""
- emoji: "PUT_EMOJI_HERE"
  name: "{safe_name}"
  description: "{query.lower().strip()}"
  aliases:
    - "{query.lower().strip()}"
"""
    return snippet


def append_entry_to_yaml(yaml_path: Path, emoji: str, query: str) -> None:
    """Append a new emoji entry to the YAML file.

    Used by the REPL's [a]dd feature for hot-adding entries.

    Args:
        yaml_path: Path to the emojis.yaml file.
        emoji: The emoji string to use.
        query: The description/query text.
    """
    safe_name = query.lower().strip().replace(" ", "_")
    safe_name = "".join(c for c in safe_name if c.isalnum() or c == "_")

    new_entry = f"""
- emoji: "{emoji}"
  name: "{safe_name}"
  description: "{query.lower().strip()}"
  aliases:
    - "{query.lower().strip()}"
"""
    with open(yaml_path, "a", encoding="utf-8") as f:
        f.write(new_entry)

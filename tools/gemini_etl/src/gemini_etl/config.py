"""Configuration constants and Source records."""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Source:
    name: str
    path: str
    extensions: frozenset[str]


@dataclass(frozen=True)
class Config:
    sources: tuple[Source, ...]
    store_name: str
    chunk_token_limit: int
    max_file_size_bytes: int
    max_concurrency: int
    state_dir: Path

    @property
    def manifest_path(self) -> Path:
        return self.state_dir / "sync_manifest.sqlite"

    @property
    def store_id_path(self) -> Path:
        return self.state_dir / "store.txt"


_DEFAULT_SOURCES = (
    Source(
        name="personal_KB",
        path="/Users/yosii/work/git/personal_KB",
        extensions=frozenset({".md"}),
    ),
    Source(
        name="personal_code",
        path="/Users/yosii/work/git/personal_code",
        extensions=frozenset({".py", ".js", ".ts", ".c", ".cpp", ".h", ".bash"}),
    ),
)


def get_config() -> Config:
    """Build the runtime config, applying env-var overrides."""
    state_dir = Path(
        os.environ.get("GEMINI_ETL_STATE_DIR", "~/.gemini_etl")
    ).expanduser()
    return Config(
        sources=_DEFAULT_SOURCES,
        store_name=os.environ.get("GEMINI_ETL_STORE_NAME", "yosi-personal-kb"),
        chunk_token_limit=int(os.environ.get("GEMINI_ETL_CHUNK_TOKEN_LIMIT", 10_000)),
        max_file_size_bytes=int(os.environ.get("GEMINI_ETL_MAX_FILE_SIZE", 2 * 1024**3)),
        max_concurrency=int(os.environ.get("GEMINI_ETL_MAX_CONCURRENCY", 4)),
        state_dir=state_dir,
    )

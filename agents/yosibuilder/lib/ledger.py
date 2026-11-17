"""Results and pricing ledger: one row per card build, rolling stats per crew, and reports."""

from __future__ import annotations

import json
import os
from collections import defaultdict
from datetime import datetime
from pathlib import Path

LEDGER = Path(os.environ.get("YB_LEDGER", str(Path.home() / ".local/share/yosibuilder/ledger.jsonl")))
PRICES = Path(__file__).resolve().parent.parent / "config" / "prices.json"
ALERT_ACCEPT = float(os.environ.get("YB_ALERT_ACCEPT", "0.8"))
WINDOW = int(os.environ.get("YB_WINDOW", "20"))
INPUT_KEYS = ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens")


def load_prices() -> dict:
    return json.loads(PRICES.read_text())


def row_usd(row: dict, prices: dict) -> float:
    """Dollar cost of one usage row: Claude's own figure, an estimate for other providers, zero for local."""
    provider = row.get("provider", "local")
    if provider == "claude":
        return float(row["cost_usd"])
    if provider == "local":
        return 0.0
    rate = prices["models"].get(row.get("model", ""), prices["unpriced"])
    tokens_in = sum(row.get(key, 0) for key in INPUT_KEYS)
    return (tokens_in * rate["input"] + row.get("output_tokens", 0) * rate["output"]) / 1e6


def cost_summary(rows: list[dict], prices: dict) -> dict:
    """Per-provider dollars and tokens for a set of usage rows, plus the priority-weighted total."""
    usd: dict[str, float] = defaultdict(float)
    tokens: dict[str, int] = defaultdict(int)
    for row in rows:
        provider = row.get("provider", "local")
        usd[provider] += row_usd(row, prices)
        tokens[provider] += sum(row.get(key, 0) for key in (*INPUT_KEYS, "output_tokens"))
    weighted = sum(value * prices["weights"].get(provider, 1.0) for provider, value in usd.items())
    return {"usd": {k: round(v, 4) for k, v in usd.items()}, "tokens": dict(tokens), "weighted_usd": round(weighted, 4)}


def append(entry: dict) -> None:
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER.open("a") as f:
        f.write(json.dumps({"ts": datetime.now().isoformat(timespec="seconds"), **entry}) + "\n")


def entries() -> list[dict]:
    return [json.loads(line) for line in LEDGER.read_text().splitlines()] if LEDGER.exists() else []


def crew_stats(rows: list[dict]) -> dict:
    """Acceptance and cost figures for ledger entries of one crew."""
    done = [e for e in rows if e["status"] == "done"]
    n = len(rows)
    return {
        "cards": n,
        "accepted": round(len(done) / n, 2) if n else 0.0,
        "first_review": round(sum(e["reviews"] == 1 for e in done) / n, 2) if n else 0.0,
        "claude_usd_per_card": round(sum(e["cost"]["usd"].get("claude", 0) for e in rows) / n, 4) if n else 0.0,
        "weighted_usd_per_card": round(sum(e["cost"]["weighted_usd"] for e in rows) / n, 4) if n else 0.0,
        "weighted_usd_per_accepted": round(sum(e["cost"]["weighted_usd"] for e in rows) / len(done), 4)
        if done else None,
    }


def rolling(crew: str, window: int = WINDOW) -> dict:
    return crew_stats([e for e in entries() if e["crew"] == crew][-window:])


def alert(crew: str, stats: dict) -> str | None:
    if stats["cards"] >= 5 and stats["accepted"] < ALERT_ACCEPT:
        return (f"crew '{crew}' accepted {stats['accepted']:.0%} of its last {stats['cards']} cards, below "
                f"{ALERT_ACCEPT:.0%}: sharpen the cards or switch crew (yb report shows the alternatives)")
    return None


def report(last: int | None = None) -> dict:
    by_crew: dict[str, list[dict]] = defaultdict(list)
    for entry in entries():
        by_crew[entry["crew"]].append(entry)
    return {crew: crew_stats(rows[-last:] if last else rows) for crew, rows in by_crew.items()}

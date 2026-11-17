"""Results and pricing ledger: one row per card build, priced at report time, with rolling stats per crew."""

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


def load_prices() -> dict:
    return json.loads(PRICES.read_text())


def model_breakdown(rows: list[dict]) -> dict:
    """Tokens per model (fresh input, cached input, output) and Claude's own dollar figure, from usage rows."""
    models: dict[str, dict] = defaultdict(lambda: {"provider": "local", "fresh": 0, "cached": 0, "output": 0,
                                                   "claude_usd": 0.0})
    for row in rows:
        entry = models[row.get("model", "unknown")]
        entry["provider"] = row.get("provider", "local")
        entry["fresh"] += row.get("input_tokens", 0) + row.get("cache_creation_input_tokens", 0)
        entry["cached"] += row.get("cache_read_input_tokens", 0)
        entry["output"] += row.get("output_tokens", 0)
        entry["claude_usd"] += row.get("cost_usd", 0.0)
    return dict(models)


def model_usd(model: str, usage: dict, prices: dict) -> float:
    """Dollars for one model's usage: Claude's own figure, list-price estimate for others, zero for local."""
    if usage["provider"] == "claude":
        return usage["claude_usd"]
    if usage["provider"] == "local":
        return 0.0
    rate = prices["models"].get(model, prices["unpriced"])
    return (usage["fresh"] * rate["input"] + usage["cached"] * rate.get("cached_input", rate["input"])
            + usage["output"] * rate["output"]) / 1e6


def price(models: dict, prices: dict) -> dict:
    """Per-provider dollars and tokens, and the priority-weighted total, at today's prices."""
    usd: dict[str, float] = defaultdict(float)
    tokens: dict[str, int] = defaultdict(int)
    for model, usage in models.items():
        usd[usage["provider"]] += model_usd(model, usage, prices)
        tokens[usage["provider"]] += usage["fresh"] + usage["cached"] + usage["output"]
    weighted = sum(value * prices["weights"].get(provider, 1.0) for provider, value in usd.items())
    return {"usd": {k: round(v, 4) for k, v in usd.items()}, "tokens": dict(tokens), "weighted_usd": round(weighted, 4)}


def append(entry: dict) -> None:
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER.open("a") as f:
        f.write(json.dumps({"ts": datetime.now().isoformat(timespec="seconds"), **entry}) + "\n")


def entries() -> list[dict]:
    return [json.loads(line) for line in LEDGER.read_text().splitlines()] if LEDGER.exists() else []


def crew_stats(rows: list[dict], prices: dict) -> dict:
    """Acceptance and cost figures for ledger entries of one crew, priced with today's prices."""
    n = len(rows)
    if not n:
        return {"cards": 0}
    done = [e for e in rows if e["status"] == "done"]
    costs = [price(e["models"], prices) for e in rows]
    weighted = sum(c["weighted_usd"] for c in costs)
    return {
        "cards": n,
        "accepted": round(len(done) / n, 2),
        "first_review": round(sum(e["reviews"] == 1 for e in done) / n, 2),
        "claude_usd_per_card": round(sum(c["usd"].get("claude", 0) for c in costs) / n, 4),
        "gemini_usd_per_card": round(sum(c["usd"].get("agy", 0) for c in costs) / n, 4),
        "weighted_usd_per_card": round(weighted / n, 4),
        "weighted_usd_per_accepted": round(weighted / len(done), 4) if done else None,
    }


def rolling(crew: str, window: int = WINDOW) -> dict:
    return crew_stats([e for e in entries() if e["crew"] == crew][-window:], load_prices())


def alert(crew: str, stats: dict) -> str | None:
    if stats["cards"] >= 5 and stats["accepted"] < ALERT_ACCEPT:
        return (f"crew '{crew}' accepted {stats['accepted']:.0%} of its last {stats['cards']} cards, below "
                f"{ALERT_ACCEPT:.0%}: sharpen the cards or switch crew (yb report shows the alternatives)")
    return None


def report(last: int | None = None) -> dict:
    by_crew: dict[str, list[dict]] = defaultdict(list)
    for entry in entries():
        by_crew[entry["crew"]].append(entry)
    prices = load_prices()
    return {crew: crew_stats(rows[-last:] if last else rows, prices) for crew, rows in by_crew.items()}

#!/usr/bin/env python3
"""Claude Code status line: model · dir · context used · cost · duration · lines changed · plan limits.

Reads the status-line JSON from stdin. Every field is optional; missing ones are skipped.
The last input is saved to ~/.claude/statusline-last-input.json for debugging.
"""
import json
import os
import sys
import time

DIM, RESET = "\033[2m", "\033[0m"
GREEN, YELLOW, RED = "\033[32m", "\033[33m", "\033[31m"


def color_pct(p):
    c = GREEN if p < 50 else YELLOW if p < 80 else RED
    return f"{c}{p:.0f}%{RESET}"


def k(n):
    return f"{n / 1_000_000:.1f}M" if n >= 1_000_000 else f"{n / 1000:.0f}k" if n >= 1000 else str(n)


def context_from_transcript(path):
    """Fallback: tokens in context = input + cache tokens of the last main-chain assistant message."""
    try:
        with open(path, "rb") as f:
            f.seek(0, 2)
            f.seek(max(0, f.tell() - 400_000))
            lines = f.read().decode("utf-8", "ignore").splitlines()
    except OSError:
        return None
    for line in reversed(lines):
        try:
            e = json.loads(line)
        except ValueError:
            continue
        if e.get("isSidechain"):
            continue
        u = (e.get("message") or {}).get("usage")
        if e.get("type") == "assistant" and u:
            return u.get("input_tokens", 0) + u.get("cache_read_input_tokens", 0) + u.get("cache_creation_input_tokens", 0)
    return None


def main():
    try:
        d = json.load(sys.stdin)
    except ValueError:
        d = {}
    try:
        with open(os.path.expanduser("~/.claude/statusline-last-input.json"), "w") as f:
            json.dump(d, f, indent=1)
    except OSError:
        pass

    parts = []
    model = (d.get("model") or {}).get("display_name") or (d.get("model") or {}).get("id")
    if model:
        parts.append(model)
    cwd = (d.get("workspace") or {}).get("current_dir") or d.get("cwd")
    if cwd:
        parts.append(os.path.basename(cwd.rstrip("/")) or cwd)

    # Context window
    cw = d.get("context_window") or {}
    size = cw.get("context_window_size") or (1_000_000 if "1m" in str((d.get("model") or {}).get("id", "")).lower() else 200_000)
    used = None
    cu = cw.get("current_usage")
    if isinstance(cu, dict):
        used = cu.get("input_tokens", 0) + cu.get("cache_read_input_tokens", 0) + cu.get("cache_creation_input_tokens", 0)
    if used is None and d.get("transcript_path"):
        used = context_from_transcript(d["transcript_path"])
    pct = cw.get("used_percentage")
    if pct is None and used is not None:
        pct = 100 * used / size
    if pct is not None:
        parts.append(f"ctx {color_pct(pct)}" + (f" {DIM}{k(used)}/{k(size)}{RESET}" if used is not None else ""))

    # Session cost / time / lines
    cost = d.get("cost") or {}
    if cost.get("total_cost_usd") is not None:
        parts.append(f"${cost['total_cost_usd']:.2f}")
    ms = cost.get("total_duration_ms")
    if ms:
        m = int(ms // 60000)
        parts.append(f"{m // 60}h{m % 60:02d}m" if m >= 60 else f"{m}m")
    add, rem = cost.get("total_lines_added"), cost.get("total_lines_removed")
    if add or rem:
        parts.append(f"{GREEN}+{add or 0}{RESET}/{RED}-{rem or 0}{RESET}")

    # Plan usage limits, if the client provides them (shape varies by version)
    # Shown as "5h 15% 3.5/5h": usage, then time elapsed in the window. Usage is coloured by pace
    # (usage % vs elapsed %): green = on or under pace, yellow = ahead of pace, red = will run out early.
    windows = {"five_hour": ("5h", 5 * 3600, "h"), "seven_day": ("wk", 7 * 86400, "d")}
    rl = d.get("rate_limits") or {}
    now = time.time()
    for name, (label, length, unit) in windows.items():
        v = rl.get(name)
        if not isinstance(v, dict) or not isinstance(v.get("used_percentage"), (int, float)):
            continue
        p, s = v["used_percentage"], f"{label} "
        reset = v.get("resets_at")
        if isinstance(reset, (int, float)):
            elapsed = min(length, max(0.0, length - (reset - now)))
            frac = elapsed / length
            c = GREEN if p <= frac * 100 + 5 else YELLOW if p <= frac * 100 * 1.5 + 10 else RED
            step = 3600 if unit == "h" else 86400
            warn = ""
            # Warn when the current rate would hit 100% before the window resets. Ignore the first 10% of
            # the window unless usage is already high (a few early requests aren't a trend).
            if p >= 100:
                warn = f" {RED}⚠ limit reached{RESET}"
            elif p > 0 and (frac >= 0.10 or p >= 30):
                to_full = elapsed * (100 - p) / p        # seconds until 100% at the current rate
                if to_full < length - elapsed:
                    eta = f"{to_full / 60:.0f}m" if to_full < 3600 else f"{to_full / 3600:.1f}h" if to_full < 86400 else f"{to_full / 86400:.1f}d"
                    warn = f" {RED}⚠ out in ~{eta}{RESET}"
            if warn:
                c = RED
            s += f"{c}{p:.0f}%{RESET} {DIM}{elapsed / step:.1f}/{length // step}{unit}{RESET}{warn}"
        else:
            s += color_pct(p)
        parts.append(s)

    print(f" {DIM}·{RESET} ".join(parts))


if __name__ == "__main__":
    main()

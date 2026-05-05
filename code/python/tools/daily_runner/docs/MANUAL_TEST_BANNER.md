# Banner — Manual Smoke Test

**Target time:** ≤ 5 minutes. Run before merging a banner-related change or after touching any of `src/banner/`, `main.py`, `src/core/models.py`, or `code/bash/tools/launcher/launcher.sh`.

## Prereqs

- venv at `code/python/tools/daily_runner/.venv`, deps installed (`pip install -e ".[dev]"`)
- shell: zsh on macOS

> **Note on dates:** the bundled example schedule covers Q1 2026 only. If today's date is past Q1, fields like `dod` / `next_event` may be empty in the EXPECT lines below — that's correct behavior, not a bug. To exercise full output, point at a current `schedules.json` (see Quick start in [README.md](../README.md#standup-banner)).

## Setup (~30s)

```bash
cd /Users/yosii/work/git/personal_code/code/python/tools/daily_runner
source .venv/bin/activate

# Throwaway sandbox so we don't touch your real config
TMP=$(mktemp -d)
cp config/schedules.example.json "$TMP/schedules.json"
python - <<EOF
import json, os
TMP = os.environ["TMP"]
cfg = json.load(open("config.json"))
cfg["banner"] = {
    "enabled": False,
    "schedules_path": f"{TMP}/schedules.json",
    "default_fields": ["sprint", "sprint_week", "champion", "dod", "next_event"],
}
json.dump(cfg, open(f"{TMP}/config.json", "w"), indent=2)
EOF
export TMP   # export for re-use below

CFG=$TMP/config.json
```

## Checks

Each check ends with **EXPECT** lines. If reality matches, ✅. If not, capture stdout and investigate.

> **Note:** the CLI mode enters an interactive timer after the banner. Press **Ctrl+C** to exit each run before moving on.

### 1. Bare `-b` shows the default cadence panel (~30s)

```bash
python main.py --mode cli --config $CFG --team imagine_dragons -b
```

EXPECT (cols ≥ 80):
- A cyan-bordered panel.
- Title contains `Sprint 26.Q1.X · Week N · <weekday>`.
- Body has `Champion: Alice/Bob/...`, `DoD: ...`, and `DR in Nd · ...` or `Prod in Nd · ...`.
- Banner appears **before** any timer prompts.

### 2. `-b "text"` becomes free-text-only (~30s)

```bash
python main.py --mode cli --config $CFG --team imagine_dragons -b "welcome back Muhe"
```

EXPECT:
- Single panel containing only `welcome back Muhe`.
- No `Sprint`, no `Champion`, no `DR`/`Prod` — disambiguator routed to text.

### 3. Explicit fields + text both render (~30s)

```bash
python main.py --mode cli --config $CFG --team imagine_dragons \
  --banner-fields sprint,dod --banner-text "team meeting today"
```

EXPECT:
- Panel with `Sprint`, `DoD`, AND `team meeting today` line.
- No `Champion`, no `next_event` (filtered out).

### 4. `--no-banner` suppresses (~15s)

```bash
python main.py --mode cli --config $CFG --team imagine_dragons -b --no-banner
```

EXPECT:
- No panel. No `Sprint`. Goes straight to standup timer / recovery prompt.

### 5. Unknown field is rejected at parse time (~15s)

```bash
python main.py --mode cli --config $CFG --team imagine_dragons --banner-fields sprint,bogus
```

EXPECT:
- `argparse` error: `unknown banner field(s): bogus. Known: champion, dod, next_event, sprint, sprint_week`
- Exit code **non-zero**, no banner printed.

### 6. Missing-schedule error banner (~30s)

```bash
BAD=$(mktemp -d)/config.json
python - <<EOF
import json, os
BAD = os.environ.get("BAD", "${BAD}")
json.dump({"version": "1.0", "banner": {"enabled": False, "schedules_path": "/no/such/file.json", "default_fields": ["sprint"]}}, open("${BAD}", "w"))
EOF
python main.py --mode cli --config $BAD --team imagine_dragons -b
```

EXPECT:
- Yellow-bordered panel titled `⚠ Banner unavailable`.
- Headline `schedules.json not found at:`
- Body shows `/no/such/file.json` and the 3-step Fix instructions including `--no-banner`.
- Standup proceeds (does not abort).

### 7. Malformed-schedule path uses different headline (~30s)

```bash
BROKEN=$(mktemp -d)
echo "not valid json" > $BROKEN/schedules.json
python - <<EOF
import json, os
json.dump({"version": "1.0", "banner": {"enabled": False, "schedules_path": f"$BROKEN/schedules.json", "default_fields": ["sprint"]}}, open(f"$BROKEN/config.json", "w"))
EOF
python main.py --mode cli --config $BROKEN/config.json --team imagine_dragons -b
```

EXPECT:
- Yellow panel, headline `schedules.json could not be parsed:` (not "not found at").
- `(invalid JSON: ...)` reason shown.

### 8. Width adaptation eyeball check (~30s)

Resize the terminal to ~60 cols, then re-run check 1.

EXPECT:
- Title abbreviates: `26.Q1.X · WN · Mon DD`.
- Labels shrink: `Champ:` and `DoD:`.
- Names truncated to 4 chars (`Alic`, `Yoch`).

Resize to ~35 cols and re-run.

EXPECT:
- No box-drawing characters.
- One pipe-separated line: `26.Q1.X WN | Champ:Alic | DoD:... | DR in Nd`.

### 9. Sprints table is honored when present (~30s)

The bundled `config/schedules.example.json` ships with an explicit `sprints` block. Verify it overrides the `DR - 14` heuristic:

```bash
python -c "
from datetime import date
from pathlib import Path
from src.banner.cadence import current_sprint, sprint_week
from src.banner.schedule_loader import load_schedules
sched = load_schedules(Path('config/schedules.example.json'))
# Sprint Q1.1 in the example: start=2026-01-04, end=2026-01-24
today = date(2026, 1, 18)
print('sprint:', current_sprint(sched, today))
print('week:',   sprint_week(sched, current_sprint(sched, today), today))
"
```

EXPECT:
- `sprint: 26.Q1.1`
- `week: 3` (Jan 4 + 14 days = Jan 18 → day 15 → week 3)

### 10. Launcher menu wiring (~60s)

```bash
bash /Users/yosii/work/git/personal_code/code/bash/tools/launcher/launcher.sh
```

- Pick the Daily Standup Timer entry.
- EXPECT options `[1]` through `[6]`, prompt `[0-6]`.
- Pick `[2]` → CLI starts WITH banner. **Ctrl+C** out.
- Pick `[3]` → prompts `Enter banner text:`. Type `manual smoke test` and Enter. Banner appears with that text. **Ctrl+C** out.
- Pick `[0]` → returns to main menu.

## Cleanup

```bash
rm -rf "$TMP" "$BAD" "$BROKEN" 2>/dev/null
```

## Pass criteria

All 9 checks ✅. Time ≤ 5 minutes (excluding Ctrl+C waits).

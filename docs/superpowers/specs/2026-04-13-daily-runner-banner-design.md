# Daily Runner — Standup Banner

**Status:** Spec — pending implementation
**Owner:** yosi
**Created:** 2026-04-13
**Target module:** `code/python/tools/daily_runner/`

## Goal

Add an opt-in banner to the Daily Standup Timer CLI that surfaces release-cadence context (sprint, week, champion, DoD, next release event) and an optional free-text greeting, before the timer starts. Two flavors are independently togglable: cadence fields and free text.

## Non-goals

- UI (Streamlit) banner — CLI only for now.
- History view banner.
- Editing schedule data from inside daily_runner — the JSON is owned by another repo.
- Auto-discovery of `schedules.json` location.

## CLI surface

```
-b [VALUE]                # banner ON; VALUE is fields-csv OR free text (auto-detected)
--banner-fields F1,F2,... # explicit fields override
--banner-text "..."       # explicit free text
--no-banner               # force off, overrides config
```

### Disambiguation rules for bare `-b VALUE`

The parser inspects `VALUE`:

1. If absent → banner ON, default fields from config.
2. If contains spaces → free text.
3. If matches `^[a-z_,]+$` AND every comma-separated token is a known field → fields list.
4. Otherwise → free text.

`--banner-fields` and `--banner-text` are unambiguous and may be combined.

### Examples

```
python main.py --mode cli -b
python main.py --mode cli -b sprint,champion,dod
python main.py --mode cli -b "welcome back Muhe"
python main.py --mode cli --banner-fields sprint,dod --banner-text "welcome back Muhe"
python main.py --mode cli --no-banner   # explicit off
```

### Precedence

`--no-banner` > `-b/--banner-fields/--banner-text` > `config.banner.enabled`.

## Config (`config.json`) additions

```json
{
  "banner": {
    "enabled": false,
    "schedules_path": "/Users/yosii/work/CheckPoint/Jira/release/reminder_app/config/schedules.json",
    "default_fields": ["sprint", "sprint_week", "champion", "dod", "next_event"]
  }
}
```

`enabled: true` makes `-b` implicit on every CLI run; can be overridden by `--no-banner`. `schedules_path` is read literally; no glob/expansion beyond `~`.

## Field set

| Field         | Output example                    | Source                                                                                              |
| ------------- | --------------------------------- | --------------------------------------------------------------------------------------------------- |
| `sprint`      | `26.Q2.1`                         | latest key in `rotation_schedule` whose `[sprint_start, next_sprint_start)` window contains today.  |
| `sprint_week` | `Week 2`                          | `(today - sprint_start).days // 7 + 1`, clamped to `[1, 3]`.                                        |
| `champion`    | `Yocheved`                        | `rotation_schedule[sprint].champion` — title-cased.                                                 |
| `dod`         | `Yocheved`                        | `dod_schedule[week_of_today]` where `week_of_today = Sunday of this week`. Title-cased.             |
| `next_event`  | `DR in 13d · Mon Apr 26`          | State machine: pre-DR→DR; post-DR pre-prod→Prod; post-prod→next sprint's DR.                        |

### Sprint-window definition

`sprint_start = dr_date - timedelta(days=14)`. The "current sprint" is the latest sprint whose `sprint_start <= today < next_sprint_start`. If today precedes all sprint starts, fall back to the earliest sprint.

### `next_event` state transitions

| Today vs current sprint   | Display                          |
| ------------------------- | -------------------------------- |
| `today < dr`              | `DR in <N>d · <Mon DD>`          |
| `dr <= today < prod`      | `Prod in <N>d · <Mon DD>`        |
| `today >= prod`           | next sprint's DR (same format)   |

`<N>` is calendar-day delta. `<Mon DD>` formatting: `Mon Apr 26`.

## Module layout

```
src/banner/
├── __init__.py            # exposes render_banner(args, config) -> str | None
├── schedule_loader.py     # load_schedules(path) -> Schedules | raises BannerError
├── cadence.py             # pure date logic; no I/O
├── renderer.py            # rich.Panel composition; width-adaptive
└── errors.py              # BannerError, MissingScheduleError
```

### Responsibilities

- **`schedule_loader`** — open file, parse JSON, validate top-level keys (`rotation_schedule`, `dod_schedule`, `team_members`), raise `MissingScheduleError` (with the path) on `FileNotFoundError`. No date logic.
- **`cadence`** — pure functions: `current_sprint(schedules, today)`, `sprint_week(schedules, sprint_id, today)`, `dod_for(schedules, today)`, `next_event(schedules, today)`. Take `today: date` for testability.
- **`renderer`** — assembles fields into a `rich.Panel`. Decides layout from `Console().width`. Handles error rendering (missing-schedule banner).
- **`__init__.py`** — thin orchestrator: parse CLI args, load config, dispatch to loader/cadence/renderer, return final string for the caller to print.

## Renderer behavior

### Width thresholds

- `width >= 80` → wide panel (full labels, full names, full date).
- `40 <= width < 80` → narrow panel (4-char name truncation, short labels: `Champ`, `DoD`, `DR in Nd`).
- `width < 40` → single-line plain text, no panel chrome.

### Wide layout (mock, 80 cols)

```
╭─ Sprint 26.Q2.1 · Week 2 ──────── Mon Apr 13 ─╮
│  Champion: Yocheved   DoD: Yocheved            │
│  DR in 13d · Mon Apr 26                        │
│  welcome back Muhe!                            │
╰────────────────────────────────────────────────╯
```

### Narrow layout (mock, 60 cols)

```
╭─ 26.Q2.1 W2 · Apr 13 ──────────╮
│ Champ: Yoch   DoD: Yoch        │
│ DR in 13d                      │
│ welcome back Muhe!             │
╰────────────────────────────────╯
```

### Tiny layout (<40 cols)

```
26.Q2.1 W2 | Champ:Yoch | DoD:Yoch | DR 13d
welcome back Muhe!
```

### Styling

- Border color: cyan (matches launcher palette).
- Labels: dim white.
- Values: bold.
- Countdown ≤2 days: yellow. Day-of: red.
- Free-text line: dim, no styling overrides — preserves user-supplied emoji.

## Error handling — missing schedules.json

When any cadence field is requested but the file doesn't exist or is unreadable, render this in place of the cadence panel and continue with the timer (non-fatal):

```
╭─ ⚠ Banner unavailable ─────────────────────────╮
│ schedules.json not found at:                   │
│   <resolved path>                              │
│                                                │
│ Fix:                                           │
│   1. Set banner.schedules_path in config.json  │
│   2. Or copy the example:                      │
│      cp config/schedules.example.json \        │
│         config/schedules.json                  │
│   3. Or run with --no-banner to suppress       │
╰────────────────────────────────────────────────╯
```

If only `--banner-text` is supplied (no fields), the loader is never called — free-text-only banner works without `schedules.json`.

If JSON parses but is malformed (missing required keys, bad date strings), the same error banner appears with the underlying error message in place of the path note.

If the user supplies both fields (which fail) AND free text, the error banner renders, **then** the free-text line renders below it. Free text is never silently dropped because the schedule is missing.

## Example schedule file

`code/python/tools/daily_runner/config/schedules.example.json` ships with the repo. Same shape as the real `schedules.json` but with anonymized names and dates anchored at `2026-01-01` (relative offsets preserved). README points users to it for first-run setup.

## Testing

Coverage target: ≥90% for the new `src/banner/` module.

### `test_schedule_loader.py`

- File missing → `MissingScheduleError` with path in message.
- File present, invalid JSON → `BannerError`.
- File present, missing required top-level key → `BannerError`.
- File present, valid → returns parsed `Schedules` object.
- Empty path string → `MissingScheduleError`.

### `test_cadence.py`

Parametrized table: `(today, expected_sprint, expected_week, expected_dod, expected_next_event)` covering:

- Mid-sprint week 2.
- Sprint boundary day (last day of sprint N, first day of sprint N+1).
- DR day itself.
- Day between DR and prod.
- Prod day.
- Day after prod (rolls to next sprint's DR).
- Today before any sprint start (clamps to earliest sprint).
- Today after last sprint (returns last sprint).
- Year boundary (dec→jan).

All tests use frozen dates; no `datetime.now()` in code under test.

### `test_renderer.py`

- Wide width (100): assert all field labels appear in output.
- Narrow width (60): assert short labels and 4-char truncation.
- Tiny width (35): assert single-line, no panel chrome.
- Free-text-only banner: no cadence fields rendered.
- Missing-schedule path: error banner content matches expected fragments.
- Countdown styling: `≤2` days produces yellow, `0` days produces red.

### `test_cli_parsing.py`

- `-b` → banner enabled, default fields.
- `-b sprint,dod` → fields override.
- `-b "welcome back"` → free text only.
- `-b sprint,dod --banner-text "hi"` → fields + text.
- `-b "x" --banner-fields y` → both explicit, both honored.
- `--no-banner -b sprint` → banner OFF (negation wins).
- Config `enabled: true` + no flags → banner ON.
- Config `enabled: true` + `--no-banner` → banner OFF.

### Snapshot tests

Renderer output captured as fixture strings; pytest asserts substring presence rather than exact match (resilient to minor rich formatting changes).

## Launcher integration

`code/bash/tools/launcher/launcher.sh`, `show_daily_timer_menu` and `handle_daily_timer_menu`:

```
[1]  Start Meeting (CLI)
[2]  Start Meeting (CLI + Banner)              ← new
[3]  Start Meeting (CLI + Banner + Text)       ← new
[4]  Start Meeting (Web UI)
[5]  View Meeting History
[6]  View History (Custom Range)
[0]  ← Back to Main Menu
```

Handler logic:

- `[2]` → `python main.py --mode cli --team imagine_dragons -b`
- `[3]` → prompts `Enter banner text: `, then runs `python main.py --mode cli --team imagine_dragons -b "<entered>"`. Empty input falls back to `[2]` behavior.

The existing prompt-loop `[0-4]` updates to `[0-6]`. Existing tests in `code/bash/tools/launcher/tests/` get a new test case for the renumbered choices.

## Documentation

Update breadcrumbs at every level that references daily_runner:

- **`code/python/tools/daily_runner/README.md`** — full **Banner** section: CLI examples, config schema, field reference, troubleshooting (missing schedules.json), wide/narrow ASCII mocks. Pointer to `config/schedules.example.json`.
- **`code/python/tools/README.md`** — one-line bump under daily_runner entry: "with optional standup banner showing release cadence".
- **`code/python/README.md`** — if it lists daily_runner, add banner to the bullet.
- **`code/README.md`** — if a tools-overview section exists.
- **`code/bash/tools/launcher/README.md`** — document the two new menu items.
- **`code/bash/tools/launcher/CHANGELOG.md`** — entry for the new menu options.

Only edit READMEs that already mention daily_runner. Don't add new cross-refs.

## Implementation phases

Designed for parallel agent execution where possible.

### Phase 1 — Foundations (parallel-safe)

1A. **Schedule loader** — `src/banner/schedule_loader.py` + `errors.py` + `test_schedule_loader.py` + `config/schedules.example.json`.

1B. **Cadence logic** — `src/banner/cadence.py` + `test_cadence.py`.

1C. **Renderer** — `src/banner/renderer.py` + `test_renderer.py`. Uses fakes for cadence; doesn't depend on 1B.

These three can run in parallel as separate agents — no shared files.

### Phase 2 — Wiring (sequential, depends on Phase 1)

2A. **Module orchestrator** — `src/banner/__init__.py` exposing `render_banner(args, config)`.

2B. **CLI integration** — modify `main.py` to register `-b/--banner-fields/--banner-text/--no-banner`, route to `render_banner`, print result before timer starts. Add `test_cli_parsing.py`.

2C. **Config schema** — extend config loader to parse `banner` section with sensible defaults.

### Phase 3 — Surface (parallel-safe, depends on Phase 2)

3A. **Launcher menu** — update `launcher.sh` `show_daily_timer_menu` + `handle_daily_timer_menu` + launcher tests.

3B. **Docs** — README cascade.

3C. **Coverage gate** — verify ≥90% on `src/banner/`; fix gaps.

### Phase 4 — Validation

End-to-end smoke test: real `schedules.json`, run all CLI variations, verify visual output at three terminal widths, run launcher menu options 2 and 3.

## Risks & open questions

- **Width detection in piped contexts** (`python main.py | tee out.log`) — `Console().width` falls back to 80. Acceptable.
- **Title-casing names** — `dod_schedule` uses `"muhe"`, `team_members` uses `"muhammad": ...` and `"muhe": ...` (same Slack ID). Renderer should prefer `team_members` lookup for canonical name; if not found, fall back to title-casing the raw value.
- **Sprint detection at year boundaries** — sprint keys span calendar years (`25.Q4.4` → `26.Q1.1`). Logic uses dates, not key names, so this is naturally handled, but covered explicitly in tests.
- **Free-text length** — no enforced limit. Renderer wraps via rich; very long text on narrow terminals may dominate the panel. Acceptable.

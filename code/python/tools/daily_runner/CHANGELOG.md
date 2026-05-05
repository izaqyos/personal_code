# Changelog

All notable changes to the Daily Standup Timer will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added — Standup Banner

- Opt-in CLI banner showing release-cadence context (sprint, week, champion, DoD, next DR/Prod event) plus optional free-text greeting before standup starts.
- CLI flags: `-b [VALUE]` (bare or fields-csv or free text), `--banner-fields`, `--banner-text`, `--no-banner`.
- `--banner-fields` validates tokens against the canonical set (`sprint`, `sprint_week`, `champion`, `dod`, `next_event`); unknowns rejected at parse time.
- New `banner` section in `config.json`: `enabled`, `schedules_path` (absolute or `~`-prefixed), `default_fields`. `BannerConfig.default_fields` validated against the canonical set.
- Optional `sprints` section in `schedules.json` provides explicit sprint windows (`{start, end}` per sprint id). Falls back to `DR - 14 days` heuristic when absent.
- `config/schedules.example.json` ships as anonymized template anchored at 2026-01-01, with example `sprints` block.
- Width-adaptive rendering: full rich panel ≥80 cols, compact 40-79, plain text <40.
- Graceful degrade on missing/malformed `schedules.json`: distinct error headlines (`not found at:` vs `could not be parsed:`), actionable Fix instructions, standup proceeds.
- Manual smoke-test procedure at [docs/MANUAL_TEST_BANNER.md](docs/MANUAL_TEST_BANNER.md) (≤5 min, 9 checks).

### Module structure

New `src/banner/` package: `errors`, `models`, `schedule_loader`, `cadence`, `renderer`, and orchestrator (`__init__.py` exposing `render_banner` and `KNOWN_BANNER_FIELDS`).

## [1.1.0] - 2026-03-01

### Added

- Inactivity timeout for CLI mode — auto-closes forgotten meetings after 10 minutes of no keyboard input
- Meeting ends gracefully on timeout: finalizes current speaker, saves history, shows summary
- Any key press resets the inactivity timer (works during paused state too)
- `timer.inactivity_timeout_seconds` config option (range: 60-1800s, default: 600s)
- `--version` / `-V` flag to CLI entry points

### Changed

- Version is now sourced dynamically from `pyproject.toml` via `importlib.metadata`

## [1.0.0] - 2026-01-08

### Added

- Per-speaker timers with configurable time limits (default: 3 minutes)
- Visual alerts for warnings, overtime, and overflow states
- Grace period (15s) after timer expires with warning indicator
- Overflow period (90s after grace) with bold red hard-limit display
- Two interface modes: Streamlit UI and Interactive CLI
- Meeting history tracking with per-team analytics
- Session recovery for crash resilience
- Multi-team support with separate team configuration files
- Rotating file logging (5MB max, 3 backups) to `logs/` directory
- Keyboard shortcuts via `streamlit-hotkeys` in the Streamlit UI
- Launcher integration (`launcher.sh` option 5)
- E2E testing infrastructure with `pytest-playwright`
- Sample team template (`teams/sample_team.json`)

[Unreleased]: https://github.com/yosii/daily-standup-timer/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/yosii/daily-standup-timer/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/yosii/daily-standup-timer/releases/tag/v1.0.0

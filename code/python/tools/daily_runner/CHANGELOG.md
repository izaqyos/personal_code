# Changelog

All notable changes to the Daily Standup Timer will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

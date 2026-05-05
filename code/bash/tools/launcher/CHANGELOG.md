# Changelog

All notable changes to `launcher.sh` are recorded here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
this project uses [Semantic Versioning](https://semver.org/).

## Unreleased

### Added
- Daily Timer menu: `[2] Start Meeting (CLI + Banner)` runs the standup with the cadence banner.
- Daily Timer menu: `[3] Start Meeting (CLI + Banner + Text)` prompts for free text and shows it under the banner.
- Renumbered: Web UI is now `[4]`, View History is now `[5]`, View History (Custom Range) is now `[6]`.

### Fixed
- `[3] CLI + Banner + Text` now invokes `-b --banner-text "$banner_text"` instead of hardcoding `--banner-fields`. The orchestrator decides cadence vs free-text-only from config, so users without `banner.schedules_path` configured get a clean text-only banner instead of a "Banner unavailable" error.

## [1.1.0] - 2026-04-30

### Added
- Reminder submenu option `[17] Send DoD Heads-Up` wiring `remind_champion.py --dod-heads-up` with four modes: dry-run, test (yosi_test redirect), test+dry-run, and real send (with confirmation).
- `--version` / `-v` flag prints the launcher version and exits.
- `LAUNCHER_VERSION` constant inside `launcher.sh`.
- Test suite at `tests/`:
  - `test_formatting.sh` — pure helper coverage (kept from prior file `test_launcher_formatting.sh`).
  - `test_menu_rendering.sh` — every `show_*_menu` renders without errors and contains expected option labels.
  - `test_handler_dispatch.sh` — handlers shell out to the right command/arg combo, verified via a `python3` stub on PATH.
  - `run_all.sh` — runs every test file and reports a single pass/fail summary.
- `README.md` documenting layout, version, and how to run/test.

### Changed
- Relocated `code/bash/launcher.sh` → `code/bash/tools/launcher/launcher.sh` (preserved history via `git mv`).
- Relocated `code/bash/test_launcher_formatting.sh` → `code/bash/tools/launcher/tests/test_formatting.sh`.
- `code/bash/launcher.sh` is now a relative symlink to `tools/launcher/launcher.sh` so existing invocations keep working.

## [1.0.0] - prior

Initial baseline before the relocation. Contained the main launcher, all submenus
(Tracker, Repo Cleaner, Context Generator, Remind Champion, Daily Timer, MCP Helper,
Emoji Generator, Backup), and a partial test file covering formatting helpers only.

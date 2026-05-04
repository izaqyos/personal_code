# launcher.sh

Interactive bash menu that fans out into the personal toolkit: cursor tracker,
remind-champion, repo cleaner, context generator, daily standup timer, MCP
helper, emoji generator, and backup agent.

## Layout

```
code/bash/
├── launcher.sh                     # symlink → tools/launcher/launcher.sh
└── tools/launcher/
    ├── launcher.sh                 # the launcher
    ├── CHANGELOG.md
    ├── README.md
    └── tests/
        ├── run_all.sh              # runs every test_*.sh below
        ├── test_formatting.sh      # pure helper coverage
        ├── test_menu_rendering.sh  # smoke-tests every show_*_menu
        └── test_handler_dispatch.sh # asserts handlers build the right argv
```

`code/bash/launcher.sh` is a relative symlink kept for backward compatibility —
existing aliases, cron jobs, and muscle-memory invocations continue to work.

## Running

```bash
# from anywhere
/Users/yosii/work/git/personal_code/code/bash/launcher.sh

# print version and exit
launcher.sh --version
```

## Running the tests

```bash
cd code/bash/tools/launcher/tests
bash run_all.sh
```

`run_all.sh` runs every `test_*.sh` in the directory and exits non-zero if any
suite fails. Individual suites can also be run directly.

### What is covered

| Suite                       | Covers                                                                 |
| --------------------------- | ---------------------------------------------------------------------- |
| `test_formatting.sh`        | `strip_ansi`, `visible_length`, `pad_*`, box-drawing, menu-line widths |
| `test_menu_rendering.sh`    | every `show_*_menu` renders cleanly and shows expected option labels   |
| `test_handler_dispatch.sh`  | `handle_reminder_menu` cases build the right `python3 …` invocations   |

### What is **not** covered (by design)

- Interactive flows beyond the dispatched argv (we don't drive every prompt-and-confirm
  combination — too brittle for too little signal).
- The downstream Python scripts the launcher shells out to. Those have their own
  test suites.

The handler-dispatch suite mocks `python3` with a stub on `PATH` that records its
argv; tests then assert the recorded argv contains the expected flags. Keep it
that way — adding more case branches just means adding more `assert_log_contains`
lines, not new infrastructure.

## Versioning

- `LAUNCHER_VERSION` lives at the top of `launcher.sh`.
- `launcher.sh --version` (or `-v`) prints it and exits.
- See `CHANGELOG.md` for what changed and when. Bump the constant + add a
  changelog entry whenever menu options change or behaviour shifts.

## Daily Timer

The daily standup submenu wraps the `daily_runner` Python CLI/UI. New options
support the standup banner (release cadence context shown before the meeting):

- `[2] Start Meeting (CLI + Banner)` — runs CLI standup with the cadence banner enabled.
- `[3] Start Meeting (CLI + Banner + Text)` — prompts for free text, then runs CLI standup with banner + text.

See `code/python/tools/daily_runner/README.md` for the banner fields,
`schedules.json` setup, and `--no-banner` / `--banner-fields` / `--banner-text`
flags.

## Adding a new submenu option

1. Edit the relevant `show_*_menu` function (display).
2. Edit the matching `handle_*_menu` case dispatcher.
3. Update the prompt range (e.g. `[0-17]`).
4. Add a label-presence assertion in `test_menu_rendering.sh`.
5. Add `assert_log_contains` lines in `test_handler_dispatch.sh` for the new case.
6. Bump `LAUNCHER_VERSION` and add a `CHANGELOG.md` entry.
7. Run `bash tests/run_all.sh` and confirm all suites pass.

# Claude Code status line: context, cost and plan-limit pace

```
Opus 5.5 · private · ctx 17% 174k/1.0M · $18.56 · 2h05m · +1586/-39 · 5h 23% 1.0/5h ⚠ out in ~3.2h · wk 21% 2.6/7d
```

| Part | Meaning |
|---|---|
| `ctx 17% 174k/1.0M` | Context window used (green < 50%, yellow < 80%, red ≥ 80%) |
| `$18.56` | Session cost |
| `2h05m` | Session wall-clock time |
| `+1586/-39` | Lines added / removed this session |
| `5h 23% 1.0/5h` | 5-hour limit: % used, then hours elapsed in the window |
| `wk 21% 2.6/7d` | Weekly limit: % used, then days elapsed in the window |
| `⚠ out in ~3.2h` | At the current rate you'll hit 100% before the window resets |

Plan-limit colours show **pace** (usage % vs % of the window elapsed): green = on or under pace, yellow =
ahead, red = will run out before the reset. Warnings are suppressed during the first 10% of a window unless
usage is already ≥ 30%. Any field Claude Code doesn't send is skipped.

## Install
```bash
ln -sf "$PWD/statusline.py" ~/.claude/statusline.py   # run from this folder; edits here go live
```
Add to `~/.claude/settings.json`:
```json
"statusLine": { "type": "command", "command": "python3 ~/.claude/statusline.py", "padding": 0 }
```
Python 3 standard library only.

## Debug
Each refresh saves the raw input to `~/.claude/statusline-last-input.json`. Test without Claude Code:
```bash
python3 statusline.py < ~/.claude/statusline-last-input.json
```

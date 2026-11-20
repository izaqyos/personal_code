---
description: Review the current branch against the team's AI review procedure and wiki
argument-hint: "[base-ref] [--include-uncommitted]"
allowed-tools: Read, Grep, Glob, Write, Bash(aireview:*), Bash(git diff:*), Bash(git log:*), Bash(git merge-base:*), Bash(git status:*)
---

Run the team code review on the current branch.

Follow `.ai-review/REVIEW.md` exactly — it is the source of truth for the procedure,
severity rubric and output format. Read it now.

- Base ref: `$ARGUMENTS` if given, otherwise the `base` in `.ai-review/config.json`.
- Step 1: run `aireview context --base <base>` (append `--include-uncommitted` if asked)
  and read `.ai-review/out/context.md`. If `aireview` is not installed, use the
  fallback steps in REVIEW.md.
- If the user pasted a PR description, save it to `.ai-review/out/pr_body.md` first.
- Step 5: write `.ai-review/out/findings.json`, run `aireview validate --base <base>`,
  and show me the rendered report. Do not edit source files during the review.

---
mode: agent
description: Review the current branch with the team AI review procedure
tools: ["codebase", "terminal"]
---

Review the current branch following [the review procedure](../../.ai-review/REVIEW.md).

1. Run `aireview context --base origin/main` in the terminal and read
   `.ai-review/out/context.md` (fallback steps are in REVIEW.md if the CLI is missing).
2. Review in the defined passes; cite wiki rule IDs from `.ai-review/wiki/`.
3. Write `.ai-review/out/findings.json`, run `aireview validate`, and show the report.

Do not edit source files during the review.

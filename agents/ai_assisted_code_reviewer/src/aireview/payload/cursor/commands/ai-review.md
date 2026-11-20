# AI review

Review the current branch using the team procedure in `.ai-review/REVIEW.md`.

1. Run `aireview context --base origin/main` (add `--include-uncommitted` for local work)
   and read `.ai-review/out/context.md`. No CLI? Use the fallback steps in REVIEW.md.
2. Review in the passes REVIEW.md defines, citing wiki rule IDs.
3. Write `.ai-review/out/findings.json`, run `aireview validate`, show the report.

Do not modify source files during the review.

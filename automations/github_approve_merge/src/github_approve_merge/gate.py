from __future__ import annotations

import sys
from typing import TextIO

from github_approve_merge.actions import MergeDecision
from github_approve_merge.merge_action import MergeAction

_ACTION_LABEL = {
    MergeAction.ENQUEUE: "enqueue (merge queue)",
    MergeAction.DIRECT_MERGE: "direct merge",
    MergeAction.AUTO_MERGE: "enable auto-merge",
}


def _slug(d: MergeDecision) -> str:
    return f"{d.pr.owner}/{d.pr.repo}#{d.pr.number}"


def render_plan(decisions: list[MergeDecision]) -> str:
    lines = ["", "Merge plan:"]
    for d in decisions:
        prefix = "approve → " if d.will_approve else ""
        lines.append(f"  {_slug(d):<48} {d.state.name:<16} {prefix}{_ACTION_LABEL[d.action]}")
    return "\n".join(lines)


def make_gate(*, assume_yes: bool, confirm_each: bool, stream: TextIO = sys.stderr):
    """Build a gate(decisions) -> list[bool]. The gate prints a plan and blocks for
    confirmation before any merge, unless assume_yes."""

    def gate(decisions: list[MergeDecision]) -> list[bool]:
        if assume_yes:
            return [True] * len(decisions)
        if confirm_each:
            out = []
            for d in decisions:
                print(render_plan([d]), file=stream)
                print(f"Merge {_slug(d)}? [y/N]: ", file=stream, end="")
                ans = input("").strip().lower()
                out.append(ans in ("y", "yes"))
            return out
        print(render_plan(decisions), file=stream)
        print(f"Proceed with merge for {len(decisions)} PR(s)? [y/N]: ", file=stream, end="")
        ans = input("").strip().lower()
        return [ans in ("y", "yes")] * len(decisions)

    return gate

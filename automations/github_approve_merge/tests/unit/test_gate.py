import io

from github_approve_merge.actions import MergeDecision
from github_approve_merge.merge_action import MergeAction
from github_approve_merge.pr_state import PRState
from github_approve_merge.url import PRRef
from github_approve_merge.gate import render_plan, make_gate


D = [MergeDecision(PRRef("o", "r", 5), PRState.OPEN_MERGEABLE, MergeAction.ENQUEUE, False),
     MergeDecision(PRRef("o", "r", 6), PRState.OPEN_APPROVABLE, MergeAction.DIRECT_MERGE, True)]


def test_render_plan_lists_each_pr_and_action():
    text = render_plan(D)
    assert "o/r#5" in text and "enqueue" in text
    assert "o/r#6" in text and "approve" in text and "direct" in text


def test_yes_gate_auto_approves():
    gate = make_gate(assume_yes=True, confirm_each=False, stream=io.StringIO())
    assert gate(D) == [True, True]


def test_interactive_gate_reads_yes(monkeypatch):
    out = io.StringIO()
    monkeypatch.setattr("builtins.input", lambda *_: "y")
    gate = make_gate(assume_yes=False, confirm_each=False, stream=out)
    assert gate(D) == [True, True]
    assert "Proceed with merge for 2" in out.getvalue()


def test_interactive_gate_reads_no(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda *_: "")
    gate = make_gate(assume_yes=False, confirm_each=False, stream=io.StringIO())
    assert gate(D) == [False, False]


def test_confirm_each(monkeypatch):
    answers = iter(["y", "n"])
    monkeypatch.setattr("builtins.input", lambda *_: next(answers))
    gate = make_gate(assume_yes=False, confirm_each=True, stream=io.StringIO())
    assert gate(D) == [True, False]

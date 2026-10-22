"""Tests for the TF-IDF Tier 1 classifier."""

from __future__ import annotations

import pytest

from bug_triage.kb import KnowledgeBase, load_eval
from bug_triage.models import Bug, LabeledBug
from bug_triage.tier1_tfidf import Tier1Classifier


@pytest.fixture(scope="module")
def fitted(kb: KnowledgeBase) -> Tier1Classifier:
    return Tier1Classifier(kb).fit()


def _bug(text_title: str, desc: str = "", logs: str = "") -> Bug:
    return Bug(id="NEW", title=text_title, description=desc, logs=logs)


def _root(kb: KnowledgeBase, bug_id: str) -> str:
    by_id = {b.id: b for b in kb.history}
    while by_id[bug_id].duplicate_of:
        bug_id = str(by_id[bug_id].duplicate_of)
    return bug_id


def test_predict_before_fit_raises(kb: KnowledgeBase, sample_bug: Bug) -> None:
    with pytest.raises(RuntimeError):
        Tier1Classifier(kb).predict(sample_bug)


def test_fit_returns_self(kb: KnowledgeBase) -> None:
    clf = Tier1Classifier(kb)
    assert clf.fit() is clf


def test_valid_result_on_real_kb(
    fitted: Tier1Classifier, kb: KnowledgeBase, sample_bug: Bug
) -> None:
    res = fitted.predict(sample_bug)
    assert len(res.component_candidates) == 3
    scores = [c.score for c in res.component_candidates]
    assert scores == sorted(scores, reverse=True)
    assert all(0.0 <= s <= 1.0 for s in scores)
    top = res.top_component()
    assert kb.is_valid_component(top)
    assert res.team == kb.owner_team(top)
    assert res.assignee == kb.default_assignee(top)
    assert len(res.similar_bugs) == 5
    assert len(res.known_issue_hits) == 5
    for seq in (res.similar_bugs, res.known_issue_hits):
        s = [x.score for x in seq]
        assert s == sorted(s, reverse=True)
        assert all(0.0 <= v <= 1.0 for v in s)
    assert res.elapsed_ms >= 0.0


def test_history_bug_exact_text(fitted: Tier1Classifier, kb: KnowledgeBase) -> None:
    h = kb.history[0]
    res = fitted.predict(h)
    assert res.top_component() == h.component
    assert res.similar_bugs[0].bug_id == h.id
    assert res.similar_bugs[0].score > 0.99
    assert res.duplicate_of == _root(kb, h.id)


def test_duplicate_history_bug_points_to_root(fitted: Tier1Classifier, kb: KnowledgeBase) -> None:
    dup = next(b for b in kb.history if b.duplicate_of)
    res = fitted.predict(dup)
    assert res.similar_bugs[0].bug_id == dup.id
    assert res.similar_bugs[0].duplicate_of == dup.duplicate_of
    assert res.duplicate_of == _root(kb, dup.id)
    by_id = {b.id: b for b in kb.history}
    assert by_id[str(res.duplicate_of)].duplicate_of is None


def test_known_issue_symptoms_match(fitted: Tier1Classifier, kb: KnowledgeBase) -> None:
    for ki in kb.known_issues.values():
        res = fitted.predict(_bug(ki.title, ki.symptoms))
        assert res.known_issue == ki.id
        assert res.known_issue_hits[0].id == ki.id


def test_duplicate_chain_followed_to_root(tiny_kb: KnowledgeBase) -> None:
    prev = tiny_kb.history[-1]  # BUG-8 -> BUG-4
    tiny_kb.history.append(
        LabeledBug(
            id="BUG-9",
            title="Totally different zebra",
            description="zebra giraffe unique words",
            component="api",
            team="Alpha",
            assignee="Ben Hart",
            severity="low",
            duplicate_of=prev.id,
        )
    )
    clf = Tier1Classifier(tiny_kb).fit()
    res = clf.predict(_bug("Totally different zebra", "zebra giraffe unique words"))
    assert res.similar_bugs[0].bug_id == "BUG-9"
    assert res.duplicate_of == "BUG-4"


def test_dup_threshold_respected(kb: KnowledgeBase) -> None:
    h = kb.history[0]
    assert Tier1Classifier(kb, dup_threshold=1.01).fit().predict(h).duplicate_of is None
    assert Tier1Classifier(kb, dup_threshold=0.0).fit().predict(h).duplicate_of is not None


def test_ki_threshold_respected(kb: KnowledgeBase) -> None:
    ki = next(iter(kb.known_issues.values()))
    clf = Tier1Classifier(kb, ki_threshold=1.01).fit()
    assert clf.predict(_bug(ki.title, ki.symptoms)).known_issue is None


def test_top_k_honored(kb: KnowledgeBase, sample_bug: Bug) -> None:
    res = Tier1Classifier(kb, top_k=2).fit().predict(sample_bug)
    assert len(res.similar_bugs) == 2
    assert len(res.known_issue_hits) == 2


@pytest.mark.parametrize("title", ["", "x", "the"])
def test_empty_or_short_text(fitted: Tier1Classifier, title: str) -> None:
    res = fitted.predict(_bug(title))
    assert len(res.component_candidates) == 3
    assert res.duplicate_of is None
    assert res.known_issue is None
    assert all(s.score == 0.0 for s in res.similar_bugs)


def test_deterministic(fitted: Tier1Classifier, kb: KnowledgeBase, sample_bug: Bug) -> None:
    other = Tier1Classifier(kb).fit()
    a, b = fitted.predict(sample_bug), other.predict(sample_bug)
    assert a.component_candidates == b.component_candidates
    assert a.similar_bugs == b.similar_bugs


def test_single_class_history(tiny_kb: KnowledgeBase) -> None:
    tiny_kb.history = [h for h in tiny_kb.history if h.component == "auth"]
    res = Tier1Classifier(tiny_kb).fit().predict(_bug("Login fails", "password rejected"))
    assert [(c.label, c.score) for c in res.component_candidates] == [("auth", 1.0)]
    assert res.team == "Alpha"
    assert res.assignee == "Ada Quill"


def test_no_known_issues(tiny_kb: KnowledgeBase) -> None:
    tiny_kb.known_issues = {}
    res = Tier1Classifier(tiny_kb).fit().predict(_bug("Login fails", "password rejected"))
    assert res.known_issue_hits == []
    assert res.known_issue is None


def test_empty_history_rejected(tiny_kb: KnowledgeBase) -> None:
    tiny_kb.history = []
    with pytest.raises(ValueError):
        Tier1Classifier(tiny_kb).fit()


def test_real_eval_error_rate_sane(fitted: Tier1Classifier) -> None:
    bugs = load_eval()
    wrong = 0
    for b in bugs:
        p = fitted.predict(b).to_prediction()
        wrong += int(p.component != b.component or p.assignee != b.assignee)
    assert 0.05 <= wrong / len(bugs) <= 0.6

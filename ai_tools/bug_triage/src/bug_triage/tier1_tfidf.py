"""Tier 1: local TF-IDF classifier plus retrieval over history and known issues."""

from __future__ import annotations

import logging
import time
from typing import Any

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics.pairwise import linear_kernel
from sklearn.pipeline import Pipeline

from bug_triage.kb import KnowledgeBase
from bug_triage.models import (
    Bug,
    Candidate,
    KnownIssueHit,
    SimilarBug,
    Tier1Result,
)

logger = logging.getLogger(__name__)

_N_CANDIDATES = 3


def _vectorizer() -> TfidfVectorizer:
    return TfidfVectorizer(
        ngram_range=(1, 2), sublinear_tf=True, lowercase=True, stop_words="english", min_df=1
    )


def _clamp(x: float) -> float:
    return float(min(1.0, max(0.0, x)))


class Tier1Classifier:
    """TF-IDF + logistic regression component classifier with cosine retrieval."""

    def __init__(
        self,
        kb: KnowledgeBase,
        *,
        dup_threshold: float = 0.9,
        ki_threshold: float = 0.4,
        top_k: int = 5,
    ) -> None:
        self.kb = kb
        self.dup_threshold = dup_threshold
        self.ki_threshold = ki_threshold
        self.top_k = top_k
        self._fitted = False
        self._pipeline: Pipeline | None = None
        self._single_class: str | None = None
        self._hist_vec: TfidfVectorizer | None = None
        self._hist_matrix: Any = None
        self._ki_vec: TfidfVectorizer | None = None
        self._ki_matrix: Any = None
        self._ki_ids: list[str] = []

    def fit(self) -> Tier1Classifier:
        """Train the classifier and build the retrieval indexes from the knowledge base."""
        history = self.kb.history
        if not history:
            raise ValueError("knowledge base has no history to train on")
        texts = [b.text() for b in history]
        labels = [b.component for b in history]

        if len(set(labels)) == 1:
            self._single_class = labels[0]
            self._pipeline = None
        else:
            self._single_class = None
            self._pipeline = Pipeline(
                [
                    ("tfidf", _vectorizer()),
                    (
                        "clf",
                        LogisticRegression(max_iter=2000, class_weight="balanced", random_state=0),
                    ),
                ]
            ).fit(texts, labels)

        self._hist_vec = _vectorizer()
        self._hist_matrix = self._hist_vec.fit_transform(texts)

        kis = list(self.kb.known_issues.values())
        if kis:
            self._ki_ids = [k.id for k in kis]
            self._ki_vec = _vectorizer()
            self._ki_matrix = self._ki_vec.fit_transform([f"{k.title}\n{k.symptoms}" for k in kis])
        else:
            self._ki_ids, self._ki_vec, self._ki_matrix = [], None, None

        self._fitted = True
        logger.info("tier1 fitted on %d bugs, %d known issues", len(history), len(kis))
        return self

    def _candidates(self, text: str) -> list[Candidate]:
        if self._single_class is not None:
            return [Candidate(label=self._single_class, score=1.0)]
        assert self._pipeline is not None
        proba = self._pipeline.predict_proba([text])[0]
        classes = self._pipeline.classes_
        order = np.argsort(-proba, kind="stable")[:_N_CANDIDATES]
        return [Candidate(label=str(classes[i]), score=_clamp(proba[i])) for i in order]

    def _root(self, bug_id: str) -> str:
        by_id = {b.id: b for b in self.kb.history}
        seen: set[str] = set()
        while bug_id in by_id and by_id[bug_id].duplicate_of and bug_id not in seen:
            seen.add(bug_id)
            bug_id = str(by_id[bug_id].duplicate_of)
        return bug_id

    def _similar(self, text: str) -> list[SimilarBug]:
        assert self._hist_vec is not None
        sims = linear_kernel(self._hist_vec.transform([text]), self._hist_matrix)[0]
        order = np.argsort(-sims, kind="stable")[: self.top_k]
        out: list[SimilarBug] = []
        for i in order:
            h = self.kb.history[int(i)]
            out.append(
                SimilarBug(
                    bug_id=h.id,
                    title=h.title,
                    score=_clamp(sims[i]),
                    component=h.component,
                    assignee=h.assignee,
                    duplicate_of=h.duplicate_of,
                )
            )
        return out

    def _known_issues(self, text: str) -> list[KnownIssueHit]:
        if self._ki_vec is None:
            return []
        sims = linear_kernel(self._ki_vec.transform([text]), self._ki_matrix)[0]
        order = np.argsort(-sims, kind="stable")[: self.top_k]
        return [
            KnownIssueHit(
                id=self._ki_ids[int(i)],
                title=self.kb.known_issues[self._ki_ids[int(i)]].title,
                score=_clamp(sims[i]),
            )
            for i in order
        ]

    def predict(self, bug: Bug) -> Tier1Result:
        """Classify a bug and retrieve similar bugs and known issues."""
        if not self._fitted:
            raise RuntimeError("Tier1Classifier.predict called before fit()")
        start = time.perf_counter()
        text = bug.text()
        candidates = self._candidates(text)
        top = candidates[0].label
        similar = self._similar(text)
        hits = self._known_issues(text)

        duplicate_of: str | None = None
        if similar and similar[0].score >= self.dup_threshold:
            duplicate_of = self._root(similar[0].bug_id)
        known_issue = hits[0].id if hits and hits[0].score >= self.ki_threshold else None

        return Tier1Result(
            component_candidates=candidates,
            team=self.kb.owner_team(top),
            assignee=self.kb.default_assignee(top),
            similar_bugs=similar,
            known_issue_hits=hits,
            duplicate_of=duplicate_of,
            known_issue=known_issue,
            elapsed_ms=(time.perf_counter() - start) * 1000.0,
        )

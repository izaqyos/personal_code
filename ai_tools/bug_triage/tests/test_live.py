"""Live end-to-end test (Ollama judge + real Claude CLI). Run with: pytest -m live."""

from __future__ import annotations

import shutil

import httpx
import pytest

from bug_triage.final_claude import FinalTriager
from bug_triage.judge import Judge
from bug_triage.kb import KnowledgeBase, load_eval
from bug_triage.llm.ollama_client import OllamaClient
from bug_triage.models import PipelineResult
from bug_triage.pipeline import Pipeline
from bug_triage.tier1_tfidf import Tier1Classifier

pytestmark = pytest.mark.live

OLLAMA_URL = "http://localhost:11434"


def _ollama_up() -> bool:
    try:
        return httpx.get(f"{OLLAMA_URL}/api/tags", timeout=2.0).status_code == 200
    except httpx.HTTPError:
        return False


def test_live_pipeline_always_escalates() -> None:
    if shutil.which("claude") is None:
        pytest.skip("claude CLI not installed")
    if not _ollama_up():
        pytest.skip(f"Ollama not reachable at {OLLAMA_URL}")
    kb = KnowledgeBase.load()
    pipeline = Pipeline(
        Tier1Classifier(kb).fit(),
        Judge(OllamaClient(), kb),
        FinalTriager(kb),
        policy="always",
    )
    for bug in load_eval()[:3]:
        result = pipeline.run(bug)
        assert PipelineResult.model_validate(result.model_dump()) == result
        assert result.decision.escalated
        assert kb.is_valid_component(result.decision.component)
        assert [t.tier for t in result.trace][0] == "tier1"

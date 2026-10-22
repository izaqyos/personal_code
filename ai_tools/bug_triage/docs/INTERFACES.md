# bug_triage: frozen interfaces (contract between modules)

All data is **invented**. No real companies, products or people. The fictional product is **"Larkspur"**,
a SaaS project-management app. Python ≥ 3.11, pydantic v2, mypy --strict, ruff line length 100.
Library code logs via `logging.getLogger(__name__)`; never `print` (except `cli.py`).

## models.py (owner: Agent A). Other agents import, never edit
```python
Severity = Literal["low", "medium", "high", "critical"]
TierName = Literal["tier1", "judge", "final"]
FinalPolicy = Literal["always", "on-disagreement", "never"]

class Bug(BaseModel):            id: str; title: str; description: str; logs: str = ""
    def text(self) -> str        # title + "\n" + description + "\n" + logs, stripped

class LabeledBug(Bug):           component: str; team: str; assignee: str; severity: Severity
                                 duplicate_of: str | None = None; known_issue: str | None = None

class Candidate(BaseModel):      label: str; score: float            # score in [0, 1]
class SimilarBug(BaseModel):     bug_id: str; title: str; score: float; component: str; assignee: str
                                 duplicate_of: str | None = None
class KnownIssueHit(BaseModel):  id: str; title: str; score: float

class Prediction(BaseModel):     component: str; team: str; assignee: str
                                 duplicate_of: str | None = None; known_issue: str | None = None

class Tier1Result(BaseModel):
    component_candidates: list[Candidate]   # top 3, sorted by score desc
    team: str                                # owner team of the top component
    assignee: str                            # default assignee of the top component
    similar_bugs: list[SimilarBug]           # top_k, desc
    known_issue_hits: list[KnownIssueHit]    # top_k, desc
    duplicate_of: str | None                 # top similar bug id if score >= dup_threshold
    known_issue: str | None                  # top known-issue id if score >= ki_threshold
    elapsed_ms: float
    def top_component(self) -> str
    def top_score(self) -> float
    def to_prediction(self) -> Prediction

class TriageSuggestion(BaseModel):  # LLM output: routes to a team, never a person
    component: str; team: str; duplicate_of: str | None = None; known_issue: str | None = None
    severity: Severity; confidence: float; rationale: str   # confidence in [0,1]
class TriageDecision(TriageSuggestion):  assignee: str   # suggested contact = default owner of the decided component
    source: TierName; escalated: bool; final_error: str | None = None
    def to_prediction(self) -> Prediction

class TierTrace(BaseModel):      tier: TierName; prediction: Prediction | None; elapsed_ms: float
                                 error: str | None = None
class PipelineResult(BaseModel): decision: TriageDecision; trace: list[TierTrace]
```
Field validators: confidence/score clamp-or-reject outside [0, 1] (reject = ValidationError).

## kb.py (owner: Agent A)
```python
class Team(BaseModel):       name: str; members: list[str]; components: list[str]
class Component(BaseModel):  name: str; owner_team: str; default_assignee: str; keywords: list[str]
class KnownIssue(BaseModel): id: str; title: str; component: str; symptoms: str; workaround: str
                             status: Literal["open", "fixed", "wontfix"]
class UseCase(BaseModel):    name: str; description: str; components: list[str]

class KnowledgeBase:
    teams: dict[str, Team]; components: dict[str, Component]; known_issues: dict[str, KnownIssue]
    use_cases: list[UseCase]; history: list[LabeledBug]
    @classmethod
    def load(cls, data_dir: Path | None = None) -> "KnowledgeBase"
        # default: env BUG_TRIAGE_DATA_DIR, else <project root>/data  (Path(__file__).resolve().parents[2] / "data")
        # validates referential integrity (owner teams exist, assignees are team members, KI components exist,
        # history labels valid, duplicate_of points to an earlier history id) → raises KBError
    def owner_team(self, component: str) -> str          # KeyError on unknown
    def default_assignee(self, component: str) -> str
    def team_of(self, dev: str) -> str
    def is_valid_component(self, name: str) -> bool
    def is_valid_assignee(self, name: str) -> bool
    def history_ids(self) -> set[str]
    def roster_text(self) -> str    # compact, prompt-ready: teams → members → owned components (+ keywords)

def load_eval(data_dir: Path | None = None) -> list[LabeledBug]   # data/eval.jsonl
class KBError(Exception)
```

## tier1_tfidf.py (owner: Agent B)
```python
class Tier1Classifier:
    def __init__(self, kb: KnowledgeBase, *, dup_threshold: float = 0.9, ki_threshold: float = 0.4,
                 top_k: int = 5) -> None
    def fit(self) -> "Tier1Classifier"        # train on kb.history; index history + known issues
    def predict(self, bug: Bug) -> Tier1Result  # raises RuntimeError if not fitted
```

## llm/ and judge.py (owner: Agent C)
```python
# llm/base.py
class LLMError(Exception)
class LLMClient(Protocol):
    name: str
    def complete_json(self, system: str, user: str, schema: dict[str, Any]) -> dict[str, Any]
# llm/ollama_client.py
class OllamaClient:  def __init__(self, model: str = "gemma4:12b", base_url: str = "http://localhost:11434",
                                  timeout: float = 120.0, transport: httpx.BaseTransport | None = None)
# llm/gemini_client.py
class GeminiClient:  def __init__(self, model: str = "gemini-2.5-flash", api_key: str | None = None)
                     # api_key falls back to env GEMINI_API_KEY; lazy-imports google.genai; LLMError if missing
# judge.py
class JudgeError(Exception)
class Judge:
    def __init__(self, client: LLMClient, kb: KnowledgeBase, *, max_retries: int = 1) -> None
    def build_prompt(self, bug: Bug, t1: Tier1Result) -> tuple[str, str]   # (system, user)
    def suggest(self, bug: Bug, t1: Tier1Result) -> TriageSuggestion       # JudgeError after retries
```

## final_claude.py, pipeline.py, cli.py (owner: Agent D)
```python
# final_claude.py
class FinalTriageError(Exception)
class FinalTriager:
    def __init__(self, kb: KnowledgeBase, *, model: str = "sonnet", timeout: float = 180.0,
                 claude_bin: str = "claude",
                 runner: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run) -> None
    def decide(self, bug: Bug, t1: Tier1Result, suggestion: TriageSuggestion) -> TriageSuggestion
# pipeline.py: depends only on these Protocols (not on concrete classes)
class Tier1Like(Protocol):  def predict(self, bug: Bug) -> Tier1Result
class JudgeLike(Protocol):  def suggest(self, bug: Bug, t1: Tier1Result) -> TriageSuggestion
class FinalLike(Protocol):  def decide(self, bug: Bug, t1: Tier1Result, s: TriageSuggestion) -> TriageSuggestion
class Pipeline:
    def __init__(self, tier1: Tier1Like, judge: JudgeLike | None = None, final: FinalLike | None = None, *,
                 policy: FinalPolicy = "on-disagreement", confidence_threshold: float = 0.7) -> None
    def should_escalate(self, t1: Tier1Result, s: TriageSuggestion) -> bool
    def run(self, bug: Bug) -> PipelineResult
```
Tier1Like also has `contact(component) -> str` (the component's default owner); the pipeline uses it for the
decision's `assignee` and for the judge/final trace predictions. Duplicate and known-issue links in the decision
always come from Tier 1 (traces keep the raw LLM output).
Escalation (policy "on-disagreement"): judge component != t1.top_component(), or judge confidence <
confidence_threshold. "always" → always; "never" → never (and when final is None).
Judge error → decision from Tier 1 (source "tier1", severity "medium", confidence = t1.top_score(),
rationale "fallback: <error>"), trace has the error. Final error → keep the judge decision, `final_error` set.

## evaluate.py (owner: Agent B)
```python
class RunnerLike(Protocol):  def run(self, bug: Bug) -> PipelineResult
class TierMetrics(BaseModel):  tier: TierName; n: int; acc_component: float; acc_team: float; acc_assignee: float
                               acc_duplicate: float; acc_known_issue: float; error_rate: float; mean_ms: float
    # error_rate = share of bugs where component OR team is wrong (routing); assignee reported separately
class EvalReport(BaseModel):   tiers: list[TierMetrics]; final_decision: TierMetrics; escalation_rate: float; n: int
def run_eval(bugs: list[LabeledBug], *, tier1: Tier1Like, runner: RunnerLike | None = None,
             limit: int | None = None) -> EvalReport
    # runner None → Tier 1 only (tiers = [tier1], final_decision = tier1). Otherwise per-tier metrics from the trace.
def format_report(report: EvalReport) -> str   # aligned text table + one line "tier1 x% → judge y% → final z% error"
```

## cli.py (owner: Agent D). Console script `bug-triage = bug_triage.cli:main`
```
bug-triage triage (--title T --desc D [--logs L] | --file bug.json) [--judge ollama|gemini|none]
                  [--final always|on-disagreement|never] [--model gemma4:12b]
bug-triage eval [--tiers 1|2|3] [--judge ollama|gemini] [--final ...] [--limit N]
```
`main(argv: list[str] | None = None) -> int`: 0 ok, 1 runtime error, 2 usage error. Concrete classes are imported
lazily inside a `build_pipeline(args)` function (tests monkeypatch it). `triage` prints PipelineResult JSON.

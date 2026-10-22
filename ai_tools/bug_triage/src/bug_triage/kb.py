"""Knowledge base: teams, components, known issues, use cases and labeled history."""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Any, Literal, TypeVar

import yaml
from pydantic import BaseModel, ValidationError

from bug_triage.models import LabeledBug

logger = logging.getLogger(__name__)

DATA_DIR_ENV = "BUG_TRIAGE_DATA_DIR"
_M = TypeVar("_M", bound=BaseModel)


class KBError(Exception):
    """Raised when the data set is missing, malformed or inconsistent."""


class Team(BaseModel):
    """A team of developers owning components."""

    name: str
    members: list[str]
    components: list[str]


class Component(BaseModel):
    """A product component with an owner team."""

    name: str
    owner_team: str
    default_assignee: str
    keywords: list[str]


class KnownIssue(BaseModel):
    """A documented known issue."""

    id: str
    title: str
    component: str
    symptoms: str
    workaround: str
    status: Literal["open", "fixed", "wontfix"]


class UseCase(BaseModel):
    """A product use case mapped to components."""

    name: str
    description: str
    components: list[str]


def _resolve_dir(data_dir: Path | None) -> Path:
    if data_dir is not None:
        return Path(data_dir)
    env = os.environ.get(DATA_DIR_ENV)
    if env:
        return Path(env)
    return Path(__file__).resolve().parents[2] / "data"


def _read_yaml_list(path: Path, key: str) -> list[dict[str, Any]]:
    if not path.is_file():
        raise KBError(f"missing data file: {path}")
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise KBError(f"invalid YAML in {path}: {exc}") from exc
    items = raw.get(key) if isinstance(raw, dict) else None
    if not isinstance(items, list):
        raise KBError(f"{path} must contain a top-level list under '{key}'")
    return items


def _read_jsonl(path: Path) -> list[LabeledBug]:
    if not path.is_file():
        raise KBError(f"missing data file: {path}")
    bugs: list[LabeledBug] = []
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            bugs.append(LabeledBug.model_validate(json.loads(line)))
        except (json.JSONDecodeError, ValidationError) as exc:
            raise KBError(f"{path}:{lineno}: invalid record: {exc}") from exc
    return bugs


def _validate_models(cls: type[_M], items: list[dict[str, Any]], path: Path) -> list[_M]:
    try:
        return [cls.model_validate(i) for i in items]
    except ValidationError as exc:
        raise KBError(f"{path}: invalid {cls.__name__}: {exc}") from exc


class KnowledgeBase:
    """Validated, in-memory view of the data set."""

    def __init__(
        self,
        teams: dict[str, Team],
        components: dict[str, Component],
        known_issues: dict[str, KnownIssue],
        use_cases: list[UseCase],
        history: list[LabeledBug],
    ) -> None:
        self.teams = teams
        self.components = components
        self.known_issues = known_issues
        self.use_cases = use_cases
        self.history = history

    @classmethod
    def load(cls, data_dir: Path | None = None) -> KnowledgeBase:
        """Load and validate the data set (arg, else $BUG_TRIAGE_DATA_DIR, else <root>/data)."""
        d = _resolve_dir(data_dir)
        logger.info("loading knowledge base from %s", d)
        team_list = _validate_models(Team, _read_yaml_list(d / "teams.yaml", "teams"), d)
        comp_list = _validate_models(
            Component, _read_yaml_list(d / "components.yaml", "components"), d
        )
        ki_list = _validate_models(
            KnownIssue, _read_yaml_list(d / "known_issues.yaml", "known_issues"), d
        )
        uc_list = _validate_models(UseCase, _read_yaml_list(d / "use_cases.yaml", "use_cases"), d)
        history = _read_jsonl(d / "history.jsonl")
        kb = cls(
            teams={t.name: t for t in team_list},
            components={c.name: c for c in comp_list},
            known_issues={k.id: k for k in ki_list},
            use_cases=uc_list,
            history=history,
        )
        kb._check_unique(team_list, comp_list, ki_list)
        kb._validate()
        return kb

    @staticmethod
    def _check_unique(teams: list[Team], comps: list[Component], kis: list[KnownIssue]) -> None:
        for label, names in (
            ("team", [t.name for t in teams]),
            ("component", [c.name for c in comps]),
            ("known issue", [k.id for k in kis]),
        ):
            if len(set(names)) != len(names):
                raise KBError(f"duplicate {label} names/ids")

    def _validate(self) -> None:
        for comp in self.components.values():
            if comp.owner_team not in self.teams:
                raise KBError(f"component {comp.name}: unknown owner team {comp.owner_team}")
            if comp.default_assignee not in self.teams[comp.owner_team].members:
                raise KBError(
                    f"component {comp.name}: default assignee {comp.default_assignee} "
                    f"is not a member of {comp.owner_team}"
                )
        for team in self.teams.values():
            for cname in team.components:
                owned = self.components.get(cname)
                if owned is None or owned.owner_team != team.name:
                    raise KBError(f"team {team.name} lists component {cname} it does not own")
        for ki in self.known_issues.values():
            if ki.component not in self.components:
                raise KBError(f"known issue {ki.id}: unknown component {ki.component}")
        for uc in self.use_cases:
            for cname in uc.components:
                if cname not in self.components:
                    raise KBError(f"use case {uc.name}: unknown component {cname}")
        self._validate_history()

    def _validate_history(self) -> None:
        seen: set[str] = set()
        for bug in self.history:
            if bug.id in seen:
                raise KBError(f"duplicate history id {bug.id}")
            comp = self.components.get(bug.component)
            if comp is None:
                raise KBError(f"{bug.id}: unknown component {bug.component}")
            if bug.team != comp.owner_team:
                raise KBError(f"{bug.id}: team {bug.team} does not own {bug.component}")
            if bug.assignee not in self.teams[comp.owner_team].members:
                raise KBError(f"{bug.id}: assignee {bug.assignee} not in team {bug.team}")
            if bug.duplicate_of is not None and bug.duplicate_of not in seen:
                raise KBError(f"{bug.id}: duplicate_of {bug.duplicate_of} is not an earlier id")
            if bug.known_issue is not None:
                ki = self.known_issues.get(bug.known_issue)
                if ki is None:
                    raise KBError(f"{bug.id}: unknown known issue {bug.known_issue}")
                if ki.component != bug.component:
                    raise KBError(f"{bug.id}: known issue {ki.id} belongs to {ki.component}")
            seen.add(bug.id)

    def owner_team(self, component: str) -> str:
        """Owner team of a component (KeyError if unknown)."""
        return self.components[component].owner_team

    def default_assignee(self, component: str) -> str:
        """Default assignee of a component (KeyError if unknown)."""
        return self.components[component].default_assignee

    def team_of(self, dev: str) -> str:
        """Team of a developer (KeyError if unknown)."""
        for team in self.teams.values():
            if dev in team.members:
                return team.name
        raise KeyError(dev)

    def is_valid_component(self, name: str) -> bool:
        """True if the component exists."""
        return name in self.components

    def is_valid_assignee(self, name: str) -> bool:
        """True if the developer is a member of any team."""
        return any(name in t.members for t in self.teams.values())

    def history_ids(self) -> set[str]:
        """Ids of all history bugs."""
        return {b.id for b in self.history}

    def roster_text(self) -> str:
        """Compact prompt-ready roster: teams, members, owned components with keywords."""
        lines: list[str] = []
        for team in self.teams.values():
            lines.append(f"Team {team.name}: members {', '.join(team.members)}")
            for cname in team.components:
                comp = self.components[cname]
                lines.append(
                    f"  - {comp.name} (default assignee {comp.default_assignee}; "
                    f"keywords: {', '.join(comp.keywords)})"
                )
        return "\n".join(lines)


def load_eval(data_dir: Path | None = None) -> list[LabeledBug]:
    """Load the held-out evaluation set (eval.jsonl)."""
    return _read_jsonl(_resolve_dir(data_dir) / "eval.jsonl")

"""Pydantic models for parsing schedules.json."""

from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class RotationEntry(BaseModel):
    """One sprint entry from rotation_schedule."""

    model_config = ConfigDict(extra="ignore")

    champion: str
    dr: date
    prod: date
    # Optional: the CoreGateway ambassador table has no go/no-go column, so
    # Core-train entries carry dr + prod only. Parsed for completeness, unused
    # by cadence/rendering.
    go_nogo: date | None = None
    release_title: str | None = None


class SprintWindow(BaseModel):
    """Explicit sprint window (overrides DR-14 heuristic when present)."""

    model_config = ConfigDict(extra="ignore")

    start: date
    end: date


class Schedules(BaseModel):
    """Top-level schedules.json contents."""

    model_config = ConfigDict(extra="ignore")

    team_members: dict[str, str] = Field(default_factory=dict)
    rotation_schedule: dict[str, RotationEntry]
    dod_schedule: dict[date, str] = Field(default_factory=dict)
    sprints: dict[str, SprintWindow] = Field(default_factory=dict)

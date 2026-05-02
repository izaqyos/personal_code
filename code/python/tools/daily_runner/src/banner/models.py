"""Pydantic models for parsing schedules.json."""

from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class RotationEntry(BaseModel):
    """One sprint entry from rotation_schedule."""

    model_config = ConfigDict(extra="ignore")

    champion: str
    dr: date
    go_nogo: date
    prod: date
    release_title: str | None = None


class Schedules(BaseModel):
    """Top-level schedules.json contents."""

    model_config = ConfigDict(extra="ignore")

    team_members: dict[str, str] = Field(default_factory=dict)
    rotation_schedule: dict[str, RotationEntry]
    dod_schedule: dict[date, str] = Field(default_factory=dict)

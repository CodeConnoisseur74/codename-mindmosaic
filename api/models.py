from datetime import datetime
from uuid import UUID

from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Column, Field, SQLModel


class StudyPlanInput(SQLModel):
    goals: str
    days: int
    time_per_day: int
    preferred_topics: list[str]


class Activity(SQLModel):
    time_minutes: int
    activity: str


class WeekPlan(SQLModel):
    day: int
    activities: list[Activity]


class StudyPlanOutput(SQLModel):
    study_plan: list[WeekPlan]


class StudyPlan(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    plan_id: UUID = Field(..., description='UUID of the study plan')
    input_data: dict = Field(
        sa_column=Column(JSONB), description='Input data for the study plan'
    )  # Use Column(JSONB) for proper PostgreSQL JSONB support
    study_plan: dict = Field(
        sa_column=Column(JSONB), description='Generated study plan'
    )
    created_at: datetime | None = Field(default_factory=datetime.utcnow)

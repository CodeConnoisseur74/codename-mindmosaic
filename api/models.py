from sqlmodel import SQLModel, Field
from typing import List, Optional


class StudyPlanBase(SQLModel):
    goals: str
    time_per_day: int
    preferred_topics: List[str]


class StudyPlan(StudyPlanBase, table=True):
    plan_id: Optional[int] = Field(default=None, primary_key=True)

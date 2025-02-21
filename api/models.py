from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Column, Field, Relationship, SQLModel


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
    plan_id: UUID
    input_data: dict = Field(
        sa_column=Column(JSONB), description='Input data for the study plan'
    )
    study_plan: dict = Field(
        sa_column=Column(JSONB), description='Generated study plan'
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: Optional[int] = Field(default=None, foreign_key='user.id')

    # Define the link back to User
    user: 'User' = Relationship(back_populates='study_plans')


class UserCreate(BaseModel):
    username: str
    full_name: Optional[str] = None
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    full_name: Optional[str] = None
    email: EmailStr

    class Config:
        from_attributes = True


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    full_name: Optional[str] = None
    email: Optional[str] = None
    hashed_password: str

    # Define a list of StudyPlans
    study_plans: List[StudyPlan] = Relationship(back_populates='user')


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None

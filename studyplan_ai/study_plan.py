import uuid

import marvin
from pydantic import BaseModel, Field


class StudyPlanInput(BaseModel):
    goals: str = Field(..., description='The goals for the study plan')
    time_per_day: int = Field(..., description='Time allocated per day for study')
    preferred_topics: list[str] = Field(..., description='Topics preferred for study')


class StudyPlanOutput(BaseModel):
    plan_id: str = Field(..., description='The unique identifier for the study plan')
    goals: str
    time_per_day: int
    preferred_topics: list[str]


@marvin.fn
def create_study_plan(input_data: StudyPlanInput) -> StudyPlanOutput:
    """Generate a study plan with daily activities based on the provided input
    data.

    Input:
    - `goals`: A single specific goal for the study plan
    (e.g., "Learn Python OOP concepts").
    - `time_per_day`: The total study time available per day in minutes (e.g., 60).
    - `preferred_topics`: A list of topics preferred for study
    (e.g., ["Python", "OOP"]).

    Output:
    Returns a dictionary where each key is a day (e.g., 1, 2, 3)
    and the value is a list of activities for that day.
    Each activity is a dictionary containing:
    - `time_minutes`: Time allocated to the activity in minutes
    (ensures daily total does not exceed `time_per_day`).
    - `activity`: A description of the activity (e.g., "Read OOP theory").

    Ensure:
    - Activities are diverse and derived from `preferred_topics`.
    - The total time for activities in each day does not exceed `time_per_day`.
    - Output is concise and actionable, avoiding redundant information.

    Example output:
    {
        1: [
            {"time_minutes": 20, "activity": "Read OOP theory"},
            {"time_minutes": 40, "activity": "Practice coding"},
        ],
        2: [
            {"time_minutes": 30, "activity": "Review OOP patterns"},
            {"time_minutes": 30, "activity": "Work on a small project"},
        ],
        3: [
            {"time_minutes": 20, "activity": "Watch an OOP tutorial"},
            {"time_minutes": 40, "activity": "Apply concepts to a coding challenge"},
        ]
    }
    """
    plan_id = str(uuid.uuid4())
    return StudyPlanOutput(
        plan_id=plan_id,
        goals=input_data.goals,
        time_per_day=input_data.time_per_day,
        preferred_topics=input_data.preferred_topics,
    )

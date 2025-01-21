import marvin
from pydantic import BaseModel, Field


class StudyPlanInput(BaseModel):
    goals: str = Field(..., description="The goals for the study plan")
    days: int = Field(..., description="Number of days to generate the study plan for")
    time_per_day: int = Field(..., description="Time allocated per day for study")
    preferred_topics: list[str] = Field(..., description="Topics preferred for study")


class Activity(BaseModel):
    time_minutes: int = Field(
        ..., description="Time allocated to the activity in minutes"
    )
    activity: str = Field(..., description="Description of the activity")


class WeekPlan(BaseModel):
    day: int = Field(..., description="Day of the week")
    activities: list[Activity] = Field(
        ..., description="List of activities for the day"
    )


class StudyPlanOutput(BaseModel):
    study_plan: list[WeekPlan] = Field(
        ..., description="List of activities for each day of the week"
    )


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
    - List of week days, where each day has one or more activities depending on
    time effort per day.

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


if __name__ == "__main__":
    plan = create_study_plan(
        StudyPlanInput(
            goals="Learn Python OOP concepts",
            days=7,
            time_per_day=60,
            preferred_topics=["Python", "OOP"],
        )
    )
    for week_day in plan.study_plan:
        print(f"Day {week_day.day}:")
        for activity in week_day.activities:
            print(f" - {activity.activity} ({activity.time_minutes} minutes)")
        print()

from pydantic import BaseModel, Field
import marvin
import uuid


class StudyPlanInput(BaseModel):
    goals: str = Field(..., description="The goals for the study plan")
    time_per_day: int = Field(..., description="Time allocated per day for study")
    preferred_topics: list[str] = Field(..., description="Topics preferred for study")


class StudyPlanOutput(BaseModel):
    plan_id: str = Field(..., description="The unique identifier for the study plan")
    goals: str
    time_per_day: int
    preferred_topics: list[str]


@marvin.fn
def create_study_plan(input_data: StudyPlanInput) -> StudyPlanOutput:
    """
    Generates a structured study plan based on the input goals, time, and topics.
    The function will ensure output is suitable for database storage.
    """
    # Implement the logic to create a study plan
    plan_id = str(uuid.uuid4())
    return StudyPlanOutput(
        plan_id=plan_id,
        goals=input_data.goals,
        time_per_day=input_data.time_per_day,
        preferred_topics=input_data.preferred_topics,
    )

from dotenv import load_dotenv
import os
import marvin

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from studyplan_ai.study_plan import (
    create_study_plan,
)


# Load environment variables from .env file
load_dotenv()

# Access the API key
openai_api_key = os.getenv("MARVIN_OPENAI_API_KEY")
marvin.settings.openai.api_key = openai_api_key

app = FastAPI()

# Database mockup (replace with actual database in production)
study_plans: dict[str, "StudyPlan"] = {}


# Base model for shared fields
class StudyPlanBase(BaseModel):
    goals: str
    time_per_day: int
    preferred_topics: list[str]


# Input schema for creating a plan
class StudyPlanInput(StudyPlanBase):
    pass  # No additional fields for input


# Output schema and internal storage representation
class StudyPlan(StudyPlanBase):
    id: str  # Add unique identifier for the output


@app.post("/create_study_plan", response_model=StudyPlan)
async def create_study_plan_endpoint(plan: StudyPlanInput) -> StudyPlan:
    # Delegate the creation logic to another function
    study_plan = create_study_plan(plan)
    study_plans[study_plan.id] = study_plan
    return study_plan


@app.get("/get_study_plan/{plan_id}", response_model=StudyPlan)
async def get_study_plan(plan_id: str) -> StudyPlan:
    if plan_id not in study_plans:
        raise HTTPException(status_code=404, detail="Study plan not found.")
    return study_plans[plan_id]

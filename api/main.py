import os

import marvin
import json
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session
from .db import init_db, get_session
from .models import StudyPlan
from pydantic import BaseModel

# Load environment variables from .env file
load_dotenv()

# Access the API key
openai_api_key = os.getenv('MARVIN_OPENAI_API_KEY')
marvin.settings.openai.api_key = openai_api_key

app = FastAPI()

# Initialise the database
init_db()

# Database mockup (replace with actual database in production)
study_plans: dict[str, 'StudyPlan'] = {}


# Base model for shared fields
class StudyPlanBase(BaseModel):
    goals: str
    time_per_day: int
    preferred_topics: list[str]


# Input schema for creating a plan
class StudyPlanInput(StudyPlanBase):
    pass  # No additional fields for input


@app.post('/create_study_plan', response_model=StudyPlan)
async def create_study_plan_endpoint(
    plan: StudyPlanInput, session: Session = Depends(get_session)
) -> StudyPlan:
    db_study_plan = StudyPlan(
        goals=plan.goals,
        time_per_day=plan.time_per_day,
        preferred_topics=json.dumps(
            plan.preferred_topics
        ),  # Convert list to JSON string
    )
    session.add(db_study_plan)
    session.commit()
    session.refresh(db_study_plan)
    # Convert JSON string back to list when returning
    db_study_plan.preferred_topics = json.loads(db_study_plan.preferred_topics)
    return db_study_plan


@app.get('/get_study_plan/{plan_id}', response_model=StudyPlan)
async def get_study_plan(
    plan_id: int, session: Session = Depends(get_session)
) -> StudyPlan:
    study_plan = session.get(StudyPlan, plan_id)
    if not study_plan:
        raise HTTPException(status_code=404, detail='Study plan not found.')
    return study_plan

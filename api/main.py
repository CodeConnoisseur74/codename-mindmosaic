from contextlib import asynccontextmanager
from uuid import UUID

import marvin
from decouple import config
from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session

from .ai import create_study_plan
from .db import get_session, init_db, save_study_plan
from .db import get_study_plan as get_study_plan_db
from .models import StudyPlan, StudyPlanInput

openai_api_key = config('MARVIN_OPENAI_API_KEY')
marvin.settings.openai.api_key = openai_api_key


@asynccontextmanager
async def lifespan(app):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.post('/create_study_plan', response_model=StudyPlan)
async def create_study_plan_endpoint(
    plan: StudyPlanInput, session: Session = Depends(get_session)
) -> StudyPlan:
    output_plan = create_study_plan(plan)
    db_study_plan = save_study_plan(plan, output_plan)
    return db_study_plan


@app.get('/get_study_plan/{plan_id}', response_model=StudyPlan)
async def get_study_plan(
    plan_id: UUID, session: Session = Depends(get_session)
) -> StudyPlan:
    study_plan = get_study_plan_db(plan_id)
    if study_plan is None:
        raise HTTPException(status_code=404, detail='Study plan not found.')
    return study_plan

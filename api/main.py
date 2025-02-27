from contextlib import asynccontextmanager
from datetime import timedelta
from uuid import UUID

import marvin
from decouple import config
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlmodel import Session

from .ai import create_study_plan
from .auth import authenticate_user, create_access_token, get_current_user
from .db import get_session, init_db, save_study_plan
from .db import get_study_plan as get_study_plan_db
from .db import get_study_plans as get_study_plans_db
from .models import StudyPlan, StudyPlanInput, Token, User, UserCreate, UserResponse

# Load secret settings
openai_api_key = config('MARVIN_OPENAI_API_KEY')
marvin.settings.openai.api_key = openai_api_key

ACCESS_TOKEN_EXPIRE_MINUTES = 30


@asynccontextmanager
async def lifespan(app):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


@app.post('/register/', response_model=UserResponse)
async def register_user(user: UserCreate, session: Session = Depends(get_session)):
    db_user = session.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail='Username already registered')

    hashed_password = pwd_context.hash(user.password)
    db_user = User(
        username=user.username,
        hashed_password=hashed_password,
        full_name=user.full_name,
        email=user.email,
    )

    session.add(db_user)
    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail='Internal Server Error') from e
    session.refresh(db_user)
    return db_user


@app.post(
    '/create_study_plan',
    response_model=StudyPlan,
)
async def create_study_plan_endpoint(
    plan: StudyPlanInput,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> StudyPlan:
    output_plan = create_study_plan(plan)
    db_study_plan = save_study_plan(plan, output_plan, current_user.id)
    return db_study_plan


@app.get(
    '/get_study_plan/{plan_id}',
    response_model=StudyPlan,
    dependencies=[Depends(get_current_user)],
)
async def get_study_plan(
    plan_id: UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> StudyPlan:
    study_plan = get_study_plan_db(plan_id, current_user.id)
    if study_plan is None:
        raise HTTPException(
            status_code=404, detail='Study plan not found or not authorised to access.'
        )
    return study_plan


@app.get(
    '/get_study_plans',
    response_model=list[
        dict
    ],  # Return a list of dictionaries instead of raw DB objects
    dependencies=[Depends(get_current_user)],
)
async def get_study_plans(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> list[dict]:
    study_plans = get_study_plans_db(current_user.id)

    if not study_plans:
        return []  # Return empty list instead of 404

    return [
        {
            'plan_id': str(sp.plan_id),
            'created_at': sp.created_at,
            'input_data': sp.input_data,
            'study_plan': sp.study_plan,
        }
        for sp in study_plans
    ]


@app.post('/token', response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': user.username}, expires_delta=access_token_expires
    )
    return {'access_token': access_token, 'token_type': 'bearer'}


@app.delete('/delete_study_plan/{plan_id}')
async def delete_study_plan(
    plan_id: UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """
    Delete a study plan if it belongs to the current user.
    """
    study_plan = (
        session.query(StudyPlan)
        .filter(StudyPlan.plan_id == plan_id, StudyPlan.user_id == current_user.id)
        .first()
    )

    if not study_plan:
        raise HTTPException(
            status_code=404, detail='Study plan not found or unauthorized to delete.'
        )

    session.delete(study_plan)
    session.commit()

    return {'message': 'Study plan deleted successfully'}

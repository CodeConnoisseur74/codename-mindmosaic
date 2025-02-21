import uuid

from decouple import config
from sqlmodel import Session, SQLModel, and_, create_engine, select

from .ai import StudyPlanInput, StudyPlanOutput
from .models import StudyPlan, User

DATABASE_URL = config('DATABASE_URL')

engine = create_engine(DATABASE_URL)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


def get_user(username: str) -> User | None:
    with Session(engine) as session:
        statement = select(User).where(User.username == username)
        result = session.exec(statement).first()
        return result


def save_study_plan(
    input_data: StudyPlanInput, output_data: StudyPlanOutput, user_id: int
) -> StudyPlan:
    with Session(engine) as session:
        user = session.get(User, user_id)
        study_plan = StudyPlan(
            plan_id=uuid.uuid4(),
            input_data=input_data.dict(),
            study_plan=output_data.dict(),
            user=user,
        )
        session.add(study_plan)
        session.commit()
        session.refresh(study_plan)
        return study_plan


def get_study_plan(plan_id: uuid.UUID, user_id: int) -> StudyPlan | None:
    with Session(engine) as session:
        statement = select(StudyPlan).where(
            and_(StudyPlan.plan_id == plan_id, StudyPlan.user_id == user_id)
        )
        result = session.exec(statement).first()
        return result

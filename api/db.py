import uuid

from decouple import config
from sqlmodel import Session, SQLModel, create_engine, select

from .ai import StudyPlanInput, StudyPlanOutput
from .models import StudyPlan

DATABASE_URL = config('DATABASE_URL')

engine = create_engine(DATABASE_URL)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


def save_study_plan(
    input_data: StudyPlanInput, output_data: StudyPlanOutput
) -> StudyPlan:
    with Session(engine) as session:
        study_plan = StudyPlan(
            plan_id=uuid.uuid4(),
            input_data=input_data.dict(),
            study_plan=output_data.dict(),
        )
        session.add(study_plan)
        session.commit()
        session.refresh(study_plan)
        return study_plan


def get_study_plan(plan_id: uuid.UUID) -> StudyPlan | None:
    with Session(engine) as session:
        statement = select(StudyPlan).where(StudyPlan.plan_id == plan_id)
        result = session.exec(statement).first()
        return result

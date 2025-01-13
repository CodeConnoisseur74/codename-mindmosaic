from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Database mockup (replace with actual database in production)
study_plans = {}


# Define input schema
class StudyPlanInput(BaseModel):
    user_id: int
    goals: str
    time_per_day: int
    preferred_topics: list


@app.post("/create_study_plan")
async def create_study_plan(plan: StudyPlanInput):
    # Simulate saving to a database
    study_plans[plan.user_id] = {
        "goals": plan.goals,
        "time_per_day": plan.time_per_day,
        "preferred_topics": plan.preferred_topics,
    }
    return {
        "message": "Study plan created successfully.",
        "plan": study_plans[plan.user_id],
    }


@app.get("/get_study_plan/{user_id}")
async def get_study_plan(user_id: int):
    # Fetch study plan from "database"
    if user_id in study_plans:
        return {"user_id": user_id, "study_plan": study_plans[user_id]}
    else:
        raise HTTPException(status_code=404, detail="Study plan not found.")

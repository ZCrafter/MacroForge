from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..deps import get_db, get_current_user
from ..models import Goal
from ..schemas import GoalIn
from ..services.goals import calculate_goals

router = APIRouter(prefix="/goals", tags=["goals"])

@router.get("")
def list_goals(_: str = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Goal).order_by(Goal.nutrient.asc()).all()

@router.post("")
def upsert_goal(data: GoalIn, _: str = Depends(get_current_user), db: Session = Depends(get_db)):
    goal = db.query(Goal).filter(Goal.nutrient == data.nutrient).first()
    if not goal:
        goal = Goal(**data.model_dump())
        db.add(goal)
    else:
        for k, v in data.model_dump().items():
            setattr(goal, k, v)
    db.commit()
    return {"ok": True}

@router.post("/calculate")
def calc_goals(profile: dict, _: str = Depends(get_current_user), db: Session = Depends(get_db)):
    goals = calculate_goals(profile)
    for g in goals:
        goal = db.query(Goal).filter(Goal.nutrient == g['nutrient']).first()
        if not goal:
            goal = Goal(**g)
            db.add(goal)
        else:
            for k, v in g.items():
                setattr(goal, k, v)
    db.commit()
    return goals

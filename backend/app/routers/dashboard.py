from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..deps import get_db, get_current_user
from ..models import Meal, MealPlan
from ..routers.meals import calc_meal

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("")
def dashboard(_: str = Depends(get_current_user), db: Session = Depends(get_db)):
    meals = db.query(Meal).all()
    output = []
    totals = {"calories": 0, "protein_g": 0, "carbs_g": 0, "fat_g": 0, "fiber_g": 0, "sugar_g": 0, "sodium_mg": 0, "price": 0}
    for meal in meals:
        plan = db.query(MealPlan).filter(MealPlan.meal_id == meal.id).first()
        per_meal = calc_meal(meal, db)
        servings = plan.servings_per_week if plan else 0
        weekly = {k: v * servings for k, v in per_meal.items()}
        for k in totals:
            totals[k] += weekly[k]
        output.append({"meal_id": meal.id, "name": meal.name, "servings_per_week": servings, "per_meal": per_meal, "weekly": weekly})
    return {"meals": output, "totals": totals}

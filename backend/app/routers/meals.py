from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..deps import get_db, get_current_user
from ..models import Meal, MealItem, MealPlan, Ingredient
from ..schemas import MealIn, MealOut, MealItemIn, MealPlanIn

router = APIRouter(prefix="/meals", tags=["meals"])

def calc_meal(meal: Meal, db: Session):
    items = db.query(MealItem).filter(MealItem.meal_id == meal.id).all()
    totals = {"calories": 0, "protein_g": 0, "carbs_g": 0, "fat_g": 0, "fiber_g": 0, "sugar_g": 0, "sodium_mg": 0, "price": 0}
    for item in items:
        ing = db.query(Ingredient).get(item.ingredient_id)
        factor = item.amount / max(ing.quantity, 1e-9)
        for k in totals:
            totals[k] += getattr(ing, k, 0) * factor
    return totals

@router.get("")
def list_meals(_: str = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Meal).order_by(Meal.name.asc()).all()

@router.post("", response_model=MealOut)
def create_meal(data: MealIn, _: str = Depends(get_current_user), db: Session = Depends(get_db)):
    item = Meal(**data.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.post("/item")
def add_item(data: MealItemIn, _: str = Depends(get_current_user), db: Session = Depends(get_db)):
    item = MealItem(**data.model_dump())
    db.add(item)
    db.commit()
    return {"ok": True}

@router.post("/plan")
def set_plan(data: MealPlanIn, _: str = Depends(get_current_user), db: Session = Depends(get_db)):
    plan = db.query(MealPlan).filter(MealPlan.meal_id == data.meal_id).first()
    if not plan:
        plan = MealPlan(meal_id=data.meal_id, servings_per_week=data.servings_per_week)
        db.add(plan)
    else:
        plan.servings_per_week = data.servings_per_week
    db.commit()
    return {"ok": True}

@router.get("/{meal_id}/calc")
def meal_calc(meal_id: int, _: str = Depends(get_current_user), db: Session = Depends(get_db)):
    meal = db.query(Meal).get(meal_id)
    plan = db.query(MealPlan).filter(MealPlan.meal_id == meal_id).first()
    per_meal = calc_meal(meal, db)
    weekly = {k: v * (plan.servings_per_week if plan else 0) for k, v in per_meal.items()}
    return {"meal": meal.name, "per_meal": per_meal, "weekly": weekly, "servings_per_week": plan.servings_per_week if plan else 0}

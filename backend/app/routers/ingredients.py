from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..deps import get_db, get_current_user
from ..models import Ingredient
from ..schemas import IngredientIn, IngredientOut
from ..services.nutrition import search_foods, food_details

router = APIRouter(prefix="/ingredients", tags=["ingredients"])

@router.get("", response_model=list[IngredientOut])
def list_ingredients(_: str = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Ingredient).order_by(Ingredient.name.asc()).all()

@router.post("", response_model=IngredientOut)
def create_ingredient(data: IngredientIn, _: str = Depends(get_current_user), db: Session = Depends(get_db)):
    item = Ingredient(**data.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.put("/{ingredient_id}", response_model=IngredientOut)
def update_ingredient(ingredient_id: int, data: IngredientIn, _: str = Depends(get_current_user), db: Session = Depends(get_db)):
    item = db.query(Ingredient).get(ingredient_id)
    for k, v in data.model_dump().items():
        setattr(item, k, v)
    item.manual_overrides = True
    db.commit()
    db.refresh(item)
    return item

@router.delete("/{ingredient_id}")
def delete_ingredient(ingredient_id: int, _: str = Depends(get_current_user), db: Session = Depends(get_db)):
    item = db.query(Ingredient).get(ingredient_id)
    db.delete(item)
    db.commit()
    return {"ok": True}

@router.post("/search")
async def usda_search(query: dict, _: str = Depends(get_current_user)):
    return await search_foods(query.get("query", ""))

@router.post("/import/{fdc_id}")
async def usda_import(fdc_id: int, _: str = Depends(get_current_user), db: Session = Depends(get_db)):
    data = await food_details(fdc_id)
    ing = Ingredient(
        name=data.get("description", f"FDC {fdc_id}"),
        category="imported",
        source="usda",
        source_fdc_id=str(fdc_id),
        manual_overrides=False,
    )
    db.add(ing)
    db.commit()
    db.refresh(ing)
    return ing

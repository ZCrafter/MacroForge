from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..deps import get_db, get_current_user
from ..models import Ingredient
from ..schemas import IngredientIn, IngredientOut
from ..services.nutrition import search_foods, food_details

router = APIRouter(prefix="/ingredients", tags=["ingredients"])

def to_output(ing: Ingredient):
    return ing

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
    if not item:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    for k, v in data.model_dump().items():
        setattr(item, k, v)
    item.manual_overrides = True
    db.commit()
    db.refresh(item)
    return item

@router.post("/{ingredient_id}/revert", response_model=IngredientOut)
def revert_ingredient(ingredient_id: int, _: str = Depends(get_current_user), db: Session = Depends(get_db)):
    item = db.query(Ingredient).get(ingredient_id)
    if not item:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    item.manual_overrides = False
    db.commit()
    db.refresh(item)
    return item

@router.delete("/{ingredient_id}")
def delete_ingredient(ingredient_id: int, _: str = Depends(get_current_user), db: Session = Depends(get_db)):
    item = db.query(Ingredient).get(ingredient_id)
    if not item:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    db.delete(item)
    db.commit()
    return {"ok": True}

@router.post("/search")
async def usda_search(query: dict, _: str = Depends(get_current_user)):
    q = query.get("query", "").strip()
    page_size = int(query.get("page_size", 10))
    return await search_foods(q, page_size=page_size)

@router.post("/import/{fdc_id}")
async def usda_import(fdc_id: int, _: str = Depends(get_current_user), db: Session = Depends(get_db)):
    data = await food_details(fdc_id)
    if not data:
        raise HTTPException(status_code=400, detail="USDA import unavailable or empty")

    nutrients = {n.get("nutrient", {}).get("name"): n.get("amount", 0) for n in data.get("foodNutrients", []) if n.get("nutrient")}
    ing = Ingredient(
        name=data.get("description", f"FDC {fdc_id}"),
        category="imported",
        unit="g",
        quantity=100,
        calories=nutrients.get("Energy", 0),
        protein_g=nutrients.get("Protein", 0),
        carbs_g=nutrients.get("Carbohydrate, by difference", 0),
        fat_g=nutrients.get("Total lipid (fat)", 0),
        fiber_g=nutrients.get("Fiber, total dietary", 0),
        sugar_g=nutrients.get("Sugars, total including NLEA", 0),
        sodium_mg=nutrients.get("Sodium, Na", 0),
        price=0,
        source="usda",
        source_fdc_id=str(fdc_id),
        manual_overrides=False,
    )
    db.add(ing)
    db.commit()
    db.refresh(ing)
    return ing

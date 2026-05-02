from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LoginIn(BaseModel):
    username: str
    password: str

class ProfileOut(BaseModel):
    sex: str
    age: int
    height_in: float
    weight_lb: float
    activity_level: str
    calories_goal: float
    calories_goal_manual: bool
    calories_goal_note: str
    class Config:
        from_attributes = True

class ProfileIn(BaseModel):
    sex: str
    age: int
    height_in: float
    weight_lb: float
    activity_level: str
    calories_goal: float | None = None
    calories_goal_manual: bool | None = None
    calories_goal_note: str | None = None

class IngredientIn(BaseModel):
    name: str
    category: str = "general"
    unit: str = "g"
    quantity: float = 100
    calories: float = 0
    protein_g: float = 0
    carbs_g: float = 0
    fat_g: float = 0
    fiber_g: float = 0
    sugar_g: float = 0
    sodium_mg: float = 0
    price: float = 0
    source: str = "manual"
    source_fdc_id: str = ""
    vitamin_a_iu: float = 0
    vitamin_c_mg: float = 0
    vitamin_d_iu: float = 0
    calcium_mg: float = 0
    iron_mg: float = 0
    potassium_mg: float = 0
    magnesium_mg: float = 0

class IngredientOut(IngredientIn):
    id: int
    manual_overrides: bool
    class Config:
        from_attributes = True

class MealIn(BaseModel):
    name: str
    notes: str = ""

class MealOut(MealIn):
    id: int
    class Config:
        from_attributes = True

class MealItemIn(BaseModel):
    meal_id: int
    ingredient_id: int
    amount: float
    unit: str

class MealPlanIn(BaseModel):
    meal_id: int
    servings_per_week: int

class GoalIn(BaseModel):
    nutrient: str
    target_per_day: float
    target_per_week: float
    source: str = "manual"
    explanation: str = ""
    manual_override: bool = False

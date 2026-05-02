from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Text, DateTime, func
from sqlalchemy.orm import relationship
from .db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

class UserProfile(Base):
    __tablename__ = "user_profiles"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    sex = Column(String, default="unspecified")
    age = Column(Integer, default=30)
    height_in = Column(Float, default=70)
    weight_lb = Column(Float, default=180)
    activity_level = Column(String, default="moderate")
    calories_goal = Column(Float, default=2400)
    calories_goal_manual = Column(Boolean, default=False)
    calories_goal_note = Column(Text, default="")
    user = relationship("User")

class Ingredient(Base):
    __tablename__ = "ingredients"
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True, nullable=False)
    category = Column(String, default="general")
    unit = Column(String, default="g")
    quantity = Column(Float, default=100)
    calories = Column(Float, default=0)
    protein_g = Column(Float, default=0)
    carbs_g = Column(Float, default=0)
    fat_g = Column(Float, default=0)
    fiber_g = Column(Float, default=0)
    sugar_g = Column(Float, default=0)
    sodium_mg = Column(Float, default=0)
    vitamin_a_iu = Column(Float, default=0)
    vitamin_c_mg = Column(Float, default=0)
    vitamin_d_iu = Column(Float, default=0)
    calcium_mg = Column(Float, default=0)
    iron_mg = Column(Float, default=0)
    potassium_mg = Column(Float, default=0)
    magnesium_mg = Column(Float, default=0)
    price = Column(Float, default=0)
    source = Column(String, default="manual")
    source_fdc_id = Column(String, default="")
    manual_overrides = Column(Boolean, default=False)

class IngredientNutrient(Base):
    __tablename__ = "ingredient_nutrients"
    id = Column(Integer, primary_key=True)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), nullable=False)
    nutrient_name = Column(String, nullable=False)
    amount = Column(Float, default=0)
    unit = Column(String, default="")
    source_amount = Column(Float, default=0)
    source_unit = Column(String, default="")
    manual_value = Column(Boolean, default=False)

class Meal(Base):
    __tablename__ = "meals"
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True, nullable=False)
    notes = Column(Text, default="")

class MealItem(Base):
    __tablename__ = "meal_items"
    id = Column(Integer, primary_key=True)
    meal_id = Column(Integer, ForeignKey("meals.id"), nullable=False)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), nullable=False)
    amount = Column(Float, default=1)
    unit = Column(String, default="g")

class MealPlan(Base):
    __tablename__ = "meal_plans"
    id = Column(Integer, primary_key=True)
    meal_id = Column(Integer, ForeignKey("meals.id"), nullable=False, unique=True)
    servings_per_week = Column(Integer, default=0)

class Goal(Base):
    __tablename__ = "goals"
    id = Column(Integer, primary_key=True)
    nutrient = Column(String, unique=True, nullable=False)
    target_per_day = Column(Float, default=0)
    target_per_week = Column(Float, default=0)
    source = Column(String, default="manual")
    explanation = Column(Text, default="")
    manual_override = Column(Boolean, default=False)

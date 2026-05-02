from fastapi import FastAPI
from .routers import auth, ingredients, meals, goals, dashboard

app = FastAPI(title="MacroForge API")

app.include_router(auth.router)
app.include_router(ingredients.router)
app.include_router(meals.router)
app.include_router(goals.router)
app.include_router(dashboard.router)

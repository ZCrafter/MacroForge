import httpx
from ..config import settings

USDA_BASE = "https://api.nal.usda.gov/fdc/v1"

async def search_foods(query: str):
    if not settings.usda_api_key:
        return []
    params = {"query": query, "api_key": settings.usda_api_key, "pageSize": 10}
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(f"{USDA_BASE}/foods/search", params=params)
        r.raise_for_status()
        return r.json().get("foods", [])

async def food_details(fdc_id: int):
    if not settings.usda_api_key:
        return {}
    params = {"api_key": settings.usda_api_key}
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(f"{USDA_BASE}/food/{fdc_id}", params=params)
        r.raise_for_status()
        return r.json()

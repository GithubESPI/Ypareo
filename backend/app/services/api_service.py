import httpx
from fastapi import HTTPException

async def fetch_api_data(url: str, headers: dict):
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, timeout=60.0)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Erreur lors de l'appel API")
        return response.json()

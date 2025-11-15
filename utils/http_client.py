from fastapi import HTTPException
import httpx

async def request(method: str, url: str, json: dict = None, headers: dict = None):
    try:
        timeout_config = httpx.Timeout(120.0, connect=30.0, read=120.0, write=120.0, pool=5.0)
        async with httpx.AsyncClient(timeout=timeout_config) as client:
            response = await client.request(method, url, json=json, headers=headers)
            response.raise_for_status()
            return response.json()
    except httpx.RequestError:
        raise HTTPException(status_code=500, detail="Error connecting to the service")
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)

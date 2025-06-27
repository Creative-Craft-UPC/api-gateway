import httpx

async def request(method: str, url: str, json: dict = None):
    timeout_config = httpx.Timeout(120.0, connect=30.0, read=120.0, write=120.0, pool=5.0)
    async with httpx.AsyncClient(timeout=timeout_config) as client:
        response = await client.request(method, url, json=json)
        response.raise_for_status()
        return response.json()

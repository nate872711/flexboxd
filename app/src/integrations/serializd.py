import httpx
from rich import print


class SerializdClient:
    BASE = "https://api.serializd.com"

    def __init__(self, api_key):
        self.api_key = api_key

    async def get_activity(self):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        url = f"{self.BASE}/v1/activity"

        try:
            async with httpx.AsyncClient() as client:
                r = await client.get(url, headers=headers)
                return r.json()
        except Exception as e:
            print(f"[red]Serializd error: {e}")
            return {}

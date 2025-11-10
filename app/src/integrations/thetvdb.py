import httpx
from rich import print

class TheTVDBClient:
    def __init__(self, api_key: str, pin: str):
        self.api_key = api_key
        self.pin = pin
        self.token = None
        self.base = "https://api4.thetvdb.com/v4"

    async def authenticate(self):
        """Authenticate using API key + PIN → store JWT"""
        url = f"{self.base}/login"
        payload = {
            "apikey": self.api_key,
            "pin": self.pin
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload)
            if response.status_code != 200:
                print(f"[red]TheTVDB auth failed: {response.text}")
                return None
            
            self.token = response.json().get("data", {}).get("token")
            print("[green]TheTVDB authentication successful!")
            return self.token

    async def _get(self, endpoint: str):
        """Internal helper for authenticated GET requests"""
        headers = {"Authorization": f"Bearer {self.token}"}
        url = f"{self.base}{endpoint}"

        async with httpx.AsyncClient() as client:
            return await client.get(url, headers=headers)

    async def get_series(self, tvdb_id: int):
        """Retrieve series metadata"""
        response = await self._get(f"/series/{tvdb_id}")
        return response.json()

    async def search(self, query: str):
        """Search TVDB for series/episodes"""
        response = await self._get(f"/search?query={query}")
        return response.json()

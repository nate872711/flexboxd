import httpx
from rich import print


class MusicboardClient:
    BASE = "https://api.musicboard.app/v1"

    def __init__(self, username, api_key):
        self.username = username
        self.api_key = api_key

    async def get_profile(self):
        url = f"{self.BASE}/users/{self.username}"

        try:
            async with httpx.AsyncClient() as client:
                r = await client.get(url)
                return r.json()
        except Exception as e:
            print(f"[red]Musicboard error: {e}")
            return {}

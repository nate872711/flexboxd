import logging
import httpx

log = logging.getLogger("musicboard")

class MusicboardClient:
    BASE = "https://api.musicboard.app/v1"

    def __init__(self, username: str, api_key: str):
        self.username = username
        self.api_key = api_key

    async def get_profile(self):
        url = f"{self.BASE}/users/{self.username}"
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                r = await client.get(url, headers={"Authorization": f"Bearer {self.api_key}"})
                r.raise_for_status()
                return r.json()
        except Exception as e:
            log.exception(f"Musicboard error: {e}")
            return {}

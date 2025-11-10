import httpx
from bs4 import BeautifulSoup
from rich import print


class LetterboxdClient:
    BASE = "https://letterboxd.com"

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.client = httpx.AsyncClient()

    async def get_watched(self):
        """Scrape watched films (Letterboxd has no official API)."""
        url = f"{self.BASE}/{self.username}/films/diary/"

        try:
            r = await self.client.get(url)
            soup = BeautifulSoup(r.text, "lxml")

            films = [tag.get("data-film-slug") for tag in soup.select("li.diary-entry-row")]
            return films
            
        except Exception as e:
            print(f"[red]Letterboxd scrape error: {e}")
            return []

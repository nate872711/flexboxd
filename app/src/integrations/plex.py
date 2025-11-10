from plexapi.server import PlexServer
from rich import print


class PlexClient:
    def __init__(self, server_url: str, token: str, username: str = ""):
        self.server_url = server_url
        self.token = token
        self.username = username
        self.plex = None

        try:
            self.plex = PlexServer(self.server_url, self.token)
            print("[green]Connected to Plex Server")
        except Exception as e:
            print(f"[red]Failed to connect to Plex: {e}")

    def get_watched(self):
        """Get all watched media from Plex."""
        try:
            history = self.plex.history()
            return history
        except Exception as e:
            print(f"[red]Plex watched history error: {e}")
            return []

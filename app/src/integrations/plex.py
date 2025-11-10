import logging
from plexapi.server import PlexServer

log = logging.getLogger("plex")

class PlexClient:
    def __init__(self, server_url: str, token: str, username: str = ""):
        self.server_url = server_url
        self.token = token
        self.username = username
        self.plex = None

        try:
            self.plex = PlexServer(self.server_url, self.token)
            log.info("Connected to Plex Server")
        except Exception as e:
            log.exception(f"Failed to connect to Plex: {e}")

    def get_watched(self):
        """Return Plex watch history (list of Video objects)."""
        if not self.plex:
            log.warning("Plex client not initialized")
            return []
        try:
            return self.plex.history() or []
        except Exception as e:
            log.exception(f"Plex history error: {e}")
            return []

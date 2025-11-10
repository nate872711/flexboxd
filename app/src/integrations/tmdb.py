import logging
import tmdbsimple as tmdb

log = logging.getLogger("tmdb")

class TMDbClient:
    def __init__(self, api_key: str):
        tmdb.API_KEY = api_key
        log.info("TMDb client initialized")

    def search_movie(self, query: str):
        try:
            s = tmdb.Search()
            result = s.movie(query=query) or {}
            return result.get("results", [])
        except Exception as e:
            log.exception(f"TMDb search error: {e}")
            return []

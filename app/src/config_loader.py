import os
import yaml
import logging
from pathlib import Path

log = logging.getLogger("config")


CONFIG_PATH = Path("/config/config.yml")


def load_config():
    """
    Loads config.yml if it exists.
    Otherwise returns None so main.py can trigger auto-generation.
    """
    if CONFIG_PATH.exists():
        log.info("📄 Loading config.yml...")
        with open(CONFIG_PATH, "r") as f:
            return yaml.safe_load(f)
    else:
        log.warning("⚠️ config.yml not found — will attempt auto-generation from environment variables")
        return None


def generate_config_from_env():
    """
    Creates config.yml based entirely on docker-compose.yml environment variables.
    """
    config = {
        "general": {
            "log_level": os.getenv("LOG_LEVEL", "INFO"),
            "sync_interval_minutes": int(os.getenv("SYNC_INTERVAL_MINUTES", 30)),
            "sync_direction": os.getenv("SYNC_DIRECTION", "plex->trakt,letterboxd,imdb"),
        },

        "plex": {
            "enabled": os.getenv("PLEX_ENABLED", "false").lower() == "true",
            "server_url": os.getenv("PLEX_SERVER_URL", ""),
            "token": os.getenv("PLEX_TOKEN", ""),
            "username": os.getenv("PLEX_USERNAME", "")
        },

        "tautulli": {
            "enabled": os.getenv("TAUTULLI_ENABLED", "false").lower() == "true",
            "api_url": os.getenv("TAUTULLI_API_URL", ""),
            "api_key": os.getenv("TAUTULLI_API_KEY", "")
        },

        "trakt": {
            "enabled": os.getenv("TRAKT_ENABLED", "false").lower() == "true",
            "client_id": os.getenv("TRAKT_CLIENT_ID", ""),
            "client_secret": os.getenv("TRAKT_CLIENT_SECRET", ""),
            "access_token": os.getenv("TRAKT_ACCESS_TOKEN", ""),
            "refresh_token": os.getenv("TRAKT_REFRESH_TOKEN", "")
        },

        "letterboxd": {
            "enabled": os.getenv("LETTERBOXD_ENABLED", "false").lower() == "true",
            "username": os.getenv("LETTERBOXD_USERNAME", ""),
            "password": os.getenv("LETTERBOXD_PASSWORD", "")
        },

        "imdb": {
            "enabled": os.getenv("IMDB_ENABLED", "false").lower() == "true",
            "csv_path": os.getenv("IMDB_CSV_PATH", "/config/imdb_ratings.csv")
        },

        "tvdb": {
            "enabled": os.getenv("TVDB_ENABLED", "false").lower() == "true",
            "api_key": os.getenv("TVDB_API_KEY", ""),
            "pin": os.getenv("TVDB_PIN", "")
        },

        "serializd": {
            "enabled": os.getenv("SERIALIZD_ENABLED", "false").lower() == "true",
            "api_key": os.getenv("SERIALIZD_API_KEY", "")
        },

        "musicboard": {
            "enabled": os.getenv("MUSICBOARD_ENABLED", "false").lower() == "true",
            "username": os.getenv("MUSICBOARD_USERNAME", ""),
            "api_key": os.getenv("MUSICBOARD_API_KEY", "")
        },

        "tmdb": {
            "enabled": os.getenv("TMDB_ENABLED", "false").lower() == "true",
            "api_key": os.getenv("TMDB_API_KEY", "")
        },

        "custom_lists": {
            "enabled": os.getenv("CUSTOM_LISTS_ENABLED", "false").lower() == "true",
        }
    }

    # Save config file
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        yaml.safe_dump(config, f, sort_keys=False)

    log.info("🆕 Generated new config.yml from environment variables")
    return config

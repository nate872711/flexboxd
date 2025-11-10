import os
import yaml
import logging
from pathlib import Path

log = logging.getLogger("config")
CONFIG_PATH = Path("/config/config.yml")

def _env_bool(name: str, default: bool = False) -> bool:
    return os.getenv(name, str(default)).strip().lower() in {"1","true","yes","on"}

def load_config():
    """Load /config/config.yml if present; otherwise return None."""
    if CONFIG_PATH.exists():
        log.info("📄 Loading config.yml...")
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    log.warning("⚠️ config.yml not found — will generate from environment variables")
    return None

def generate_config_from_env():
    """Create config.yml from environment variables (for Docker-first setup)."""
    cfg = {
        "general": {
            "log_level": os.getenv("LOG_LEVEL", "INFO"),
            "sync_interval_minutes": int(os.getenv("SYNC_INTERVAL_MINUTES", "30")),
            # Comma-separated destinations. Example: "plex->trakt,letterboxd,imdb"
            "sync_direction": os.getenv("SYNC_DIRECTION", "plex->trakt,letterboxd,imdb"),
        },

        "plex": {
            "enabled": _env_bool("PLEX_ENABLED", True),
            "server_url": os.getenv("PLEX_SERVER_URL", ""),
            "token": os.getenv("PLEX_TOKEN", ""),
            "username": os.getenv("PLEX_USERNAME", ""),
        },

        "tautulli": {
            "enabled": _env_bool("TAUTULLI_ENABLED", False),
            "api_url": os.getenv("TAUTULLI_API_URL", ""),
            "api_key": os.getenv("TAUTULLI_API_KEY", ""),
        },

        "trakt": {
            "enabled": _env_bool("TRAKT_ENABLED", True),
            "client_id": os.getenv("TRAKT_CLIENT_ID", ""),
            "client_secret": os.getenv("TRAKT_CLIENT_SECRET", ""),
            "access_token": os.getenv("TRAKT_ACCESS_TOKEN", ""),
            "refresh_token": os.getenv("TRAKT_REFRESH_TOKEN", ""),
        },

        "letterboxd": {
            "enabled": _env_bool("LETTERBOXD_ENABLED", False),
            "username": os.getenv("LETTERBOXD_USERNAME", ""),
            "password": os.getenv("LETTERBOXD_PASSWORD", ""),
        },

        "imdb": {
            "enabled": _env_bool("IMDB_ENABLED", False),
            "csv_path": os.getenv("IMDB_CSV_PATH", "/config/imdb_ratings.csv"),
        },

        "tvdb": {
            "enabled": _env_bool("TVDB_ENABLED", False),
            "api_key": os.getenv("TVDB_API_KEY", ""),
            "pin": os.getenv("TVDB_PIN", ""),
        },

        "serializd": {
            "enabled": _env_bool("SERIALIZD_ENABLED", False),
            "api_key": os.getenv("SERIALIZD_API_KEY", ""),
        },

        "musicboard": {
            "enabled": _env_bool("MUSICBOARD_ENABLED", False),
            "username": os.getenv("MUSICBOARD_USERNAME", ""),
            "api_key": os.getenv("MUSICBOARD_API_KEY", ""),
        },

        "tmdb": {
            "enabled": _env_bool("TMDB_ENABLED", False),
            "api_key": os.getenv("TMDB_API_KEY", ""),
        },

        "custom_lists": {
            "enabled": _env_bool("CUSTOM_LISTS_ENABLED", False),
        },
    }

    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        yaml.safe_dump(cfg, f, sort_keys=False, allow_unicode=True)
    log.info("🆕 Generated /config/config.yml from environment variables")
    return cfg

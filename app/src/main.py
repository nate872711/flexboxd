import asyncio
import logging
from rich.console import Console

from config_loader import load_config, generate_config_from_env

# Integration clients
from integrations.plex import PlexClient
from integrations.trakt import TraktClient
from integrations.letterboxd import LetterboxdClient
from integrations.imdb import IMDbClient
from integrations.thetvdb import TheTVDBClient
from integrations.serializd import SerializdClient
from integrations.musicboard import MusicboardClient
from integrations.tmdb import TMDbClient

from sync_engine import SyncEngine

console = Console()
log = logging.getLogger("watchweave")
services = {}  # active clients


async def initialize_services(config):
    """Init enabled integrations and stash in the global `services` dict."""
    # Plex
    if config["plex"]["enabled"]:
        services["plex"] = PlexClient(
            config["plex"]["server_url"],
            config["plex"]["token"],
            config["plex"]["username"]
        )
        console.print("[green]✔ Plex enabled")

    # Trakt
    if config["trakt"]["enabled"]:
        trakt = TraktClient(
            client_id=config["trakt"]["client_id"],
            client_secret=config["trakt"]["client_secret"],
            access_token=config["trakt"]["access_token"],
            refresh_token=config["trakt"]["refresh_token"]
        )
        await trakt.authenticate()
        services["trakt"] = trakt
        console.print("[green]✔ Trakt enabled")

    # Letterboxd
    if config["letterboxd"]["enabled"]:
        services["letterboxd"] = LetterboxdClient(
            config["letterboxd"]["username"],
            config["letterboxd"]["password"]
        )
        console.print("[green]✔ Letterboxd enabled")

    # IMDb
    if config["imdb"]["enabled"]:
        services["imdb"] = IMDbClient(config["imdb"]["csv_path"])
        console.print("[green]✔ IMDb enabled")

    # TheTVDB
    if config["tvdb"]["enabled"]:
        tvdb = TheTVDBClient(
            api_key=config["tvdb"]["api_key"],
            pin=config["tvdb"]["pin"]
        )
        await tvdb.authenticate()
        services["tvdb"] = tvdb
        console.print("[green]✔ TheTVDB enabled")

    # Serializd
    if config["serializd"]["enabled"]:
        services["serializd"] = SerializdClient(config["serializd"]["api_key"])
        console.print("[green]✔ Serializd enabled")

    # Musicboard
    if config["musicboard"]["enabled"]:
        services["musicboard"] = MusicboardClient(
            username=config["musicboard"]["username"],
            api_key=config["musicboard"]["api_key"]
        )
        console.print("[green]✔ Musicboard enabled")

    # TMDb
    if config["tmdb"]["enabled"]:
        services["tmdb"] = TMDbClient(api_key=config["tmdb"]["api_key"])
        console.print("[green]✔ TMDb enabled")

    console.print("[bold green]All enabled integrations initialized.\n")


async def run_scheduler(config):
    """Simple interval loop that triggers SyncEngine.sync_all()."""
    interval = int(config["general"]["sync_interval_minutes"])
    engine = SyncEngine(services, config)

    console.print(f"[cyan]🔁 Sync interval: every {interval} minutes")
    while True:
        console.print("[yellow]▶ Running sync cycle…")
        try:
            await engine.sync_all()
            console.print("[green]✓ Sync cycle finished")
        except Exception as e:
            log.exception(f"Sync cycle failed: {e}")
        await asyncio.sleep(interval * 60)


async def main():
    cfg = load_config()
    if not cfg:
        cfg = generate_config_from_env()

    logging.basicConfig(
        level=cfg["general"]["log_level"],
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    console.print("[bold blue]🚀 Starting WatchWeave...\n")
    await initialize_services(cfg)
    await run_scheduler(cfg)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("[red]🛑 WatchWeave stopped")

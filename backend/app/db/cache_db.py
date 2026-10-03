from valkey.asyncio import Valkey

from app.config.config import Settings

vlky: Valkey | None = None


async def init_cache():
    global vlky

    if vlky is None:
        vlky = Valkey(
            host=Settings.VALKEY_HOST,
            port=Settings.VALKEY_PORT,
            password=Settings.VALKEY_PASSWORD,
            db=Settings.VALKEY_DB,
            encoding="utf-8",
            decode_responses=True,
            max_connections=50,
        )


async def close_cache_connection():
    global vlky

    if vlky is not None:
        await vlky.close()
        vlky = None


def get_vlky():
    if vlky is None:
        raise RuntimeError("Valkey not initialized")
    return vlky

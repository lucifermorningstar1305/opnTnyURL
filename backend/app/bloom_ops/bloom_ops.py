from valkey.asyncio import ResponseError, Valkey

from app.logger.logger import RichLogger

logger = RichLogger(name="backend.bloom_ops")


async def create_bloom_filter(
    conn: Valkey,
    filter_name: str,
    fp_rate: float = 1e-10,
    capacity=1_000_000,
    *,
    ignore_if_exists: bool = True,
):
    try:
        logger.info(
            f"[green] Creating bloom filter [bold]{filter_name}[/][/]", markup=True
        )
        await conn.bf().reserve(key=filter_name, errorRate=fp_rate, capacity=capacity)
    except ResponseError as e:
        if ignore_if_exists and "exists" in str(e).lower():
            logger.warning(
                f"[orange] Filter with name {filter_name} already exists. Skipping creation....[/]",
                markup=True,
            )
            return

        logger.exception(
            msg=f"[red blink] Failed to create bloom filter [bold]{filter_name}[/][/]",
            markup=True,
        )
        raise


async def ensure_bloom_filter(
    conn: Valkey,
    filter_name: str,
    capacity: int = 1_000_000,
    fp_rate: float = 1e-10,
    *,
    ignore_if_exists: bool = True,
):
    await create_bloom_filter(
        conn=conn,
        filter_name=filter_name,
        capacity=capacity,
        fp_rate=fp_rate,
        ignore_if_exists=ignore_if_exists,
    )


async def bloom_check(conn: Valkey, filter_name: str, value: str) -> bool:
    bf = conn.bf()
    exists = await bf.exists(filter_name, value)
    return exists


async def bloom_add(conn: Valkey, filter_name: str, value: str):
    bf = conn.bf()
    await bf.add(key=filter_name, item=value)

# LICENSE HEADER MANAGED BY add-license-header
#
# Copyright (c) 2026 Adityam Ghosh
# SPDX-License-Identifier: MIT
#

import string

from sqlalchemy import select, text
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession
from valkey.asyncio import Valkey

from app.bloom_ops.bloom_ops import bloom_check
from app.config.config import Settings
from app.logger.logger import RichLogger
from app.models.tables import ShortTable

CHARS = string.digits + string.ascii_uppercase + string.ascii_lowercase


logger = RichLogger(name="backend.services.urls")


def base62_encode(val: int):
    if val == 0:
        return CHARS[0]

    encoding = ""

    while val > 0:
        val, rem = divmod(val, 62)
        encoding = CHARS[rem] + encoding

    return encoding


async def add_url(session: AsyncSession, vlky: Valkey, url: str) -> str | None:

    machine_id = f"{Settings.MACHINE_ID}"
    bloom_res = await bloom_check(
        conn=vlky, filter_name=Settings.VALKEY_BLOOM_FILTER_NAME, value=url
    )

    logger.info(f"[cyan] Exists in Bloom: {bloom_res} [/]", markup=True)

    if bloom_res:
        stmt = select(ShortTable.short_id).where(ShortTable.original_url == url)
        res = (await session.execute(stmt)).one_or_none()

        if res is not None:
            return res.short_id

    db_id = (
        await session.execute(text("SELECT nextval('short_url_tbl_id_seq')"))
    ).scalar_one()

    short_id = f"{machine_id}{base62_encode(db_id)}"
    stmt = (
        pg_insert(ShortTable)
        .values(id=db_id, original_url=url, short_id=short_id)
        .on_conflict_do_nothing(index_elements=[ShortTable.original_url])
    )

    await session.execute(stmt)
    await session.flush()

    return short_id


async def get_url(session: AsyncSession, vlky: Valkey, short_id: str) -> str | None:

    vlky_res = await vlky.get(short_id)
    if vlky_res is not None:
        return vlky_res

    stmt = select(ShortTable.original_url).where(ShortTable.short_id == short_id)

    res = (await session.execute(stmt)).one_or_none()

    if res is not None:
        await vlky.set(short_id, res.original_url, ex=5000)

    return res.original_url if res is not None else None

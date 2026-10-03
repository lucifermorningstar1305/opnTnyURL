# LICENSE HEADER MANAGED BY add-license-header
#
# Copyright (c) 2026 Adityam Ghosh
# SPDX-License-Identifier: MIT
#

import datetime
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from valkey.asyncio import Valkey

from app.bloom_ops.bloom_ops import bloom_add, ensure_bloom_filter
from app.config.config import Settings
from app.db.cache_db import close_cache_connection, get_vlky, init_cache
from app.db.db import get_session
from app.logger.logger import RichLogger
from app.models.req import AddUrlRequest
from app.services.urls import add_url, get_url

logger = RichLogger(name="backend.app")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_cache()
    vlky = get_vlky()

    await ensure_bloom_filter(
        conn=vlky,
        filter_name=Settings.VALKEY_BLOOM_FILTER_NAME,
        capacity=Settings.VALKEY_BLOOM_FILTER_CAPACITY,
        fp_rate=Settings.VALKEY_BLOOM_FILTER_FP_RATE,
    )

    yield

    await close_cache_connection()


origins = Settings.CORS_ORIGIN.split(",")
app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=Settings.CORS_ALLOWED_METHODS.split(","),
    allow_headers=["*"],
)


@app.get("/health")
async def get_health():
    return {
        "message": f"I'm alive. Current time: {datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%d %H:%M:%SZ')}",
        "statusCode": 200,
    }


@app.post("/add")
async def add_original_url(
    url: AddUrlRequest,
    session: Annotated[AsyncSession, Depends(get_session)],
    vlky: Annotated[Valkey, Depends(get_vlky)],
):
    try:
        res = await add_url(session=session, vlky=vlky, url=str(url.url).strip())
        await bloom_add(
            conn=vlky,
            filter_name=Settings.VALKEY_BLOOM_FILTER_NAME,
            value=str(url.url).strip(),
        )
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"success": True, "data": str(res), "error": None},
        )
    except Exception:
        logger.exception(
            f"[red blink] Failed to [bold]insert {url}[/] with exception[/]",
            markup=True,
        )

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"success": False, "data": None, "error": "Internal Server Error"},
        )


@app.get("/{short_id}")
async def redirect_url(
    short_id: str,
    session: Annotated[AsyncSession, Depends(get_session)],
    vlky: Annotated[Valkey, Depends(get_vlky)],
):
    original_url = await get_url(session=session, vlky=vlky, short_id=short_id)
    if original_url is None:
        raise HTTPException(status_code=404, detail="Short url not found")

    return RedirectResponse(url=original_url, status_code=302)

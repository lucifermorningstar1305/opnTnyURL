# LICENSE HEADER MANAGED BY add-license-header
#
# Copyright (c) 2026 Adityam Ghosh
# SPDX-License-Identifier: MIT
#

import datetime

from sqlalchemy import DateTime, Integer, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class BaseTable(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, nullable=False, index=True
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class ShortTable(BaseTable):
    __tablename__ = "short_url_tbl"

    original_url: Mapped[str] = mapped_column(nullable=False, unique=True)
    short_id: Mapped[str] = mapped_column(nullable=False, unique=True)

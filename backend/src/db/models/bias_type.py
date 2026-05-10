"""ORM model: bias category (e.g. anchoring, confirmation)."""

from __future__ import annotations

import datetime

from sqlalchemy import DateTime, Integer, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base


class BiasType(Base):
    """One cognitive-bias taxonomy entry referenced by ``Case`` rows."""

    __tablename__ = "bias_type"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    slug: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    name_en: Mapped[str] = mapped_column(Text, nullable=False)
    description_en: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

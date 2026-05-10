"""ORM model: translated row for a ``UiString`` (composite PK)."""

from __future__ import annotations

import datetime

from sqlalchemy import DateTime, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base


class UiStringTranslation(Base):
    """Locale-specific translation tied to ``UiString.key`` with FK cascade."""

    __tablename__ = "ui_string_translation"

    key: Mapped[str] = mapped_column(
        Text,
        ForeignKey("ui_string.key", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )
    locale: Mapped[str] = mapped_column(Text, primary_key=True)
    source_hash: Mapped[str] = mapped_column(Text, nullable=False)
    title_translated: Mapped[str] = mapped_column(Text, nullable=False)
    description_translated: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

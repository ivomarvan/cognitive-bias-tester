"""SQLAlchemy ORM declarative base (2.x style — no legacy declarative_base)."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Root mapper registry for all ORM models (maps to Alembic ``target_metadata``)."""

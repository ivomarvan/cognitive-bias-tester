"""GET /v1/i18n/{locale} — UI chrome translations with English fallback."""

from __future__ import annotations

import re
from collections.abc import Sequence

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.ui_string import UiString
from src.db.models.ui_string_translation import UiStringTranslation
from src.db.repositories.ui_string import UiStringRepository
from src.db.session import get_session

router = APIRouter(prefix="/v1", tags=["i18n"])

_LOCALE_RE = re.compile(r"^[a-zA-Z]{2,8}(-[a-zA-Z0-9]{2,8})*$")


class I18nResponse(BaseModel):
    """Payload returned by ``GET /v1/i18n/{locale}``."""

    locale: str = Field(description="Requested IETF language tag.")
    translations: dict[str, str] = Field(
        description="Map of UI key to display title (English fallback when needed).",
    )
    stale_keys: list[str] = Field(
        default_factory=list,
        description="Keys whose translation ``source_hash`` no longer matches English source.",
    )


def validate_locale_path(locale: str) -> str:
    """Reject empty or unsafe path-like locale strings.

    Args:
        locale: Raw path segment from the URL.

    Returns:
        The same string if valid.

    Raises:
        HTTPException: 422 when the tag is not a simple BCP-47-like token.
    """
    if (
        not locale
        or "/" in locale
        or "." in locale
        or ".." in locale
        or not _LOCALE_RE.fullmatch(locale)
    ):
        raise HTTPException(status_code=422, detail="Invalid locale format")
    return locale


def build_i18n_payload(
    locale: str,
    rows: Sequence[tuple[UiString, UiStringTranslation | None]],
) -> I18nResponse:
    """Resolve translation rows into API payload (testable without HTTP).

    Args:
        locale: Requested locale (after validation).
        rows: Pairs from ``UiStringRepository.get_all_with_translation``.

    Returns:
        Structured response following the MVP i18n rules.

    Raises:
        None.
    """
    translations: dict[str, str] = {}
    stale_keys: list[str] = []

    if locale == "en":
        for ui_string, _translation in rows:
            translations[ui_string.key] = ui_string.title
        return I18nResponse(locale=locale, translations=translations, stale_keys=[])

    for ui_string, translation in rows:
        if translation is None:
            translations[ui_string.key] = ui_string.title
        elif translation.source_hash != ui_string.source_hash:
            translations[ui_string.key] = ui_string.title
            stale_keys.append(ui_string.key)
        else:
            translations[ui_string.key] = translation.title_translated

    stale_keys.sort()
    return I18nResponse(locale=locale, translations=translations, stale_keys=stale_keys)


async def get_ui_string_repo(
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> UiStringRepository:
    """Instantiate ``UiStringRepository`` for the current request session.

    Args:
        session: Request-scoped async session.

    Returns:
        Repository bound to ``session``.

    Raises:
        None.
    """
    return UiStringRepository(session)


@router.get("/i18n/{locale}", response_model=I18nResponse)
async def get_i18n(
    locale: str,
    repo: UiStringRepository = Depends(get_ui_string_repo),  # noqa: B008
) -> I18nResponse:
    """Return all UI string titles for ``locale`` with English fallback.

    Missing translations use English and do not appear in ``stale_keys``.
    Hash mismatches use English and list the key in ``stale_keys`` for background refresh.

    Args:
        locale: IETF language tag (e.g. ``en``, ``cs``, ``pt-BR``).
        repo: Data access for UI strings and translations.

    Returns:
        ``I18nResponse`` with ``translations`` and ``stale_keys``.

    Raises:
        HTTPException: 422 for malformed locale strings.
        sqlalchemy.exc.SQLAlchemyError: Propagated from the database layer.
    """
    validate_locale_path(locale)
    rows = await repo.get_all_with_translation(locale)
    return build_i18n_payload(locale, rows)

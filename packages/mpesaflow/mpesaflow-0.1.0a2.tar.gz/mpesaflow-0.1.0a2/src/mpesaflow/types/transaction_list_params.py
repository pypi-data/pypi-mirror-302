# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["TransactionListParams"]


class TransactionListParams(TypedDict, total=False):
    app_id: Required[Annotated[str, PropertyInfo(alias="appId")]]

    ending_before: str
    """Cursor for the previous page"""

    limit: int
    """Number of items to return"""

    starting_after: str
    """Cursor for the next page"""

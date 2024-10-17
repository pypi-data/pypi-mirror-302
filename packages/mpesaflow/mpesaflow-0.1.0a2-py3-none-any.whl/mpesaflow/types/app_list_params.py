# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["AppListParams"]


class AppListParams(TypedDict, total=False):
    ending_before: str
    """Cursor for the previous page"""

    limit: int
    """Number of items to return"""

    starting_after: str
    """Cursor for the next page"""

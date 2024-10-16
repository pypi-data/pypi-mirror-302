# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["TransactionListParams"]


class TransactionListParams(TypedDict, total=False):
    app_id: Required[Annotated[str, PropertyInfo(alias="appId")]]

    ending_before: str

    limit: int

    starting_after: str

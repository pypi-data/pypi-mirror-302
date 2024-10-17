# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["TransactionCreateParams"]


class TransactionCreateParams(TypedDict, total=False):
    account_reference: Annotated[str, PropertyInfo(alias="accountReference")]

    amount: float

    mpesa_request_id: Annotated[str, PropertyInfo(alias="mpesaRequestId")]

    phone_number: Annotated[str, PropertyInfo(alias="phoneNumber")]

    transaction_desc: Annotated[str, PropertyInfo(alias="transactionDesc")]

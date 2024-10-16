# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["Transaction"]


class Transaction(BaseModel):
    id: Optional[str] = None

    account_reference: Optional[str] = FieldInfo(alias="accountReference", default=None)

    amount: Optional[float] = None

    date_created: Optional[datetime] = None

    mpesa_request_id: Optional[str] = FieldInfo(alias="mpesaRequestId", default=None)

    phone_number: Optional[str] = FieldInfo(alias="phoneNumber", default=None)

    result_desc: Optional[str] = FieldInfo(alias="resultDesc", default=None)

    status: Optional[Literal["pending", "completed", "failed"]] = None

    transaction_desc: Optional[str] = FieldInfo(alias="transactionDesc", default=None)

    transaction_id: Optional[str] = FieldInfo(alias="transactionId", default=None)

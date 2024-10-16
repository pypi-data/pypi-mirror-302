# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["TransactionCreateResponse"]


class TransactionCreateResponse(BaseModel):
    message: Optional[str] = None

    transaction_id: Optional[str] = FieldInfo(alias="transactionId", default=None)

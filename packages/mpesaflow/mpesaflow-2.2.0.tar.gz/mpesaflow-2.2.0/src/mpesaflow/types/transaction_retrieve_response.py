# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel
from .transaction import Transaction

__all__ = ["TransactionRetrieveResponse"]


class TransactionRetrieveResponse(BaseModel):
    transaction: Optional[Transaction] = None

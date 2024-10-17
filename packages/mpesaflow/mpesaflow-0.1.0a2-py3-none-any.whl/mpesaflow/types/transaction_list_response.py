# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel
from .transaction import Transaction

__all__ = ["TransactionListResponse"]


class TransactionListResponse(BaseModel):
    data: Optional[List[Transaction]] = None

# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel
from .application import Application

__all__ = ["AppListResponse"]


class AppListResponse(BaseModel):
    data: Optional[List[Application]] = None

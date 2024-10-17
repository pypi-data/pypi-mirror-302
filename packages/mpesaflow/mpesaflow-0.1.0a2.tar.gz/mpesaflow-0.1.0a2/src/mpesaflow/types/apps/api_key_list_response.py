# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["APIKeyListResponse", "Data"]


class Data(BaseModel):
    id: Optional[str] = None

    application_id: Optional[str] = FieldInfo(alias="applicationId", default=None)

    key_name: Optional[str] = FieldInfo(alias="keyName", default=None)


class APIKeyListResponse(BaseModel):
    data: Optional[List[Data]] = None

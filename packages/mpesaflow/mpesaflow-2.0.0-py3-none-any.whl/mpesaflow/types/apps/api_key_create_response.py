# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["APIKeyCreateResponse"]


class APIKeyCreateResponse(BaseModel):
    api_key_id: Optional[str] = FieldInfo(alias="apiKeyId", default=None)

    message: Optional[str] = None

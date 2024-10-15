# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..._models import BaseModel

__all__ = ["Error"]


class Error(BaseModel):
    message: Optional[str] = None

    name: Optional[str] = None

# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["EventRetrieveResponse", "Data"]


class Data(BaseModel):
    id: str

    created_at: int

    level: Literal["info", "warn", "error"]

    message: str

    object: Literal["fine_tuning.job.event"]


class EventRetrieveResponse(BaseModel):
    data: List[Data]

    object: Literal["list"]

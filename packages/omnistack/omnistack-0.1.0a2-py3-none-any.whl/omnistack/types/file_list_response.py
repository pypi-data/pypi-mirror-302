# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import Literal

from .._models import BaseModel
from .openai_file import OpenAIFile

__all__ = ["FileListResponse"]


class FileListResponse(BaseModel):
    data: List[OpenAIFile]

    object: Literal["list"]

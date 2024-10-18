# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["Invite"]


class Invite(BaseModel):
    id: str
    """The identifier, which can be referenced in API endpoints"""

    email: str
    """The email address of the individual to whom the invite was sent"""

    expires_at: int
    """The Unix timestamp (in seconds) of when the invite expires."""

    invited_at: int
    """The Unix timestamp (in seconds) of when the invite was sent."""

    object: Literal["organization.invite"]
    """The object type, which is always `organization.invite`"""

    role: Literal["owner", "reader"]
    """`owner` or `reader`"""

    status: Literal["accepted", "expired", "pending"]
    """`accepted`,`expired`, or `pending`"""

    accepted_at: Optional[int] = None
    """The Unix timestamp (in seconds) of when the invite was accepted."""

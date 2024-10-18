# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["InviteCreateParams"]


class InviteCreateParams(TypedDict, total=False):
    email: Required[str]
    """Send an email to this address"""

    role: Required[Literal["reader", "owner"]]
    """`owner` or `reader`"""

# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from omnistack import Omnistack, AsyncOmnistack
from tests.utils import assert_matches_type
from omnistack.types.organization import AuditLogListResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestAuditLogs:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_list(self, client: Omnistack) -> None:
        audit_log = client.organization.audit_logs.list()
        assert_matches_type(AuditLogListResponse, audit_log, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Omnistack) -> None:
        audit_log = client.organization.audit_logs.list(
            actor_emails=["string", "string", "string"],
            actor_ids=["string", "string", "string"],
            after="after",
            before="before",
            effective_at={
                "gt": 0,
                "gte": 0,
                "lt": 0,
                "lte": 0,
            },
            event_types=["api_key.created", "api_key.updated", "api_key.deleted"],
            limit=0,
            project_ids=["string", "string", "string"],
            resource_ids=["string", "string", "string"],
        )
        assert_matches_type(AuditLogListResponse, audit_log, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Omnistack) -> None:
        response = client.organization.audit_logs.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        audit_log = response.parse()
        assert_matches_type(AuditLogListResponse, audit_log, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Omnistack) -> None:
        with client.organization.audit_logs.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            audit_log = response.parse()
            assert_matches_type(AuditLogListResponse, audit_log, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncAuditLogs:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_list(self, async_client: AsyncOmnistack) -> None:
        audit_log = await async_client.organization.audit_logs.list()
        assert_matches_type(AuditLogListResponse, audit_log, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncOmnistack) -> None:
        audit_log = await async_client.organization.audit_logs.list(
            actor_emails=["string", "string", "string"],
            actor_ids=["string", "string", "string"],
            after="after",
            before="before",
            effective_at={
                "gt": 0,
                "gte": 0,
                "lt": 0,
                "lte": 0,
            },
            event_types=["api_key.created", "api_key.updated", "api_key.deleted"],
            limit=0,
            project_ids=["string", "string", "string"],
            resource_ids=["string", "string", "string"],
        )
        assert_matches_type(AuditLogListResponse, audit_log, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncOmnistack) -> None:
        response = await async_client.organization.audit_logs.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        audit_log = await response.parse()
        assert_matches_type(AuditLogListResponse, audit_log, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncOmnistack) -> None:
        async with async_client.organization.audit_logs.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            audit_log = await response.parse()
            assert_matches_type(AuditLogListResponse, audit_log, path=["response"])

        assert cast(Any, response.is_closed) is True

# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from omnistack import Omnistack, AsyncOmnistack
from tests.utils import assert_matches_type
from omnistack.types.shared import ProjectServiceAccount
from omnistack.types.organization.projects import (
    ServiceAccountListResponse,
    ServiceAccountCreateResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestServiceAccounts:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Omnistack) -> None:
        service_account = client.organization.projects.service_accounts.create(
            project_id="project_id",
            name="name",
        )
        assert_matches_type(ServiceAccountCreateResponse, service_account, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Omnistack) -> None:
        response = client.organization.projects.service_accounts.with_raw_response.create(
            project_id="project_id",
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        service_account = response.parse()
        assert_matches_type(ServiceAccountCreateResponse, service_account, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Omnistack) -> None:
        with client.organization.projects.service_accounts.with_streaming_response.create(
            project_id="project_id",
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            service_account = response.parse()
            assert_matches_type(ServiceAccountCreateResponse, service_account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create(self, client: Omnistack) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `project_id` but received ''"):
            client.organization.projects.service_accounts.with_raw_response.create(
                project_id="",
                name="name",
            )

    @parametrize
    def test_method_retrieve(self, client: Omnistack) -> None:
        service_account = client.organization.projects.service_accounts.retrieve(
            service_account_id="service_account_id",
            project_id="project_id",
        )
        assert_matches_type(ProjectServiceAccount, service_account, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Omnistack) -> None:
        response = client.organization.projects.service_accounts.with_raw_response.retrieve(
            service_account_id="service_account_id",
            project_id="project_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        service_account = response.parse()
        assert_matches_type(ProjectServiceAccount, service_account, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Omnistack) -> None:
        with client.organization.projects.service_accounts.with_streaming_response.retrieve(
            service_account_id="service_account_id",
            project_id="project_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            service_account = response.parse()
            assert_matches_type(ProjectServiceAccount, service_account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Omnistack) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `project_id` but received ''"):
            client.organization.projects.service_accounts.with_raw_response.retrieve(
                service_account_id="service_account_id",
                project_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `service_account_id` but received ''"):
            client.organization.projects.service_accounts.with_raw_response.retrieve(
                service_account_id="",
                project_id="project_id",
            )

    @parametrize
    def test_method_list(self, client: Omnistack) -> None:
        service_account = client.organization.projects.service_accounts.list(
            project_id="project_id",
        )
        assert_matches_type(ServiceAccountListResponse, service_account, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Omnistack) -> None:
        service_account = client.organization.projects.service_accounts.list(
            project_id="project_id",
            after="after",
            limit=0,
        )
        assert_matches_type(ServiceAccountListResponse, service_account, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Omnistack) -> None:
        response = client.organization.projects.service_accounts.with_raw_response.list(
            project_id="project_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        service_account = response.parse()
        assert_matches_type(ServiceAccountListResponse, service_account, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Omnistack) -> None:
        with client.organization.projects.service_accounts.with_streaming_response.list(
            project_id="project_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            service_account = response.parse()
            assert_matches_type(ServiceAccountListResponse, service_account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: Omnistack) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `project_id` but received ''"):
            client.organization.projects.service_accounts.with_raw_response.list(
                project_id="",
            )


class TestAsyncServiceAccounts:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncOmnistack) -> None:
        service_account = await async_client.organization.projects.service_accounts.create(
            project_id="project_id",
            name="name",
        )
        assert_matches_type(ServiceAccountCreateResponse, service_account, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncOmnistack) -> None:
        response = await async_client.organization.projects.service_accounts.with_raw_response.create(
            project_id="project_id",
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        service_account = await response.parse()
        assert_matches_type(ServiceAccountCreateResponse, service_account, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncOmnistack) -> None:
        async with async_client.organization.projects.service_accounts.with_streaming_response.create(
            project_id="project_id",
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            service_account = await response.parse()
            assert_matches_type(ServiceAccountCreateResponse, service_account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create(self, async_client: AsyncOmnistack) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `project_id` but received ''"):
            await async_client.organization.projects.service_accounts.with_raw_response.create(
                project_id="",
                name="name",
            )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncOmnistack) -> None:
        service_account = await async_client.organization.projects.service_accounts.retrieve(
            service_account_id="service_account_id",
            project_id="project_id",
        )
        assert_matches_type(ProjectServiceAccount, service_account, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncOmnistack) -> None:
        response = await async_client.organization.projects.service_accounts.with_raw_response.retrieve(
            service_account_id="service_account_id",
            project_id="project_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        service_account = await response.parse()
        assert_matches_type(ProjectServiceAccount, service_account, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncOmnistack) -> None:
        async with async_client.organization.projects.service_accounts.with_streaming_response.retrieve(
            service_account_id="service_account_id",
            project_id="project_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            service_account = await response.parse()
            assert_matches_type(ProjectServiceAccount, service_account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncOmnistack) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `project_id` but received ''"):
            await async_client.organization.projects.service_accounts.with_raw_response.retrieve(
                service_account_id="service_account_id",
                project_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `service_account_id` but received ''"):
            await async_client.organization.projects.service_accounts.with_raw_response.retrieve(
                service_account_id="",
                project_id="project_id",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncOmnistack) -> None:
        service_account = await async_client.organization.projects.service_accounts.list(
            project_id="project_id",
        )
        assert_matches_type(ServiceAccountListResponse, service_account, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncOmnistack) -> None:
        service_account = await async_client.organization.projects.service_accounts.list(
            project_id="project_id",
            after="after",
            limit=0,
        )
        assert_matches_type(ServiceAccountListResponse, service_account, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncOmnistack) -> None:
        response = await async_client.organization.projects.service_accounts.with_raw_response.list(
            project_id="project_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        service_account = await response.parse()
        assert_matches_type(ServiceAccountListResponse, service_account, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncOmnistack) -> None:
        async with async_client.organization.projects.service_accounts.with_streaming_response.list(
            project_id="project_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            service_account = await response.parse()
            assert_matches_type(ServiceAccountListResponse, service_account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncOmnistack) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `project_id` but received ''"):
            await async_client.organization.projects.service_accounts.with_raw_response.list(
                project_id="",
            )

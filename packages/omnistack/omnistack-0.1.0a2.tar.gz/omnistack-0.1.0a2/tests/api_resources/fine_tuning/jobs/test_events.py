# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from omnistack import Omnistack, AsyncOmnistack
from tests.utils import assert_matches_type
from omnistack.types.fine_tuning.jobs import EventRetrieveResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestEvents:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: Omnistack) -> None:
        event = client.fine_tuning.jobs.events.retrieve(
            fine_tuning_job_id="ft-AF1WoRqd3aJAHsqc9NY7iL8F",
        )
        assert_matches_type(EventRetrieveResponse, event, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: Omnistack) -> None:
        event = client.fine_tuning.jobs.events.retrieve(
            fine_tuning_job_id="ft-AF1WoRqd3aJAHsqc9NY7iL8F",
            after="after",
            limit=0,
        )
        assert_matches_type(EventRetrieveResponse, event, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Omnistack) -> None:
        response = client.fine_tuning.jobs.events.with_raw_response.retrieve(
            fine_tuning_job_id="ft-AF1WoRqd3aJAHsqc9NY7iL8F",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event = response.parse()
        assert_matches_type(EventRetrieveResponse, event, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Omnistack) -> None:
        with client.fine_tuning.jobs.events.with_streaming_response.retrieve(
            fine_tuning_job_id="ft-AF1WoRqd3aJAHsqc9NY7iL8F",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event = response.parse()
            assert_matches_type(EventRetrieveResponse, event, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Omnistack) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `fine_tuning_job_id` but received ''"):
            client.fine_tuning.jobs.events.with_raw_response.retrieve(
                fine_tuning_job_id="",
            )


class TestAsyncEvents:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncOmnistack) -> None:
        event = await async_client.fine_tuning.jobs.events.retrieve(
            fine_tuning_job_id="ft-AF1WoRqd3aJAHsqc9NY7iL8F",
        )
        assert_matches_type(EventRetrieveResponse, event, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncOmnistack) -> None:
        event = await async_client.fine_tuning.jobs.events.retrieve(
            fine_tuning_job_id="ft-AF1WoRqd3aJAHsqc9NY7iL8F",
            after="after",
            limit=0,
        )
        assert_matches_type(EventRetrieveResponse, event, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncOmnistack) -> None:
        response = await async_client.fine_tuning.jobs.events.with_raw_response.retrieve(
            fine_tuning_job_id="ft-AF1WoRqd3aJAHsqc9NY7iL8F",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event = await response.parse()
        assert_matches_type(EventRetrieveResponse, event, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncOmnistack) -> None:
        async with async_client.fine_tuning.jobs.events.with_streaming_response.retrieve(
            fine_tuning_job_id="ft-AF1WoRqd3aJAHsqc9NY7iL8F",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event = await response.parse()
            assert_matches_type(EventRetrieveResponse, event, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncOmnistack) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `fine_tuning_job_id` but received ''"):
            await async_client.fine_tuning.jobs.events.with_raw_response.retrieve(
                fine_tuning_job_id="",
            )

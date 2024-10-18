# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from omnistack import Omnistack, AsyncOmnistack
from tests.utils import assert_matches_type
from omnistack.types.threads.runs import RunStepObject, StepListResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSteps:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: Omnistack) -> None:
        step = client.threads.runs.steps.retrieve(
            step_id="step_id",
            thread_id="thread_id",
            run_id="run_id",
        )
        assert_matches_type(RunStepObject, step, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: Omnistack) -> None:
        step = client.threads.runs.steps.retrieve(
            step_id="step_id",
            thread_id="thread_id",
            run_id="run_id",
            include=["step_details.tool_calls[*].file_search.results[*].content"],
        )
        assert_matches_type(RunStepObject, step, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Omnistack) -> None:
        response = client.threads.runs.steps.with_raw_response.retrieve(
            step_id="step_id",
            thread_id="thread_id",
            run_id="run_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        step = response.parse()
        assert_matches_type(RunStepObject, step, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Omnistack) -> None:
        with client.threads.runs.steps.with_streaming_response.retrieve(
            step_id="step_id",
            thread_id="thread_id",
            run_id="run_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            step = response.parse()
            assert_matches_type(RunStepObject, step, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Omnistack) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `thread_id` but received ''"):
            client.threads.runs.steps.with_raw_response.retrieve(
                step_id="step_id",
                thread_id="",
                run_id="run_id",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `run_id` but received ''"):
            client.threads.runs.steps.with_raw_response.retrieve(
                step_id="step_id",
                thread_id="thread_id",
                run_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `step_id` but received ''"):
            client.threads.runs.steps.with_raw_response.retrieve(
                step_id="",
                thread_id="thread_id",
                run_id="run_id",
            )

    @parametrize
    def test_method_list(self, client: Omnistack) -> None:
        step = client.threads.runs.steps.list(
            run_id="run_id",
            thread_id="thread_id",
        )
        assert_matches_type(StepListResponse, step, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Omnistack) -> None:
        step = client.threads.runs.steps.list(
            run_id="run_id",
            thread_id="thread_id",
            after="after",
            before="before",
            include=["step_details.tool_calls[*].file_search.results[*].content"],
            limit=0,
            order="asc",
        )
        assert_matches_type(StepListResponse, step, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Omnistack) -> None:
        response = client.threads.runs.steps.with_raw_response.list(
            run_id="run_id",
            thread_id="thread_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        step = response.parse()
        assert_matches_type(StepListResponse, step, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Omnistack) -> None:
        with client.threads.runs.steps.with_streaming_response.list(
            run_id="run_id",
            thread_id="thread_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            step = response.parse()
            assert_matches_type(StepListResponse, step, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: Omnistack) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `thread_id` but received ''"):
            client.threads.runs.steps.with_raw_response.list(
                run_id="run_id",
                thread_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `run_id` but received ''"):
            client.threads.runs.steps.with_raw_response.list(
                run_id="",
                thread_id="thread_id",
            )


class TestAsyncSteps:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncOmnistack) -> None:
        step = await async_client.threads.runs.steps.retrieve(
            step_id="step_id",
            thread_id="thread_id",
            run_id="run_id",
        )
        assert_matches_type(RunStepObject, step, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncOmnistack) -> None:
        step = await async_client.threads.runs.steps.retrieve(
            step_id="step_id",
            thread_id="thread_id",
            run_id="run_id",
            include=["step_details.tool_calls[*].file_search.results[*].content"],
        )
        assert_matches_type(RunStepObject, step, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncOmnistack) -> None:
        response = await async_client.threads.runs.steps.with_raw_response.retrieve(
            step_id="step_id",
            thread_id="thread_id",
            run_id="run_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        step = await response.parse()
        assert_matches_type(RunStepObject, step, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncOmnistack) -> None:
        async with async_client.threads.runs.steps.with_streaming_response.retrieve(
            step_id="step_id",
            thread_id="thread_id",
            run_id="run_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            step = await response.parse()
            assert_matches_type(RunStepObject, step, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncOmnistack) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `thread_id` but received ''"):
            await async_client.threads.runs.steps.with_raw_response.retrieve(
                step_id="step_id",
                thread_id="",
                run_id="run_id",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `run_id` but received ''"):
            await async_client.threads.runs.steps.with_raw_response.retrieve(
                step_id="step_id",
                thread_id="thread_id",
                run_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `step_id` but received ''"):
            await async_client.threads.runs.steps.with_raw_response.retrieve(
                step_id="",
                thread_id="thread_id",
                run_id="run_id",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncOmnistack) -> None:
        step = await async_client.threads.runs.steps.list(
            run_id="run_id",
            thread_id="thread_id",
        )
        assert_matches_type(StepListResponse, step, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncOmnistack) -> None:
        step = await async_client.threads.runs.steps.list(
            run_id="run_id",
            thread_id="thread_id",
            after="after",
            before="before",
            include=["step_details.tool_calls[*].file_search.results[*].content"],
            limit=0,
            order="asc",
        )
        assert_matches_type(StepListResponse, step, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncOmnistack) -> None:
        response = await async_client.threads.runs.steps.with_raw_response.list(
            run_id="run_id",
            thread_id="thread_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        step = await response.parse()
        assert_matches_type(StepListResponse, step, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncOmnistack) -> None:
        async with async_client.threads.runs.steps.with_streaming_response.list(
            run_id="run_id",
            thread_id="thread_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            step = await response.parse()
            assert_matches_type(StepListResponse, step, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncOmnistack) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `thread_id` but received ''"):
            await async_client.threads.runs.steps.with_raw_response.list(
                run_id="run_id",
                thread_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `run_id` but received ''"):
            await async_client.threads.runs.steps.with_raw_response.list(
                run_id="",
                thread_id="thread_id",
            )

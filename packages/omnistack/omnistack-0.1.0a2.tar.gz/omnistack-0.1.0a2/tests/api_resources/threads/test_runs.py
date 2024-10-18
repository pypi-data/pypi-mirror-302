# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from omnistack import Omnistack, AsyncOmnistack
from tests.utils import assert_matches_type
from omnistack.types.threads import RunListResponse
from omnistack.types.assistants import RunObject

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestRuns:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Omnistack) -> None:
        run = client.threads.runs.create(
            run_id="run_id",
            thread_id="thread_id",
        )
        assert_matches_type(RunObject, run, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Omnistack) -> None:
        run = client.threads.runs.create(
            run_id="run_id",
            thread_id="thread_id",
            metadata={},
        )
        assert_matches_type(RunObject, run, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Omnistack) -> None:
        response = client.threads.runs.with_raw_response.create(
            run_id="run_id",
            thread_id="thread_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        run = response.parse()
        assert_matches_type(RunObject, run, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Omnistack) -> None:
        with client.threads.runs.with_streaming_response.create(
            run_id="run_id",
            thread_id="thread_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            run = response.parse()
            assert_matches_type(RunObject, run, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create(self, client: Omnistack) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `thread_id` but received ''"):
            client.threads.runs.with_raw_response.create(
                run_id="run_id",
                thread_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `run_id` but received ''"):
            client.threads.runs.with_raw_response.create(
                run_id="",
                thread_id="thread_id",
            )

    @parametrize
    def test_method_retrieve(self, client: Omnistack) -> None:
        run = client.threads.runs.retrieve(
            run_id="run_id",
            thread_id="thread_id",
        )
        assert_matches_type(RunObject, run, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Omnistack) -> None:
        response = client.threads.runs.with_raw_response.retrieve(
            run_id="run_id",
            thread_id="thread_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        run = response.parse()
        assert_matches_type(RunObject, run, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Omnistack) -> None:
        with client.threads.runs.with_streaming_response.retrieve(
            run_id="run_id",
            thread_id="thread_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            run = response.parse()
            assert_matches_type(RunObject, run, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Omnistack) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `thread_id` but received ''"):
            client.threads.runs.with_raw_response.retrieve(
                run_id="run_id",
                thread_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `run_id` but received ''"):
            client.threads.runs.with_raw_response.retrieve(
                run_id="",
                thread_id="thread_id",
            )

    @parametrize
    def test_method_list(self, client: Omnistack) -> None:
        run = client.threads.runs.list(
            thread_id="thread_id",
        )
        assert_matches_type(RunListResponse, run, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Omnistack) -> None:
        run = client.threads.runs.list(
            thread_id="thread_id",
            after="after",
            before="before",
            limit=0,
            order="asc",
        )
        assert_matches_type(RunListResponse, run, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Omnistack) -> None:
        response = client.threads.runs.with_raw_response.list(
            thread_id="thread_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        run = response.parse()
        assert_matches_type(RunListResponse, run, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Omnistack) -> None:
        with client.threads.runs.with_streaming_response.list(
            thread_id="thread_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            run = response.parse()
            assert_matches_type(RunListResponse, run, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: Omnistack) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `thread_id` but received ''"):
            client.threads.runs.with_raw_response.list(
                thread_id="",
            )

    @parametrize
    def test_method_cancel(self, client: Omnistack) -> None:
        run = client.threads.runs.cancel(
            run_id="run_id",
            thread_id="thread_id",
        )
        assert_matches_type(RunObject, run, path=["response"])

    @parametrize
    def test_raw_response_cancel(self, client: Omnistack) -> None:
        response = client.threads.runs.with_raw_response.cancel(
            run_id="run_id",
            thread_id="thread_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        run = response.parse()
        assert_matches_type(RunObject, run, path=["response"])

    @parametrize
    def test_streaming_response_cancel(self, client: Omnistack) -> None:
        with client.threads.runs.with_streaming_response.cancel(
            run_id="run_id",
            thread_id="thread_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            run = response.parse()
            assert_matches_type(RunObject, run, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_cancel(self, client: Omnistack) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `thread_id` but received ''"):
            client.threads.runs.with_raw_response.cancel(
                run_id="run_id",
                thread_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `run_id` but received ''"):
            client.threads.runs.with_raw_response.cancel(
                run_id="",
                thread_id="thread_id",
            )

    @parametrize
    def test_method_submit_tool_outputs(self, client: Omnistack) -> None:
        run = client.threads.runs.submit_tool_outputs(
            run_id="run_id",
            thread_id="thread_id",
            tool_outputs=[{}, {}, {}],
        )
        assert_matches_type(RunObject, run, path=["response"])

    @parametrize
    def test_method_submit_tool_outputs_with_all_params(self, client: Omnistack) -> None:
        run = client.threads.runs.submit_tool_outputs(
            run_id="run_id",
            thread_id="thread_id",
            tool_outputs=[
                {
                    "output": "output",
                    "tool_call_id": "tool_call_id",
                },
                {
                    "output": "output",
                    "tool_call_id": "tool_call_id",
                },
                {
                    "output": "output",
                    "tool_call_id": "tool_call_id",
                },
            ],
            stream=True,
        )
        assert_matches_type(RunObject, run, path=["response"])

    @parametrize
    def test_raw_response_submit_tool_outputs(self, client: Omnistack) -> None:
        response = client.threads.runs.with_raw_response.submit_tool_outputs(
            run_id="run_id",
            thread_id="thread_id",
            tool_outputs=[{}, {}, {}],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        run = response.parse()
        assert_matches_type(RunObject, run, path=["response"])

    @parametrize
    def test_streaming_response_submit_tool_outputs(self, client: Omnistack) -> None:
        with client.threads.runs.with_streaming_response.submit_tool_outputs(
            run_id="run_id",
            thread_id="thread_id",
            tool_outputs=[{}, {}, {}],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            run = response.parse()
            assert_matches_type(RunObject, run, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_submit_tool_outputs(self, client: Omnistack) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `thread_id` but received ''"):
            client.threads.runs.with_raw_response.submit_tool_outputs(
                run_id="run_id",
                thread_id="",
                tool_outputs=[{}, {}, {}],
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `run_id` but received ''"):
            client.threads.runs.with_raw_response.submit_tool_outputs(
                run_id="",
                thread_id="thread_id",
                tool_outputs=[{}, {}, {}],
            )


class TestAsyncRuns:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncOmnistack) -> None:
        run = await async_client.threads.runs.create(
            run_id="run_id",
            thread_id="thread_id",
        )
        assert_matches_type(RunObject, run, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncOmnistack) -> None:
        run = await async_client.threads.runs.create(
            run_id="run_id",
            thread_id="thread_id",
            metadata={},
        )
        assert_matches_type(RunObject, run, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncOmnistack) -> None:
        response = await async_client.threads.runs.with_raw_response.create(
            run_id="run_id",
            thread_id="thread_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        run = await response.parse()
        assert_matches_type(RunObject, run, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncOmnistack) -> None:
        async with async_client.threads.runs.with_streaming_response.create(
            run_id="run_id",
            thread_id="thread_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            run = await response.parse()
            assert_matches_type(RunObject, run, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create(self, async_client: AsyncOmnistack) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `thread_id` but received ''"):
            await async_client.threads.runs.with_raw_response.create(
                run_id="run_id",
                thread_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `run_id` but received ''"):
            await async_client.threads.runs.with_raw_response.create(
                run_id="",
                thread_id="thread_id",
            )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncOmnistack) -> None:
        run = await async_client.threads.runs.retrieve(
            run_id="run_id",
            thread_id="thread_id",
        )
        assert_matches_type(RunObject, run, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncOmnistack) -> None:
        response = await async_client.threads.runs.with_raw_response.retrieve(
            run_id="run_id",
            thread_id="thread_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        run = await response.parse()
        assert_matches_type(RunObject, run, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncOmnistack) -> None:
        async with async_client.threads.runs.with_streaming_response.retrieve(
            run_id="run_id",
            thread_id="thread_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            run = await response.parse()
            assert_matches_type(RunObject, run, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncOmnistack) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `thread_id` but received ''"):
            await async_client.threads.runs.with_raw_response.retrieve(
                run_id="run_id",
                thread_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `run_id` but received ''"):
            await async_client.threads.runs.with_raw_response.retrieve(
                run_id="",
                thread_id="thread_id",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncOmnistack) -> None:
        run = await async_client.threads.runs.list(
            thread_id="thread_id",
        )
        assert_matches_type(RunListResponse, run, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncOmnistack) -> None:
        run = await async_client.threads.runs.list(
            thread_id="thread_id",
            after="after",
            before="before",
            limit=0,
            order="asc",
        )
        assert_matches_type(RunListResponse, run, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncOmnistack) -> None:
        response = await async_client.threads.runs.with_raw_response.list(
            thread_id="thread_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        run = await response.parse()
        assert_matches_type(RunListResponse, run, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncOmnistack) -> None:
        async with async_client.threads.runs.with_streaming_response.list(
            thread_id="thread_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            run = await response.parse()
            assert_matches_type(RunListResponse, run, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncOmnistack) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `thread_id` but received ''"):
            await async_client.threads.runs.with_raw_response.list(
                thread_id="",
            )

    @parametrize
    async def test_method_cancel(self, async_client: AsyncOmnistack) -> None:
        run = await async_client.threads.runs.cancel(
            run_id="run_id",
            thread_id="thread_id",
        )
        assert_matches_type(RunObject, run, path=["response"])

    @parametrize
    async def test_raw_response_cancel(self, async_client: AsyncOmnistack) -> None:
        response = await async_client.threads.runs.with_raw_response.cancel(
            run_id="run_id",
            thread_id="thread_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        run = await response.parse()
        assert_matches_type(RunObject, run, path=["response"])

    @parametrize
    async def test_streaming_response_cancel(self, async_client: AsyncOmnistack) -> None:
        async with async_client.threads.runs.with_streaming_response.cancel(
            run_id="run_id",
            thread_id="thread_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            run = await response.parse()
            assert_matches_type(RunObject, run, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_cancel(self, async_client: AsyncOmnistack) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `thread_id` but received ''"):
            await async_client.threads.runs.with_raw_response.cancel(
                run_id="run_id",
                thread_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `run_id` but received ''"):
            await async_client.threads.runs.with_raw_response.cancel(
                run_id="",
                thread_id="thread_id",
            )

    @parametrize
    async def test_method_submit_tool_outputs(self, async_client: AsyncOmnistack) -> None:
        run = await async_client.threads.runs.submit_tool_outputs(
            run_id="run_id",
            thread_id="thread_id",
            tool_outputs=[{}, {}, {}],
        )
        assert_matches_type(RunObject, run, path=["response"])

    @parametrize
    async def test_method_submit_tool_outputs_with_all_params(self, async_client: AsyncOmnistack) -> None:
        run = await async_client.threads.runs.submit_tool_outputs(
            run_id="run_id",
            thread_id="thread_id",
            tool_outputs=[
                {
                    "output": "output",
                    "tool_call_id": "tool_call_id",
                },
                {
                    "output": "output",
                    "tool_call_id": "tool_call_id",
                },
                {
                    "output": "output",
                    "tool_call_id": "tool_call_id",
                },
            ],
            stream=True,
        )
        assert_matches_type(RunObject, run, path=["response"])

    @parametrize
    async def test_raw_response_submit_tool_outputs(self, async_client: AsyncOmnistack) -> None:
        response = await async_client.threads.runs.with_raw_response.submit_tool_outputs(
            run_id="run_id",
            thread_id="thread_id",
            tool_outputs=[{}, {}, {}],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        run = await response.parse()
        assert_matches_type(RunObject, run, path=["response"])

    @parametrize
    async def test_streaming_response_submit_tool_outputs(self, async_client: AsyncOmnistack) -> None:
        async with async_client.threads.runs.with_streaming_response.submit_tool_outputs(
            run_id="run_id",
            thread_id="thread_id",
            tool_outputs=[{}, {}, {}],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            run = await response.parse()
            assert_matches_type(RunObject, run, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_submit_tool_outputs(self, async_client: AsyncOmnistack) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `thread_id` but received ''"):
            await async_client.threads.runs.with_raw_response.submit_tool_outputs(
                run_id="run_id",
                thread_id="",
                tool_outputs=[{}, {}, {}],
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `run_id` but received ''"):
            await async_client.threads.runs.with_raw_response.submit_tool_outputs(
                run_id="",
                thread_id="thread_id",
                tool_outputs=[{}, {}, {}],
            )

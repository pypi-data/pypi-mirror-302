# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from omnistack import Omnistack, AsyncOmnistack
from tests.utils import assert_matches_type
from omnistack.types import ThreadDeleteResponse
from omnistack.types.assistants import ThreadObject

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestThreads:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Omnistack) -> None:
        thread = client.threads.create()
        assert_matches_type(ThreadObject, thread, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Omnistack) -> None:
        thread = client.threads.create(
            messages=[
                {
                    "content": "string",
                    "role": "user",
                    "attachments": [
                        {
                            "file_id": "file_id",
                            "tools": [
                                {"type": "code_interpreter"},
                                {"type": "code_interpreter"},
                                {"type": "code_interpreter"},
                            ],
                        },
                        {
                            "file_id": "file_id",
                            "tools": [
                                {"type": "code_interpreter"},
                                {"type": "code_interpreter"},
                                {"type": "code_interpreter"},
                            ],
                        },
                        {
                            "file_id": "file_id",
                            "tools": [
                                {"type": "code_interpreter"},
                                {"type": "code_interpreter"},
                                {"type": "code_interpreter"},
                            ],
                        },
                    ],
                    "metadata": {},
                },
                {
                    "content": "string",
                    "role": "user",
                    "attachments": [
                        {
                            "file_id": "file_id",
                            "tools": [
                                {"type": "code_interpreter"},
                                {"type": "code_interpreter"},
                                {"type": "code_interpreter"},
                            ],
                        },
                        {
                            "file_id": "file_id",
                            "tools": [
                                {"type": "code_interpreter"},
                                {"type": "code_interpreter"},
                                {"type": "code_interpreter"},
                            ],
                        },
                        {
                            "file_id": "file_id",
                            "tools": [
                                {"type": "code_interpreter"},
                                {"type": "code_interpreter"},
                                {"type": "code_interpreter"},
                            ],
                        },
                    ],
                    "metadata": {},
                },
                {
                    "content": "string",
                    "role": "user",
                    "attachments": [
                        {
                            "file_id": "file_id",
                            "tools": [
                                {"type": "code_interpreter"},
                                {"type": "code_interpreter"},
                                {"type": "code_interpreter"},
                            ],
                        },
                        {
                            "file_id": "file_id",
                            "tools": [
                                {"type": "code_interpreter"},
                                {"type": "code_interpreter"},
                                {"type": "code_interpreter"},
                            ],
                        },
                        {
                            "file_id": "file_id",
                            "tools": [
                                {"type": "code_interpreter"},
                                {"type": "code_interpreter"},
                                {"type": "code_interpreter"},
                            ],
                        },
                    ],
                    "metadata": {},
                },
            ],
            metadata={},
            tool_resources={
                "code_interpreter": {"file_ids": ["string", "string", "string"]},
                "file_search": {
                    "vector_store_ids": ["string"],
                    "vector_stores": [
                        {
                            "chunking_strategy": {"type": "auto"},
                            "file_ids": ["string", "string", "string"],
                            "metadata": {},
                        }
                    ],
                },
            },
        )
        assert_matches_type(ThreadObject, thread, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Omnistack) -> None:
        response = client.threads.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        thread = response.parse()
        assert_matches_type(ThreadObject, thread, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Omnistack) -> None:
        with client.threads.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            thread = response.parse()
            assert_matches_type(ThreadObject, thread, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Omnistack) -> None:
        thread = client.threads.retrieve(
            "thread_id",
        )
        assert_matches_type(ThreadObject, thread, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Omnistack) -> None:
        response = client.threads.with_raw_response.retrieve(
            "thread_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        thread = response.parse()
        assert_matches_type(ThreadObject, thread, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Omnistack) -> None:
        with client.threads.with_streaming_response.retrieve(
            "thread_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            thread = response.parse()
            assert_matches_type(ThreadObject, thread, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Omnistack) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `thread_id` but received ''"):
            client.threads.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_update(self, client: Omnistack) -> None:
        thread = client.threads.update(
            thread_id="thread_id",
        )
        assert_matches_type(ThreadObject, thread, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Omnistack) -> None:
        thread = client.threads.update(
            thread_id="thread_id",
            metadata={},
            tool_resources={
                "code_interpreter": {"file_ids": ["string", "string", "string"]},
                "file_search": {"vector_store_ids": ["string"]},
            },
        )
        assert_matches_type(ThreadObject, thread, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Omnistack) -> None:
        response = client.threads.with_raw_response.update(
            thread_id="thread_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        thread = response.parse()
        assert_matches_type(ThreadObject, thread, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Omnistack) -> None:
        with client.threads.with_streaming_response.update(
            thread_id="thread_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            thread = response.parse()
            assert_matches_type(ThreadObject, thread, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Omnistack) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `thread_id` but received ''"):
            client.threads.with_raw_response.update(
                thread_id="",
            )

    @parametrize
    def test_method_delete(self, client: Omnistack) -> None:
        thread = client.threads.delete(
            "thread_id",
        )
        assert_matches_type(ThreadDeleteResponse, thread, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: Omnistack) -> None:
        response = client.threads.with_raw_response.delete(
            "thread_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        thread = response.parse()
        assert_matches_type(ThreadDeleteResponse, thread, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: Omnistack) -> None:
        with client.threads.with_streaming_response.delete(
            "thread_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            thread = response.parse()
            assert_matches_type(ThreadDeleteResponse, thread, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Omnistack) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `thread_id` but received ''"):
            client.threads.with_raw_response.delete(
                "",
            )


class TestAsyncThreads:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncOmnistack) -> None:
        thread = await async_client.threads.create()
        assert_matches_type(ThreadObject, thread, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncOmnistack) -> None:
        thread = await async_client.threads.create(
            messages=[
                {
                    "content": "string",
                    "role": "user",
                    "attachments": [
                        {
                            "file_id": "file_id",
                            "tools": [
                                {"type": "code_interpreter"},
                                {"type": "code_interpreter"},
                                {"type": "code_interpreter"},
                            ],
                        },
                        {
                            "file_id": "file_id",
                            "tools": [
                                {"type": "code_interpreter"},
                                {"type": "code_interpreter"},
                                {"type": "code_interpreter"},
                            ],
                        },
                        {
                            "file_id": "file_id",
                            "tools": [
                                {"type": "code_interpreter"},
                                {"type": "code_interpreter"},
                                {"type": "code_interpreter"},
                            ],
                        },
                    ],
                    "metadata": {},
                },
                {
                    "content": "string",
                    "role": "user",
                    "attachments": [
                        {
                            "file_id": "file_id",
                            "tools": [
                                {"type": "code_interpreter"},
                                {"type": "code_interpreter"},
                                {"type": "code_interpreter"},
                            ],
                        },
                        {
                            "file_id": "file_id",
                            "tools": [
                                {"type": "code_interpreter"},
                                {"type": "code_interpreter"},
                                {"type": "code_interpreter"},
                            ],
                        },
                        {
                            "file_id": "file_id",
                            "tools": [
                                {"type": "code_interpreter"},
                                {"type": "code_interpreter"},
                                {"type": "code_interpreter"},
                            ],
                        },
                    ],
                    "metadata": {},
                },
                {
                    "content": "string",
                    "role": "user",
                    "attachments": [
                        {
                            "file_id": "file_id",
                            "tools": [
                                {"type": "code_interpreter"},
                                {"type": "code_interpreter"},
                                {"type": "code_interpreter"},
                            ],
                        },
                        {
                            "file_id": "file_id",
                            "tools": [
                                {"type": "code_interpreter"},
                                {"type": "code_interpreter"},
                                {"type": "code_interpreter"},
                            ],
                        },
                        {
                            "file_id": "file_id",
                            "tools": [
                                {"type": "code_interpreter"},
                                {"type": "code_interpreter"},
                                {"type": "code_interpreter"},
                            ],
                        },
                    ],
                    "metadata": {},
                },
            ],
            metadata={},
            tool_resources={
                "code_interpreter": {"file_ids": ["string", "string", "string"]},
                "file_search": {
                    "vector_store_ids": ["string"],
                    "vector_stores": [
                        {
                            "chunking_strategy": {"type": "auto"},
                            "file_ids": ["string", "string", "string"],
                            "metadata": {},
                        }
                    ],
                },
            },
        )
        assert_matches_type(ThreadObject, thread, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncOmnistack) -> None:
        response = await async_client.threads.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        thread = await response.parse()
        assert_matches_type(ThreadObject, thread, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncOmnistack) -> None:
        async with async_client.threads.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            thread = await response.parse()
            assert_matches_type(ThreadObject, thread, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncOmnistack) -> None:
        thread = await async_client.threads.retrieve(
            "thread_id",
        )
        assert_matches_type(ThreadObject, thread, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncOmnistack) -> None:
        response = await async_client.threads.with_raw_response.retrieve(
            "thread_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        thread = await response.parse()
        assert_matches_type(ThreadObject, thread, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncOmnistack) -> None:
        async with async_client.threads.with_streaming_response.retrieve(
            "thread_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            thread = await response.parse()
            assert_matches_type(ThreadObject, thread, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncOmnistack) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `thread_id` but received ''"):
            await async_client.threads.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncOmnistack) -> None:
        thread = await async_client.threads.update(
            thread_id="thread_id",
        )
        assert_matches_type(ThreadObject, thread, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncOmnistack) -> None:
        thread = await async_client.threads.update(
            thread_id="thread_id",
            metadata={},
            tool_resources={
                "code_interpreter": {"file_ids": ["string", "string", "string"]},
                "file_search": {"vector_store_ids": ["string"]},
            },
        )
        assert_matches_type(ThreadObject, thread, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncOmnistack) -> None:
        response = await async_client.threads.with_raw_response.update(
            thread_id="thread_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        thread = await response.parse()
        assert_matches_type(ThreadObject, thread, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncOmnistack) -> None:
        async with async_client.threads.with_streaming_response.update(
            thread_id="thread_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            thread = await response.parse()
            assert_matches_type(ThreadObject, thread, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncOmnistack) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `thread_id` but received ''"):
            await async_client.threads.with_raw_response.update(
                thread_id="",
            )

    @parametrize
    async def test_method_delete(self, async_client: AsyncOmnistack) -> None:
        thread = await async_client.threads.delete(
            "thread_id",
        )
        assert_matches_type(ThreadDeleteResponse, thread, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncOmnistack) -> None:
        response = await async_client.threads.with_raw_response.delete(
            "thread_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        thread = await response.parse()
        assert_matches_type(ThreadDeleteResponse, thread, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncOmnistack) -> None:
        async with async_client.threads.with_streaming_response.delete(
            "thread_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            thread = await response.parse()
            assert_matches_type(ThreadDeleteResponse, thread, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncOmnistack) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `thread_id` but received ''"):
            await async_client.threads.with_raw_response.delete(
                "",
            )

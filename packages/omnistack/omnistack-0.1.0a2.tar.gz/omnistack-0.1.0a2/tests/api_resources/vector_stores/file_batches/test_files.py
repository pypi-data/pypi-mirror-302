# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from omnistack import Omnistack, AsyncOmnistack
from tests.utils import assert_matches_type
from omnistack.types.vector_stores.file_batches import FileListResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestFiles:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_list(self, client: Omnistack) -> None:
        file = client.vector_stores.file_batches.files.list(
            batch_id="batch_id",
            vector_store_id="vector_store_id",
        )
        assert_matches_type(FileListResponse, file, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Omnistack) -> None:
        file = client.vector_stores.file_batches.files.list(
            batch_id="batch_id",
            vector_store_id="vector_store_id",
            after="after",
            before="before",
            filter="in_progress",
            limit=0,
            order="asc",
        )
        assert_matches_type(FileListResponse, file, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Omnistack) -> None:
        response = client.vector_stores.file_batches.files.with_raw_response.list(
            batch_id="batch_id",
            vector_store_id="vector_store_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        file = response.parse()
        assert_matches_type(FileListResponse, file, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Omnistack) -> None:
        with client.vector_stores.file_batches.files.with_streaming_response.list(
            batch_id="batch_id",
            vector_store_id="vector_store_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            file = response.parse()
            assert_matches_type(FileListResponse, file, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: Omnistack) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `vector_store_id` but received ''"):
            client.vector_stores.file_batches.files.with_raw_response.list(
                batch_id="batch_id",
                vector_store_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `batch_id` but received ''"):
            client.vector_stores.file_batches.files.with_raw_response.list(
                batch_id="",
                vector_store_id="vector_store_id",
            )


class TestAsyncFiles:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_list(self, async_client: AsyncOmnistack) -> None:
        file = await async_client.vector_stores.file_batches.files.list(
            batch_id="batch_id",
            vector_store_id="vector_store_id",
        )
        assert_matches_type(FileListResponse, file, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncOmnistack) -> None:
        file = await async_client.vector_stores.file_batches.files.list(
            batch_id="batch_id",
            vector_store_id="vector_store_id",
            after="after",
            before="before",
            filter="in_progress",
            limit=0,
            order="asc",
        )
        assert_matches_type(FileListResponse, file, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncOmnistack) -> None:
        response = await async_client.vector_stores.file_batches.files.with_raw_response.list(
            batch_id="batch_id",
            vector_store_id="vector_store_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        file = await response.parse()
        assert_matches_type(FileListResponse, file, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncOmnistack) -> None:
        async with async_client.vector_stores.file_batches.files.with_streaming_response.list(
            batch_id="batch_id",
            vector_store_id="vector_store_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            file = await response.parse()
            assert_matches_type(FileListResponse, file, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncOmnistack) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `vector_store_id` but received ''"):
            await async_client.vector_stores.file_batches.files.with_raw_response.list(
                batch_id="batch_id",
                vector_store_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `batch_id` but received ''"):
            await async_client.vector_stores.file_batches.files.with_raw_response.list(
                batch_id="",
                vector_store_id="vector_store_id",
            )

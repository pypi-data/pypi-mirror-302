# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from omnistack import Omnistack, AsyncOmnistack
from tests.utils import assert_matches_type
from omnistack.types import ImageResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestGenerations:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Omnistack) -> None:
        generation = client.images.generations.create(
            prompt="A cute baby sea otter",
        )
        assert_matches_type(ImageResponse, generation, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Omnistack) -> None:
        generation = client.images.generations.create(
            prompt="A cute baby sea otter",
            model="dall-e-3",
            n=1,
            quality="standard",
            response_format="url",
            size="256x256",
            style="vivid",
            user="user-1234",
        )
        assert_matches_type(ImageResponse, generation, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Omnistack) -> None:
        response = client.images.generations.with_raw_response.create(
            prompt="A cute baby sea otter",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        generation = response.parse()
        assert_matches_type(ImageResponse, generation, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Omnistack) -> None:
        with client.images.generations.with_streaming_response.create(
            prompt="A cute baby sea otter",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            generation = response.parse()
            assert_matches_type(ImageResponse, generation, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncGenerations:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncOmnistack) -> None:
        generation = await async_client.images.generations.create(
            prompt="A cute baby sea otter",
        )
        assert_matches_type(ImageResponse, generation, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncOmnistack) -> None:
        generation = await async_client.images.generations.create(
            prompt="A cute baby sea otter",
            model="dall-e-3",
            n=1,
            quality="standard",
            response_format="url",
            size="256x256",
            style="vivid",
            user="user-1234",
        )
        assert_matches_type(ImageResponse, generation, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncOmnistack) -> None:
        response = await async_client.images.generations.with_raw_response.create(
            prompt="A cute baby sea otter",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        generation = await response.parse()
        assert_matches_type(ImageResponse, generation, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncOmnistack) -> None:
        async with async_client.images.generations.with_streaming_response.create(
            prompt="A cute baby sea otter",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            generation = await response.parse()
            assert_matches_type(ImageResponse, generation, path=["response"])

        assert cast(Any, response.is_closed) is True

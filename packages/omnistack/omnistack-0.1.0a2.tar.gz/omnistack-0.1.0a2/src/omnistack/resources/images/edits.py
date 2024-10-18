# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Mapping, Optional, cast
from typing_extensions import Literal

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven, FileTypes
from ..._utils import (
    extract_files,
    maybe_transform,
    deepcopy_minimal,
    async_maybe_transform,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.images import edit_create_params
from ...types.image_response import ImageResponse

__all__ = ["EditsResource", "AsyncEditsResource"]


class EditsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> EditsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/omnistack-python#accessing-raw-response-data-eg-headers
        """
        return EditsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> EditsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/omnistack-python#with_streaming_response
        """
        return EditsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        image: FileTypes,
        prompt: str,
        mask: FileTypes | NotGiven = NOT_GIVEN,
        model: Union[str, Literal["dall-e-2"], None] | NotGiven = NOT_GIVEN,
        n: Optional[int] | NotGiven = NOT_GIVEN,
        response_format: Optional[Literal["url", "b64_json"]] | NotGiven = NOT_GIVEN,
        size: Optional[Literal["256x256", "512x512", "1024x1024"]] | NotGiven = NOT_GIVEN,
        user: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ImageResponse:
        """
        Creates an edited or extended image given an original image and a prompt.

        Args:
          image: The image to edit. Must be a valid PNG file, less than 4MB, and square. If mask
              is not provided, image must have transparency, which will be used as the mask.

          prompt: A text description of the desired image(s). The maximum length is 1000
              characters.

          mask: An additional image whose fully transparent areas (e.g. where alpha is zero)
              indicate where `image` should be edited. Must be a valid PNG file, less than
              4MB, and have the same dimensions as `image`.

          model: The model to use for image generation. Only `dall-e-2` is supported at this
              time.

          n: The number of images to generate. Must be between 1 and 10.

          response_format: The format in which the generated images are returned. Must be one of `url` or
              `b64_json`. URLs are only valid for 60 minutes after the image has been
              generated.

          size: The size of the generated images. Must be one of `256x256`, `512x512`, or
              `1024x1024`.

          user: A unique identifier representing your end-user, which can help OpenAI to monitor
              and detect abuse. [Learn more](/docs/guides/safety-best-practices/end-user-ids).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        body = deepcopy_minimal(
            {
                "image": image,
                "prompt": prompt,
                "mask": mask,
                "model": model,
                "n": n,
                "response_format": response_format,
                "size": size,
                "user": user,
            }
        )
        files = extract_files(cast(Mapping[str, object], body), paths=[["image"], ["mask"]])
        # It should be noted that the actual Content-Type header that will be
        # sent to the server will contain a `boundary` parameter, e.g.
        # multipart/form-data; boundary=---abc--
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return self._post(
            "/images/edits",
            body=maybe_transform(body, edit_create_params.EditCreateParams),
            files=files,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ImageResponse,
        )


class AsyncEditsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncEditsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/omnistack-python#accessing-raw-response-data-eg-headers
        """
        return AsyncEditsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncEditsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/omnistack-python#with_streaming_response
        """
        return AsyncEditsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        image: FileTypes,
        prompt: str,
        mask: FileTypes | NotGiven = NOT_GIVEN,
        model: Union[str, Literal["dall-e-2"], None] | NotGiven = NOT_GIVEN,
        n: Optional[int] | NotGiven = NOT_GIVEN,
        response_format: Optional[Literal["url", "b64_json"]] | NotGiven = NOT_GIVEN,
        size: Optional[Literal["256x256", "512x512", "1024x1024"]] | NotGiven = NOT_GIVEN,
        user: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ImageResponse:
        """
        Creates an edited or extended image given an original image and a prompt.

        Args:
          image: The image to edit. Must be a valid PNG file, less than 4MB, and square. If mask
              is not provided, image must have transparency, which will be used as the mask.

          prompt: A text description of the desired image(s). The maximum length is 1000
              characters.

          mask: An additional image whose fully transparent areas (e.g. where alpha is zero)
              indicate where `image` should be edited. Must be a valid PNG file, less than
              4MB, and have the same dimensions as `image`.

          model: The model to use for image generation. Only `dall-e-2` is supported at this
              time.

          n: The number of images to generate. Must be between 1 and 10.

          response_format: The format in which the generated images are returned. Must be one of `url` or
              `b64_json`. URLs are only valid for 60 minutes after the image has been
              generated.

          size: The size of the generated images. Must be one of `256x256`, `512x512`, or
              `1024x1024`.

          user: A unique identifier representing your end-user, which can help OpenAI to monitor
              and detect abuse. [Learn more](/docs/guides/safety-best-practices/end-user-ids).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        body = deepcopy_minimal(
            {
                "image": image,
                "prompt": prompt,
                "mask": mask,
                "model": model,
                "n": n,
                "response_format": response_format,
                "size": size,
                "user": user,
            }
        )
        files = extract_files(cast(Mapping[str, object], body), paths=[["image"], ["mask"]])
        # It should be noted that the actual Content-Type header that will be
        # sent to the server will contain a `boundary` parameter, e.g.
        # multipart/form-data; boundary=---abc--
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return await self._post(
            "/images/edits",
            body=await async_maybe_transform(body, edit_create_params.EditCreateParams),
            files=files,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ImageResponse,
        )


class EditsResourceWithRawResponse:
    def __init__(self, edits: EditsResource) -> None:
        self._edits = edits

        self.create = to_raw_response_wrapper(
            edits.create,
        )


class AsyncEditsResourceWithRawResponse:
    def __init__(self, edits: AsyncEditsResource) -> None:
        self._edits = edits

        self.create = async_to_raw_response_wrapper(
            edits.create,
        )


class EditsResourceWithStreamingResponse:
    def __init__(self, edits: EditsResource) -> None:
        self._edits = edits

        self.create = to_streamed_response_wrapper(
            edits.create,
        )


class AsyncEditsResourceWithStreamingResponse:
    def __init__(self, edits: AsyncEditsResource) -> None:
        self._edits = edits

        self.create = async_to_streamed_response_wrapper(
            edits.create,
        )

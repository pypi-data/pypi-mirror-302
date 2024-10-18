# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.projects.service_account_delete_response import ServiceAccountDeleteResponse

__all__ = ["ServiceAccountsResource", "AsyncServiceAccountsResource"]


class ServiceAccountsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ServiceAccountsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/omnistack-python#accessing-raw-response-data-eg-headers
        """
        return ServiceAccountsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ServiceAccountsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/omnistack-python#with_streaming_response
        """
        return ServiceAccountsResourceWithStreamingResponse(self)

    def delete(
        self,
        service_account_id: str,
        *,
        project_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ServiceAccountDeleteResponse:
        """
        Deletes a service account from the project.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not project_id:
            raise ValueError(f"Expected a non-empty value for `project_id` but received {project_id!r}")
        if not service_account_id:
            raise ValueError(f"Expected a non-empty value for `service_account_id` but received {service_account_id!r}")
        return self._delete(
            f"/organization/projects/{project_id}/service_accounts/{service_account_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ServiceAccountDeleteResponse,
        )


class AsyncServiceAccountsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncServiceAccountsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/omnistack-python#accessing-raw-response-data-eg-headers
        """
        return AsyncServiceAccountsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncServiceAccountsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/omnistack-python#with_streaming_response
        """
        return AsyncServiceAccountsResourceWithStreamingResponse(self)

    async def delete(
        self,
        service_account_id: str,
        *,
        project_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ServiceAccountDeleteResponse:
        """
        Deletes a service account from the project.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not project_id:
            raise ValueError(f"Expected a non-empty value for `project_id` but received {project_id!r}")
        if not service_account_id:
            raise ValueError(f"Expected a non-empty value for `service_account_id` but received {service_account_id!r}")
        return await self._delete(
            f"/organization/projects/{project_id}/service_accounts/{service_account_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ServiceAccountDeleteResponse,
        )


class ServiceAccountsResourceWithRawResponse:
    def __init__(self, service_accounts: ServiceAccountsResource) -> None:
        self._service_accounts = service_accounts

        self.delete = to_raw_response_wrapper(
            service_accounts.delete,
        )


class AsyncServiceAccountsResourceWithRawResponse:
    def __init__(self, service_accounts: AsyncServiceAccountsResource) -> None:
        self._service_accounts = service_accounts

        self.delete = async_to_raw_response_wrapper(
            service_accounts.delete,
        )


class ServiceAccountsResourceWithStreamingResponse:
    def __init__(self, service_accounts: ServiceAccountsResource) -> None:
        self._service_accounts = service_accounts

        self.delete = to_streamed_response_wrapper(
            service_accounts.delete,
        )


class AsyncServiceAccountsResourceWithStreamingResponse:
    def __init__(self, service_accounts: AsyncServiceAccountsResource) -> None:
        self._service_accounts = service_accounts

        self.delete = async_to_streamed_response_wrapper(
            service_accounts.delete,
        )

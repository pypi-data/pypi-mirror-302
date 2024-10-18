# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .api_keys import (
    APIKeysResource,
    AsyncAPIKeysResource,
    APIKeysResourceWithRawResponse,
    AsyncAPIKeysResourceWithRawResponse,
    APIKeysResourceWithStreamingResponse,
    AsyncAPIKeysResourceWithStreamingResponse,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from .service_accounts import (
    ServiceAccountsResource,
    AsyncServiceAccountsResource,
    ServiceAccountsResourceWithRawResponse,
    AsyncServiceAccountsResourceWithRawResponse,
    ServiceAccountsResourceWithStreamingResponse,
    AsyncServiceAccountsResourceWithStreamingResponse,
)

__all__ = ["ProjectsResource", "AsyncProjectsResource"]


class ProjectsResource(SyncAPIResource):
    @cached_property
    def service_accounts(self) -> ServiceAccountsResource:
        return ServiceAccountsResource(self._client)

    @cached_property
    def api_keys(self) -> APIKeysResource:
        return APIKeysResource(self._client)

    @cached_property
    def with_raw_response(self) -> ProjectsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/omnistack-python#accessing-raw-response-data-eg-headers
        """
        return ProjectsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ProjectsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/omnistack-python#with_streaming_response
        """
        return ProjectsResourceWithStreamingResponse(self)


class AsyncProjectsResource(AsyncAPIResource):
    @cached_property
    def service_accounts(self) -> AsyncServiceAccountsResource:
        return AsyncServiceAccountsResource(self._client)

    @cached_property
    def api_keys(self) -> AsyncAPIKeysResource:
        return AsyncAPIKeysResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncProjectsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/omnistack-python#accessing-raw-response-data-eg-headers
        """
        return AsyncProjectsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncProjectsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/omnistack-python#with_streaming_response
        """
        return AsyncProjectsResourceWithStreamingResponse(self)


class ProjectsResourceWithRawResponse:
    def __init__(self, projects: ProjectsResource) -> None:
        self._projects = projects

    @cached_property
    def service_accounts(self) -> ServiceAccountsResourceWithRawResponse:
        return ServiceAccountsResourceWithRawResponse(self._projects.service_accounts)

    @cached_property
    def api_keys(self) -> APIKeysResourceWithRawResponse:
        return APIKeysResourceWithRawResponse(self._projects.api_keys)


class AsyncProjectsResourceWithRawResponse:
    def __init__(self, projects: AsyncProjectsResource) -> None:
        self._projects = projects

    @cached_property
    def service_accounts(self) -> AsyncServiceAccountsResourceWithRawResponse:
        return AsyncServiceAccountsResourceWithRawResponse(self._projects.service_accounts)

    @cached_property
    def api_keys(self) -> AsyncAPIKeysResourceWithRawResponse:
        return AsyncAPIKeysResourceWithRawResponse(self._projects.api_keys)


class ProjectsResourceWithStreamingResponse:
    def __init__(self, projects: ProjectsResource) -> None:
        self._projects = projects

    @cached_property
    def service_accounts(self) -> ServiceAccountsResourceWithStreamingResponse:
        return ServiceAccountsResourceWithStreamingResponse(self._projects.service_accounts)

    @cached_property
    def api_keys(self) -> APIKeysResourceWithStreamingResponse:
        return APIKeysResourceWithStreamingResponse(self._projects.api_keys)


class AsyncProjectsResourceWithStreamingResponse:
    def __init__(self, projects: AsyncProjectsResource) -> None:
        self._projects = projects

    @cached_property
    def service_accounts(self) -> AsyncServiceAccountsResourceWithStreamingResponse:
        return AsyncServiceAccountsResourceWithStreamingResponse(self._projects.service_accounts)

    @cached_property
    def api_keys(self) -> AsyncAPIKeysResourceWithStreamingResponse:
        return AsyncAPIKeysResourceWithStreamingResponse(self._projects.api_keys)

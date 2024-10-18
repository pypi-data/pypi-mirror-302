# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import (
    maybe_transform,
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
from ...types.organization import audit_log_list_params
from ...types.organization.audit_log_list_response import AuditLogListResponse

__all__ = ["AuditLogsResource", "AsyncAuditLogsResource"]


class AuditLogsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AuditLogsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/omnistack-python#accessing-raw-response-data-eg-headers
        """
        return AuditLogsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AuditLogsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/omnistack-python#with_streaming_response
        """
        return AuditLogsResourceWithStreamingResponse(self)

    def list(
        self,
        *,
        actor_emails: List[str] | NotGiven = NOT_GIVEN,
        actor_ids: List[str] | NotGiven = NOT_GIVEN,
        after: str | NotGiven = NOT_GIVEN,
        before: str | NotGiven = NOT_GIVEN,
        effective_at: audit_log_list_params.EffectiveAt | NotGiven = NOT_GIVEN,
        event_types: List[
            Literal[
                "api_key.created",
                "api_key.updated",
                "api_key.deleted",
                "invite.sent",
                "invite.accepted",
                "invite.deleted",
                "login.succeeded",
                "login.failed",
                "logout.succeeded",
                "logout.failed",
                "organization.updated",
                "project.created",
                "project.updated",
                "project.archived",
                "service_account.created",
                "service_account.updated",
                "service_account.deleted",
                "user.added",
                "user.updated",
                "user.deleted",
            ]
        ]
        | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        project_ids: List[str] | NotGiven = NOT_GIVEN,
        resource_ids: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AuditLogListResponse:
        """
        List user actions and configuration changes within this organization.

        Args:
          actor_emails: Return only events performed by users with these emails.

          actor_ids: Return only events performed by these actors. Can be a user ID, a service
              account ID, or an api key tracking ID.

          after: A cursor for use in pagination. `after` is an object ID that defines your place
              in the list. For instance, if you make a list request and receive 100 objects,
              ending with obj_foo, your subsequent call can include after=obj_foo in order to
              fetch the next page of the list.

          before: A cursor for use in pagination. `before` is an object ID that defines your place
              in the list. For instance, if you make a list request and receive 100 objects,
              ending with obj_foo, your subsequent call can include before=obj_foo in order to
              fetch the previous page of the list.

          effective_at: Return only events whose `effective_at` (Unix seconds) is in this range.

          event_types: Return only events with a `type` in one of these values. For example,
              `project.created`. For all options, see the documentation for the
              [audit log object](/docs/api-reference/audit-logs/object).

          limit: A limit on the number of objects to be returned. Limit can range between 1 and
              100, and the default is 20.

          project_ids: Return only events for these projects.

          resource_ids: Return only events performed on these targets. For example, a project ID
              updated.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/organization/audit_logs",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "actor_emails": actor_emails,
                        "actor_ids": actor_ids,
                        "after": after,
                        "before": before,
                        "effective_at": effective_at,
                        "event_types": event_types,
                        "limit": limit,
                        "project_ids": project_ids,
                        "resource_ids": resource_ids,
                    },
                    audit_log_list_params.AuditLogListParams,
                ),
            ),
            cast_to=AuditLogListResponse,
        )


class AsyncAuditLogsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncAuditLogsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/omnistack-python#accessing-raw-response-data-eg-headers
        """
        return AsyncAuditLogsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAuditLogsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/omnistack-python#with_streaming_response
        """
        return AsyncAuditLogsResourceWithStreamingResponse(self)

    async def list(
        self,
        *,
        actor_emails: List[str] | NotGiven = NOT_GIVEN,
        actor_ids: List[str] | NotGiven = NOT_GIVEN,
        after: str | NotGiven = NOT_GIVEN,
        before: str | NotGiven = NOT_GIVEN,
        effective_at: audit_log_list_params.EffectiveAt | NotGiven = NOT_GIVEN,
        event_types: List[
            Literal[
                "api_key.created",
                "api_key.updated",
                "api_key.deleted",
                "invite.sent",
                "invite.accepted",
                "invite.deleted",
                "login.succeeded",
                "login.failed",
                "logout.succeeded",
                "logout.failed",
                "organization.updated",
                "project.created",
                "project.updated",
                "project.archived",
                "service_account.created",
                "service_account.updated",
                "service_account.deleted",
                "user.added",
                "user.updated",
                "user.deleted",
            ]
        ]
        | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        project_ids: List[str] | NotGiven = NOT_GIVEN,
        resource_ids: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AuditLogListResponse:
        """
        List user actions and configuration changes within this organization.

        Args:
          actor_emails: Return only events performed by users with these emails.

          actor_ids: Return only events performed by these actors. Can be a user ID, a service
              account ID, or an api key tracking ID.

          after: A cursor for use in pagination. `after` is an object ID that defines your place
              in the list. For instance, if you make a list request and receive 100 objects,
              ending with obj_foo, your subsequent call can include after=obj_foo in order to
              fetch the next page of the list.

          before: A cursor for use in pagination. `before` is an object ID that defines your place
              in the list. For instance, if you make a list request and receive 100 objects,
              ending with obj_foo, your subsequent call can include before=obj_foo in order to
              fetch the previous page of the list.

          effective_at: Return only events whose `effective_at` (Unix seconds) is in this range.

          event_types: Return only events with a `type` in one of these values. For example,
              `project.created`. For all options, see the documentation for the
              [audit log object](/docs/api-reference/audit-logs/object).

          limit: A limit on the number of objects to be returned. Limit can range between 1 and
              100, and the default is 20.

          project_ids: Return only events for these projects.

          resource_ids: Return only events performed on these targets. For example, a project ID
              updated.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/organization/audit_logs",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "actor_emails": actor_emails,
                        "actor_ids": actor_ids,
                        "after": after,
                        "before": before,
                        "effective_at": effective_at,
                        "event_types": event_types,
                        "limit": limit,
                        "project_ids": project_ids,
                        "resource_ids": resource_ids,
                    },
                    audit_log_list_params.AuditLogListParams,
                ),
            ),
            cast_to=AuditLogListResponse,
        )


class AuditLogsResourceWithRawResponse:
    def __init__(self, audit_logs: AuditLogsResource) -> None:
        self._audit_logs = audit_logs

        self.list = to_raw_response_wrapper(
            audit_logs.list,
        )


class AsyncAuditLogsResourceWithRawResponse:
    def __init__(self, audit_logs: AsyncAuditLogsResource) -> None:
        self._audit_logs = audit_logs

        self.list = async_to_raw_response_wrapper(
            audit_logs.list,
        )


class AuditLogsResourceWithStreamingResponse:
    def __init__(self, audit_logs: AuditLogsResource) -> None:
        self._audit_logs = audit_logs

        self.list = to_streamed_response_wrapper(
            audit_logs.list,
        )


class AsyncAuditLogsResourceWithStreamingResponse:
    def __init__(self, audit_logs: AsyncAuditLogsResource) -> None:
        self._audit_logs = audit_logs

        self.list = async_to_streamed_response_wrapper(
            audit_logs.list,
        )

# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

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
from ...types.tools import definition_get_params
from ..._base_client import make_request_options
from ...types.shared.tool_definition import ToolDefinition

__all__ = ["DefinitionResource", "AsyncDefinitionResource"]


class DefinitionResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> DefinitionResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ArcadeAI/arcade-py#accessing-raw-response-data-eg-headers
        """
        return DefinitionResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DefinitionResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ArcadeAI/arcade-py#with_streaming_response
        """
        return DefinitionResourceWithStreamingResponse(self)

    def get(
        self,
        *,
        director_id: str,
        tool_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ToolDefinition:
        """
        Returns the arcade tool specification for a specific tool

        Args:
          director_id: Director ID

          tool_id: Tool ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/v1/tools/definition",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "director_id": director_id,
                        "tool_id": tool_id,
                    },
                    definition_get_params.DefinitionGetParams,
                ),
            ),
            cast_to=ToolDefinition,
        )


class AsyncDefinitionResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncDefinitionResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ArcadeAI/arcade-py#accessing-raw-response-data-eg-headers
        """
        return AsyncDefinitionResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDefinitionResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ArcadeAI/arcade-py#with_streaming_response
        """
        return AsyncDefinitionResourceWithStreamingResponse(self)

    async def get(
        self,
        *,
        director_id: str,
        tool_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ToolDefinition:
        """
        Returns the arcade tool specification for a specific tool

        Args:
          director_id: Director ID

          tool_id: Tool ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/v1/tools/definition",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "director_id": director_id,
                        "tool_id": tool_id,
                    },
                    definition_get_params.DefinitionGetParams,
                ),
            ),
            cast_to=ToolDefinition,
        )


class DefinitionResourceWithRawResponse:
    def __init__(self, definition: DefinitionResource) -> None:
        self._definition = definition

        self.get = to_raw_response_wrapper(
            definition.get,
        )


class AsyncDefinitionResourceWithRawResponse:
    def __init__(self, definition: AsyncDefinitionResource) -> None:
        self._definition = definition

        self.get = async_to_raw_response_wrapper(
            definition.get,
        )


class DefinitionResourceWithStreamingResponse:
    def __init__(self, definition: DefinitionResource) -> None:
        self._definition = definition

        self.get = to_streamed_response_wrapper(
            definition.get,
        )


class AsyncDefinitionResourceWithStreamingResponse:
    def __init__(self, definition: AsyncDefinitionResource) -> None:
        self._definition = definition

        self.get = async_to_streamed_response_wrapper(
            definition.get,
        )

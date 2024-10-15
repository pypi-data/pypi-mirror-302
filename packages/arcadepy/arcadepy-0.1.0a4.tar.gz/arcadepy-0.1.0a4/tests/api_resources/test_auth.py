# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from arcadepy import Arcade, AsyncArcade
from tests.utils import assert_matches_type
from arcadepy.types.shared import AuthorizationResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestAuth:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_authorize(self, client: Arcade) -> None:
        auth = client.auth.authorize(
            auth_requirement={},
            user_id="user_id",
        )
        assert_matches_type(AuthorizationResponse, auth, path=["response"])

    @parametrize
    def test_method_authorize_with_all_params(self, client: Arcade) -> None:
        auth = client.auth.authorize(
            auth_requirement={
                "oauth2": {"scopes": ["string", "string", "string"]},
                "provider_id": "provider_id",
                "provider_type": "provider_type",
            },
            user_id="user_id",
        )
        assert_matches_type(AuthorizationResponse, auth, path=["response"])

    @parametrize
    def test_raw_response_authorize(self, client: Arcade) -> None:
        response = client.auth.with_raw_response.authorize(
            auth_requirement={},
            user_id="user_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        auth = response.parse()
        assert_matches_type(AuthorizationResponse, auth, path=["response"])

    @parametrize
    def test_streaming_response_authorize(self, client: Arcade) -> None:
        with client.auth.with_streaming_response.authorize(
            auth_requirement={},
            user_id="user_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            auth = response.parse()
            assert_matches_type(AuthorizationResponse, auth, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_status(self, client: Arcade) -> None:
        auth = client.auth.status(
            authorization_id="authorizationId",
        )
        assert_matches_type(AuthorizationResponse, auth, path=["response"])

    @parametrize
    def test_method_status_with_all_params(self, client: Arcade) -> None:
        auth = client.auth.status(
            authorization_id="authorizationId",
            scopes="scopes",
            wait=0,
        )
        assert_matches_type(AuthorizationResponse, auth, path=["response"])

    @parametrize
    def test_raw_response_status(self, client: Arcade) -> None:
        response = client.auth.with_raw_response.status(
            authorization_id="authorizationId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        auth = response.parse()
        assert_matches_type(AuthorizationResponse, auth, path=["response"])

    @parametrize
    def test_streaming_response_status(self, client: Arcade) -> None:
        with client.auth.with_streaming_response.status(
            authorization_id="authorizationId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            auth = response.parse()
            assert_matches_type(AuthorizationResponse, auth, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncAuth:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_authorize(self, async_client: AsyncArcade) -> None:
        auth = await async_client.auth.authorize(
            auth_requirement={},
            user_id="user_id",
        )
        assert_matches_type(AuthorizationResponse, auth, path=["response"])

    @parametrize
    async def test_method_authorize_with_all_params(self, async_client: AsyncArcade) -> None:
        auth = await async_client.auth.authorize(
            auth_requirement={
                "oauth2": {"scopes": ["string", "string", "string"]},
                "provider_id": "provider_id",
                "provider_type": "provider_type",
            },
            user_id="user_id",
        )
        assert_matches_type(AuthorizationResponse, auth, path=["response"])

    @parametrize
    async def test_raw_response_authorize(self, async_client: AsyncArcade) -> None:
        response = await async_client.auth.with_raw_response.authorize(
            auth_requirement={},
            user_id="user_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        auth = await response.parse()
        assert_matches_type(AuthorizationResponse, auth, path=["response"])

    @parametrize
    async def test_streaming_response_authorize(self, async_client: AsyncArcade) -> None:
        async with async_client.auth.with_streaming_response.authorize(
            auth_requirement={},
            user_id="user_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            auth = await response.parse()
            assert_matches_type(AuthorizationResponse, auth, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_status(self, async_client: AsyncArcade) -> None:
        auth = await async_client.auth.status(
            authorization_id="authorizationId",
        )
        assert_matches_type(AuthorizationResponse, auth, path=["response"])

    @parametrize
    async def test_method_status_with_all_params(self, async_client: AsyncArcade) -> None:
        auth = await async_client.auth.status(
            authorization_id="authorizationId",
            scopes="scopes",
            wait=0,
        )
        assert_matches_type(AuthorizationResponse, auth, path=["response"])

    @parametrize
    async def test_raw_response_status(self, async_client: AsyncArcade) -> None:
        response = await async_client.auth.with_raw_response.status(
            authorization_id="authorizationId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        auth = await response.parse()
        assert_matches_type(AuthorizationResponse, auth, path=["response"])

    @parametrize
    async def test_streaming_response_status(self, async_client: AsyncArcade) -> None:
        async with async_client.auth.with_streaming_response.status(
            authorization_id="authorizationId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            auth = await response.parse()
            assert_matches_type(AuthorizationResponse, auth, path=["response"])

        assert cast(Any, response.is_closed) is True

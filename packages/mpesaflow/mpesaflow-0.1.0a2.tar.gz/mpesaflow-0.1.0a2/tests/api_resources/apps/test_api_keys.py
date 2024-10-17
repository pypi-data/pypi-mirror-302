# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from mpesaflow import Mpesaflow, AsyncMpesaflow
from tests.utils import assert_matches_type
from mpesaflow.types.apps import (
    APIKeyListResponse,
    APIKeyCreateResponse,
    APIKeyDeleteResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestAPIKeys:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Mpesaflow) -> None:
        api_key = client.apps.api_keys.create(
            app_id="appId",
        )
        assert_matches_type(APIKeyCreateResponse, api_key, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Mpesaflow) -> None:
        api_key = client.apps.api_keys.create(
            app_id="appId",
            key_name="keyName",
        )
        assert_matches_type(APIKeyCreateResponse, api_key, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Mpesaflow) -> None:
        response = client.apps.api_keys.with_raw_response.create(
            app_id="appId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        api_key = response.parse()
        assert_matches_type(APIKeyCreateResponse, api_key, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Mpesaflow) -> None:
        with client.apps.api_keys.with_streaming_response.create(
            app_id="appId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            api_key = response.parse()
            assert_matches_type(APIKeyCreateResponse, api_key, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create(self, client: Mpesaflow) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `app_id` but received ''"):
            client.apps.api_keys.with_raw_response.create(
                app_id="",
            )

    @parametrize
    def test_method_list(self, client: Mpesaflow) -> None:
        api_key = client.apps.api_keys.list(
            app_id="appId",
        )
        assert_matches_type(APIKeyListResponse, api_key, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Mpesaflow) -> None:
        api_key = client.apps.api_keys.list(
            app_id="appId",
            ending_before="ending_before",
            limit=0,
            starting_after="starting_after",
        )
        assert_matches_type(APIKeyListResponse, api_key, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Mpesaflow) -> None:
        response = client.apps.api_keys.with_raw_response.list(
            app_id="appId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        api_key = response.parse()
        assert_matches_type(APIKeyListResponse, api_key, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Mpesaflow) -> None:
        with client.apps.api_keys.with_streaming_response.list(
            app_id="appId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            api_key = response.parse()
            assert_matches_type(APIKeyListResponse, api_key, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: Mpesaflow) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `app_id` but received ''"):
            client.apps.api_keys.with_raw_response.list(
                app_id="",
            )

    @parametrize
    def test_method_delete(self, client: Mpesaflow) -> None:
        api_key = client.apps.api_keys.delete(
            api_key_id="apiKeyId",
            app_id="appId",
        )
        assert_matches_type(APIKeyDeleteResponse, api_key, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: Mpesaflow) -> None:
        response = client.apps.api_keys.with_raw_response.delete(
            api_key_id="apiKeyId",
            app_id="appId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        api_key = response.parse()
        assert_matches_type(APIKeyDeleteResponse, api_key, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: Mpesaflow) -> None:
        with client.apps.api_keys.with_streaming_response.delete(
            api_key_id="apiKeyId",
            app_id="appId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            api_key = response.parse()
            assert_matches_type(APIKeyDeleteResponse, api_key, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Mpesaflow) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `app_id` but received ''"):
            client.apps.api_keys.with_raw_response.delete(
                api_key_id="apiKeyId",
                app_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `api_key_id` but received ''"):
            client.apps.api_keys.with_raw_response.delete(
                api_key_id="",
                app_id="appId",
            )


class TestAsyncAPIKeys:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncMpesaflow) -> None:
        api_key = await async_client.apps.api_keys.create(
            app_id="appId",
        )
        assert_matches_type(APIKeyCreateResponse, api_key, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncMpesaflow) -> None:
        api_key = await async_client.apps.api_keys.create(
            app_id="appId",
            key_name="keyName",
        )
        assert_matches_type(APIKeyCreateResponse, api_key, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncMpesaflow) -> None:
        response = await async_client.apps.api_keys.with_raw_response.create(
            app_id="appId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        api_key = await response.parse()
        assert_matches_type(APIKeyCreateResponse, api_key, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncMpesaflow) -> None:
        async with async_client.apps.api_keys.with_streaming_response.create(
            app_id="appId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            api_key = await response.parse()
            assert_matches_type(APIKeyCreateResponse, api_key, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create(self, async_client: AsyncMpesaflow) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `app_id` but received ''"):
            await async_client.apps.api_keys.with_raw_response.create(
                app_id="",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncMpesaflow) -> None:
        api_key = await async_client.apps.api_keys.list(
            app_id="appId",
        )
        assert_matches_type(APIKeyListResponse, api_key, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncMpesaflow) -> None:
        api_key = await async_client.apps.api_keys.list(
            app_id="appId",
            ending_before="ending_before",
            limit=0,
            starting_after="starting_after",
        )
        assert_matches_type(APIKeyListResponse, api_key, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncMpesaflow) -> None:
        response = await async_client.apps.api_keys.with_raw_response.list(
            app_id="appId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        api_key = await response.parse()
        assert_matches_type(APIKeyListResponse, api_key, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncMpesaflow) -> None:
        async with async_client.apps.api_keys.with_streaming_response.list(
            app_id="appId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            api_key = await response.parse()
            assert_matches_type(APIKeyListResponse, api_key, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncMpesaflow) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `app_id` but received ''"):
            await async_client.apps.api_keys.with_raw_response.list(
                app_id="",
            )

    @parametrize
    async def test_method_delete(self, async_client: AsyncMpesaflow) -> None:
        api_key = await async_client.apps.api_keys.delete(
            api_key_id="apiKeyId",
            app_id="appId",
        )
        assert_matches_type(APIKeyDeleteResponse, api_key, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncMpesaflow) -> None:
        response = await async_client.apps.api_keys.with_raw_response.delete(
            api_key_id="apiKeyId",
            app_id="appId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        api_key = await response.parse()
        assert_matches_type(APIKeyDeleteResponse, api_key, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncMpesaflow) -> None:
        async with async_client.apps.api_keys.with_streaming_response.delete(
            api_key_id="apiKeyId",
            app_id="appId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            api_key = await response.parse()
            assert_matches_type(APIKeyDeleteResponse, api_key, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncMpesaflow) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `app_id` but received ''"):
            await async_client.apps.api_keys.with_raw_response.delete(
                api_key_id="apiKeyId",
                app_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `api_key_id` but received ''"):
            await async_client.apps.api_keys.with_raw_response.delete(
                api_key_id="",
                app_id="appId",
            )

# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from mpesaflow import Mpesaflow, AsyncMpesaflow
from tests.utils import assert_matches_type
from mpesaflow.types import AppListResponse, AppCreateResponse, AppDeleteResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestApps:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Mpesaflow) -> None:
        app = client.apps.create()
        assert_matches_type(AppCreateResponse, app, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Mpesaflow) -> None:
        app = client.apps.create(
            description="description",
            name="name",
        )
        assert_matches_type(AppCreateResponse, app, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Mpesaflow) -> None:
        response = client.apps.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        app = response.parse()
        assert_matches_type(AppCreateResponse, app, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Mpesaflow) -> None:
        with client.apps.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            app = response.parse()
            assert_matches_type(AppCreateResponse, app, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_list(self, client: Mpesaflow) -> None:
        app = client.apps.list()
        assert_matches_type(AppListResponse, app, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Mpesaflow) -> None:
        response = client.apps.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        app = response.parse()
        assert_matches_type(AppListResponse, app, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Mpesaflow) -> None:
        with client.apps.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            app = response.parse()
            assert_matches_type(AppListResponse, app, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: Mpesaflow) -> None:
        app = client.apps.delete(
            "appId",
        )
        assert_matches_type(AppDeleteResponse, app, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: Mpesaflow) -> None:
        response = client.apps.with_raw_response.delete(
            "appId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        app = response.parse()
        assert_matches_type(AppDeleteResponse, app, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: Mpesaflow) -> None:
        with client.apps.with_streaming_response.delete(
            "appId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            app = response.parse()
            assert_matches_type(AppDeleteResponse, app, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Mpesaflow) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `app_id` but received ''"):
            client.apps.with_raw_response.delete(
                "",
            )


class TestAsyncApps:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncMpesaflow) -> None:
        app = await async_client.apps.create()
        assert_matches_type(AppCreateResponse, app, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncMpesaflow) -> None:
        app = await async_client.apps.create(
            description="description",
            name="name",
        )
        assert_matches_type(AppCreateResponse, app, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncMpesaflow) -> None:
        response = await async_client.apps.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        app = await response.parse()
        assert_matches_type(AppCreateResponse, app, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncMpesaflow) -> None:
        async with async_client.apps.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            app = await response.parse()
            assert_matches_type(AppCreateResponse, app, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_list(self, async_client: AsyncMpesaflow) -> None:
        app = await async_client.apps.list()
        assert_matches_type(AppListResponse, app, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncMpesaflow) -> None:
        response = await async_client.apps.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        app = await response.parse()
        assert_matches_type(AppListResponse, app, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncMpesaflow) -> None:
        async with async_client.apps.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            app = await response.parse()
            assert_matches_type(AppListResponse, app, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncMpesaflow) -> None:
        app = await async_client.apps.delete(
            "appId",
        )
        assert_matches_type(AppDeleteResponse, app, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncMpesaflow) -> None:
        response = await async_client.apps.with_raw_response.delete(
            "appId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        app = await response.parse()
        assert_matches_type(AppDeleteResponse, app, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncMpesaflow) -> None:
        async with async_client.apps.with_streaming_response.delete(
            "appId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            app = await response.parse()
            assert_matches_type(AppDeleteResponse, app, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncMpesaflow) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `app_id` but received ''"):
            await async_client.apps.with_raw_response.delete(
                "",
            )

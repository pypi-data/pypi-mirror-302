# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from mpesaflow import Mpesaflow, AsyncMpesaflow
from tests.utils import assert_matches_type
from mpesaflow.types import (
    TransactionListResponse,
    TransactionCreateResponse,
    TransactionRetrieveResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTransactions:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Mpesaflow) -> None:
        transaction = client.transactions.create()
        assert_matches_type(TransactionCreateResponse, transaction, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Mpesaflow) -> None:
        transaction = client.transactions.create(
            account_reference="accountReference",
            amount=0,
            mpesa_request_id="mpesaRequestId",
            phone_number="phoneNumber",
            transaction_desc="transactionDesc",
        )
        assert_matches_type(TransactionCreateResponse, transaction, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Mpesaflow) -> None:
        response = client.transactions.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        transaction = response.parse()
        assert_matches_type(TransactionCreateResponse, transaction, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Mpesaflow) -> None:
        with client.transactions.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            transaction = response.parse()
            assert_matches_type(TransactionCreateResponse, transaction, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Mpesaflow) -> None:
        transaction = client.transactions.retrieve(
            "transactionId",
        )
        assert_matches_type(TransactionRetrieveResponse, transaction, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Mpesaflow) -> None:
        response = client.transactions.with_raw_response.retrieve(
            "transactionId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        transaction = response.parse()
        assert_matches_type(TransactionRetrieveResponse, transaction, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Mpesaflow) -> None:
        with client.transactions.with_streaming_response.retrieve(
            "transactionId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            transaction = response.parse()
            assert_matches_type(TransactionRetrieveResponse, transaction, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Mpesaflow) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transaction_id` but received ''"):
            client.transactions.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_list(self, client: Mpesaflow) -> None:
        transaction = client.transactions.list(
            app_id="appId",
        )
        assert_matches_type(TransactionListResponse, transaction, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Mpesaflow) -> None:
        response = client.transactions.with_raw_response.list(
            app_id="appId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        transaction = response.parse()
        assert_matches_type(TransactionListResponse, transaction, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Mpesaflow) -> None:
        with client.transactions.with_streaming_response.list(
            app_id="appId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            transaction = response.parse()
            assert_matches_type(TransactionListResponse, transaction, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncTransactions:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncMpesaflow) -> None:
        transaction = await async_client.transactions.create()
        assert_matches_type(TransactionCreateResponse, transaction, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncMpesaflow) -> None:
        transaction = await async_client.transactions.create(
            account_reference="accountReference",
            amount=0,
            mpesa_request_id="mpesaRequestId",
            phone_number="phoneNumber",
            transaction_desc="transactionDesc",
        )
        assert_matches_type(TransactionCreateResponse, transaction, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncMpesaflow) -> None:
        response = await async_client.transactions.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        transaction = await response.parse()
        assert_matches_type(TransactionCreateResponse, transaction, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncMpesaflow) -> None:
        async with async_client.transactions.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            transaction = await response.parse()
            assert_matches_type(TransactionCreateResponse, transaction, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncMpesaflow) -> None:
        transaction = await async_client.transactions.retrieve(
            "transactionId",
        )
        assert_matches_type(TransactionRetrieveResponse, transaction, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncMpesaflow) -> None:
        response = await async_client.transactions.with_raw_response.retrieve(
            "transactionId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        transaction = await response.parse()
        assert_matches_type(TransactionRetrieveResponse, transaction, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncMpesaflow) -> None:
        async with async_client.transactions.with_streaming_response.retrieve(
            "transactionId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            transaction = await response.parse()
            assert_matches_type(TransactionRetrieveResponse, transaction, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncMpesaflow) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transaction_id` but received ''"):
            await async_client.transactions.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncMpesaflow) -> None:
        transaction = await async_client.transactions.list(
            app_id="appId",
        )
        assert_matches_type(TransactionListResponse, transaction, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncMpesaflow) -> None:
        response = await async_client.transactions.with_raw_response.list(
            app_id="appId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        transaction = await response.parse()
        assert_matches_type(TransactionListResponse, transaction, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncMpesaflow) -> None:
        async with async_client.transactions.with_streaming_response.list(
            app_id="appId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            transaction = await response.parse()
            assert_matches_type(TransactionListResponse, transaction, path=["response"])

        assert cast(Any, response.is_closed) is True

# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os as _os

import httpx
import pytest
from httpx import URL

import misa_openai
from misa_openai import DEFAULT_TIMEOUT, DEFAULT_MAX_RETRIES


def reset_state() -> None:
    misa_openai._reset_client()
    misa_openai.api_key = None or "My API Key"
    misa_openai.organization = None
    misa_openai.project = None
    misa_openai.base_url = None
    misa_openai.timeout = DEFAULT_TIMEOUT
    misa_openai.max_retries = DEFAULT_MAX_RETRIES
    misa_openai.default_headers = None
    misa_openai.default_query = None
    misa_openai.http_client = None
    misa_openai.api_type = _os.environ.get("OPENAI_API_TYPE")  # type: ignore
    misa_openai.api_version = None
    misa_openai.azure_endpoint = None
    misa_openai.azure_ad_token = None
    misa_openai.azure_ad_token_provider = None


@pytest.fixture(autouse=True)
def reset_state_fixture() -> None:
    reset_state()


def test_base_url_option() -> None:
    assert misa_openai.base_url is None
    assert misa_openai.completions._client.base_url == URL("https://api.openai.com/v1/")

    misa_openai.base_url = "http://foo.com"

    assert misa_openai.base_url == URL("http://foo.com")
    assert misa_openai.completions._client.base_url == URL("http://foo.com")


def test_timeout_option() -> None:
    assert misa_openai.timeout == misa_openai.DEFAULT_TIMEOUT
    assert misa_openai.completions._client.timeout == misa_openai.DEFAULT_TIMEOUT

    misa_openai.timeout = 3

    assert misa_openai.timeout == 3
    assert misa_openai.completions._client.timeout == 3


def test_max_retries_option() -> None:
    assert misa_openai.max_retries == misa_openai.DEFAULT_MAX_RETRIES
    assert misa_openai.completions._client.max_retries == misa_openai.DEFAULT_MAX_RETRIES

    misa_openai.max_retries = 1

    assert misa_openai.max_retries == 1
    assert misa_openai.completions._client.max_retries == 1


def test_default_headers_option() -> None:
    assert misa_openai.default_headers == None

    misa_openai.default_headers = {"Foo": "Bar"}

    assert misa_openai.default_headers["Foo"] == "Bar"
    assert misa_openai.completions._client.default_headers["Foo"] == "Bar"


def test_default_query_option() -> None:
    assert misa_openai.default_query is None
    assert misa_openai.completions._client._custom_query == {}

    misa_openai.default_query = {"Foo": {"nested": 1}}

    assert misa_openai.default_query["Foo"] == {"nested": 1}
    assert misa_openai.completions._client._custom_query["Foo"] == {"nested": 1}


def test_http_client_option() -> None:
    assert misa_openai.http_client is None

    original_http_client = misa_openai.completions._client._client
    assert original_http_client is not None

    new_client = httpx.Client()
    misa_openai.http_client = new_client

    assert misa_openai.completions._client._client is new_client


import contextlib
from typing import Iterator

from misa_openai.lib.azure import AzureOpenAI


@contextlib.contextmanager
def fresh_env() -> Iterator[None]:
    old = _os.environ.copy()

    try:
        _os.environ.clear()
        yield
    finally:
        _os.environ.clear()
        _os.environ.update(old)


def test_only_api_key_results_in_openai_api() -> None:
    with fresh_env():
        misa_openai.api_type = None
        misa_openai.api_key = "example API key"

        assert type(misa_openai.completions._client).__name__ == "_ModuleClient"


def test_azure_api_key_env_without_api_version() -> None:
    with fresh_env():
        misa_openai.api_type = None
        _os.environ["AZURE_OPENAI_API_KEY"] = "example API key"

        with pytest.raises(
            ValueError,
            match=r"Must provide either the `api_version` argument or the `OPENAI_API_VERSION` environment variable",
        ):
            misa_openai.completions._client  # noqa: B018


def test_azure_api_key_and_version_env() -> None:
    with fresh_env():
        misa_openai.api_type = None
        _os.environ["AZURE_OPENAI_API_KEY"] = "example API key"
        _os.environ["OPENAI_API_VERSION"] = "example-version"

        with pytest.raises(
            ValueError,
            match=r"Must provide one of the `base_url` or `azure_endpoint` arguments, or the `AZURE_OPENAI_ENDPOINT` environment variable",
        ):
            misa_openai.completions._client  # noqa: B018


def test_azure_api_key_version_and_endpoint_env() -> None:
    with fresh_env():
        misa_openai.api_type = None
        _os.environ["AZURE_OPENAI_API_KEY"] = "example API key"
        _os.environ["OPENAI_API_VERSION"] = "example-version"
        _os.environ["AZURE_OPENAI_ENDPOINT"] = "https://www.example"

        misa_openai.completions._client  # noqa: B018

        assert misa_openai.api_type == "azure"


def test_azure_azure_ad_token_version_and_endpoint_env() -> None:
    with fresh_env():
        misa_openai.api_type = None
        _os.environ["AZURE_OPENAI_AD_TOKEN"] = "example AD token"
        _os.environ["OPENAI_API_VERSION"] = "example-version"
        _os.environ["AZURE_OPENAI_ENDPOINT"] = "https://www.example"

        client = misa_openai.completions._client
        assert isinstance(client, AzureOpenAI)
        assert client._azure_ad_token == "example AD token"


def test_azure_azure_ad_token_provider_version_and_endpoint_env() -> None:
    with fresh_env():
        misa_openai.api_type = None
        _os.environ["OPENAI_API_VERSION"] = "example-version"
        _os.environ["AZURE_OPENAI_ENDPOINT"] = "https://www.example"
        misa_openai.azure_ad_token_provider = lambda: "token"

        client = misa_openai.completions._client
        assert isinstance(client, AzureOpenAI)
        assert client._azure_ad_token_provider is not None
        assert client._azure_ad_token_provider() == "token"

from unittest.mock import MagicMock

import pytest

from gemini_etl.tokens import CachedTokenCounter, gemini_token_counter


def test_calls_underlying_counter_once_per_text():
    calls = []

    def underlying(text: str) -> int:
        calls.append(text)
        return len(text)

    counter = CachedTokenCounter(underlying)
    counter.count("hello")
    counter.count("hello")
    counter.count("world")

    assert calls == ["hello", "world"]


def test_returns_underlying_value():
    counter = CachedTokenCounter(lambda t: 42)
    assert counter.count("anything") == 42


def test_cache_keyed_by_text_not_identity():
    calls = []

    def underlying(text: str) -> int:
        calls.append(text)
        return len(text)

    counter = CachedTokenCounter(underlying)
    counter.count("same")
    counter.count("same")
    assert len(calls) == 1


def test_empty_string_is_cached_correctly():
    calls = []

    def underlying(text: str) -> int:
        calls.append(text)
        return 0

    counter = CachedTokenCounter(underlying)
    assert counter.count("") == 0
    assert counter.count("") == 0
    assert calls == [""]


def test_gemini_counter_returns_total_tokens():
    fake_result = MagicMock()
    fake_result.total_tokens = 7
    fake_client = MagicMock()
    fake_client.models.count_tokens.return_value = fake_result

    counter = gemini_token_counter(fake_client)
    assert counter("hello") == 7
    fake_client.models.count_tokens.assert_called_once_with(
        model="gemini-2.5-flash", contents="hello",
    )


def test_gemini_counter_falls_back_to_camelCase():
    fake_result = MagicMock(spec=["totalTokens"])  # restrict attrs to camelCase only
    fake_result.totalTokens = 9
    fake_client = MagicMock()
    fake_client.models.count_tokens.return_value = fake_result

    counter = gemini_token_counter(fake_client)
    assert counter("x") == 9


def test_gemini_counter_raises_when_neither_attr_present():
    fake_result = MagicMock(spec=[])  # no attributes at all
    fake_client = MagicMock()
    fake_client.models.count_tokens.return_value = fake_result

    counter = gemini_token_counter(fake_client)
    with pytest.raises(AttributeError, match="total_tokens"):
        counter("x")


def test_gemini_counter_uses_custom_model():
    fake_result = MagicMock()
    fake_result.total_tokens = 1
    fake_client = MagicMock()
    fake_client.models.count_tokens.return_value = fake_result

    counter = gemini_token_counter(fake_client, model="gemini-2.0-pro")
    counter("y")
    fake_client.models.count_tokens.assert_called_with(
        model="gemini-2.0-pro", contents="y",
    )

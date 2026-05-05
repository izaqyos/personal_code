from gemini_etl.tokens import CachedTokenCounter


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

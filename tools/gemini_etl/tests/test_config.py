from pathlib import Path

from gemini_etl.config import Source, get_config


def test_default_config_has_two_sources():
    cfg = get_config()
    names = {s.name for s in cfg.sources}
    assert names == {"personal_KB", "personal_code"}


def test_kb_source_only_markdown():
    cfg = get_config()
    kb = next(s for s in cfg.sources if s.name == "personal_KB")
    assert kb.extensions == {".md"}
    assert isinstance(kb, Source)


def test_code_source_extensions():
    cfg = get_config()
    code = next(s for s in cfg.sources if s.name == "personal_code")
    assert code.extensions == {".py", ".js", ".ts", ".c", ".cpp", ".h", ".bash"}


def test_state_dir_expanded(monkeypatch, tmp_path):
    monkeypatch.setenv("GEMINI_ETL_STATE_DIR", str(tmp_path))
    cfg = get_config()
    assert cfg.state_dir == tmp_path


def test_chunk_token_limit_default():
    cfg = get_config()
    assert cfg.chunk_token_limit == 10_000


def test_max_concurrency_default():
    cfg = get_config()
    assert cfg.max_concurrency == 4


def test_paths_are_absolute():
    cfg = get_config()
    for s in cfg.sources:
        assert Path(s.path).is_absolute()


def test_manifest_path_is_under_state_dir(monkeypatch, tmp_path):
    monkeypatch.setenv("GEMINI_ETL_STATE_DIR", str(tmp_path))
    cfg = get_config()
    assert cfg.manifest_path == tmp_path / "sync_manifest.sqlite"


def test_store_id_path_is_under_state_dir(monkeypatch, tmp_path):
    monkeypatch.setenv("GEMINI_ETL_STATE_DIR", str(tmp_path))
    cfg = get_config()
    assert cfg.store_id_path == tmp_path / "store.txt"


def test_max_concurrency_env_override(monkeypatch):
    monkeypatch.setenv("GEMINI_ETL_MAX_CONCURRENCY", "8")
    cfg = get_config()
    assert cfg.max_concurrency == 8


def test_invalid_int_env_raises_with_helpful_message(monkeypatch):
    import pytest
    monkeypatch.setenv("GEMINI_ETL_MAX_CONCURRENCY", "four")
    with pytest.raises(ValueError, match="GEMINI_ETL_MAX_CONCURRENCY"):
        get_config()

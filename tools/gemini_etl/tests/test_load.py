from unittest.mock import MagicMock

import pytest

from gemini_etl.load import Loader, UploadResult


@pytest.fixture
def mock_client():
    client = MagicMock()
    # Default: store list returns nothing → create returns a fake store.
    client.file_search_stores.list.return_value = []
    fake_store = MagicMock()
    fake_store.name = "fileSearchStores/abc"
    fake_store.display_name = "test-store"
    client.file_search_stores.create.return_value = fake_store
    fake_doc = MagicMock()
    fake_doc.name = "fileSearchStores/abc/documents/d1"
    client.file_search_stores.documents.create.return_value = fake_doc
    fake_file = MagicMock()
    fake_file.name = "files/f1"
    client.files.upload.return_value = fake_file
    return client


def test_ensure_store_creates_when_missing(mock_client):
    loader = Loader(client=mock_client, store_display_name="test-store")
    name = loader.ensure_store()
    assert name == "fileSearchStores/abc"
    mock_client.file_search_stores.create.assert_called_once()


def test_ensure_store_returns_existing(mock_client):
    existing = MagicMock()
    existing.name = "fileSearchStores/existing"
    existing.display_name = "test-store"
    mock_client.file_search_stores.list.return_value = [existing]
    loader = Loader(client=mock_client, store_display_name="test-store")
    assert loader.ensure_store() == "fileSearchStores/existing"
    mock_client.file_search_stores.create.assert_not_called()


def test_upload_returns_document_id(mock_client, tmp_path):
    f = tmp_path / "x.md"
    f.write_text("hello")
    loader = Loader(client=mock_client, store_display_name="test-store")
    loader.ensure_store()
    result = loader.upload(path=f, display_name="personal_KB/x.md")
    assert isinstance(result, UploadResult)
    assert result.document_id == "fileSearchStores/abc/documents/d1"


def test_delete_calls_sdk(mock_client):
    loader = Loader(client=mock_client, store_display_name="test-store")
    loader.delete_document("fileSearchStores/abc/documents/d1")
    mock_client.file_search_stores.documents.delete.assert_called_once_with(
        name="fileSearchStores/abc/documents/d1"
    )


def test_retry_on_429(mock_client, tmp_path):
    """Three 429s then success."""
    f = tmp_path / "x.md"
    f.write_text("hello")

    fake_doc = MagicMock()
    fake_doc.name = "fileSearchStores/abc/documents/dN"
    err = Exception("429 too many requests")

    mock_client.file_search_stores.documents.create.side_effect = [err, err, fake_doc]
    loader = Loader(
        client=mock_client, store_display_name="test-store",
        max_attempts=5, retry_min_seconds=0,
    )
    loader.ensure_store()
    result = loader.upload(path=f, display_name="personal_KB/x.md")
    assert result.document_id.endswith("/dN")

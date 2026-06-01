import os

import pytest


def pytest_collection_modifyitems(config, items):
    if os.environ.get("PYTEST_LIVE") == "1":
        return
    skip_live = pytest.mark.skip(reason="PYTEST_LIVE=1 not set")
    for item in items:
        if "live" in item.keywords:
            item.add_marker(skip_live)

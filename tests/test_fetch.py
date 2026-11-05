import json
from src.fetch import get_company_facts


def test_uses_cache_when_present(tmp_path):
    fake = {"entityName": "TEST CO", "facts": {"us-gaap": {}}}
    (tmp_path / "CIK0000000001.json").write_text(json.dumps(fake))
    assert get_company_facts(1, cache_dir=tmp_path)["entityName"] == "TEST CO"

import pytest
import requests
import src.fetch as fetch


class FakeFailedResponse:
    def raise_for_status(self):
        raise requests.HTTPError("404")


def test_failed_download_raises_and_does_not_cache(tmp_path, monkeypatch):
    monkeypatch.setattr(fetch.requests, "get", lambda *a, **k: FakeFailedResponse())
    with pytest.raises(requests.HTTPError):
        fetch.get_company_facts(123, cache_dir=tmp_path)
    assert not list(tmp_path.iterdir())

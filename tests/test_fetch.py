import json
from src.fetch import get_company_facts


def test_uses_cache_when_present(tmp_path):
    fake = {"entityName": "TEST CO", "facts": {"us-gaap": {}}}
    (tmp_path / "CIK0000000001.json").write_text(json.dumps(fake))
    assert get_company_facts(1, cache_dir=tmp_path)["entityName"] == "TEST CO"
import json
import os
import time
from pathlib import Path

import requests

HEADERS = {"User-Agent": os.environ.get("SEC_USER_AGENT", "Pradhyun Nambi your.email@example.com")}
URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json"


def get_company_facts(cik, cache_dir="data/cache"):
    """Return companyfacts JSON for a CIK, using a local cache if present."""
    cache_path = Path(cache_dir) / f"CIK{cik:010d}.json"
    if cache_path.exists():
        return json.loads(cache_path.read_text())

    resp = requests.get(URL.format(cik=cik), headers=HEADERS, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(json.dumps(data))
    time.sleep(0.2)
    return data


if __name__ == "__main__":
    print("User-Agent being sent:", HEADERS["User-Agent"])
    facts = get_company_facts(200406)
    print(facts["entityName"], "-", len(facts["facts"]["us-gaap"]), "us-gaap tags")
    
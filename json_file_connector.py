import json
from pathlib import Path

SEEN_IDS_FILE = Path("seen_ids.json")

def load_seen_ids() -> set[str]:
    if not SEEN_IDS_FILE.exists():
        return set()
    with open(SEEN_IDS_FILE, "r") as f:
        return set(json.load(f))

def save_seen_ids(ids: set[str]):
    with open(SEEN_IDS_FILE, "w") as f:
        json.dump(sorted(ids), f, indent=2)
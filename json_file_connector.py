import json
from pathlib import Path
from datetime import datetime, timedelta, timezone

from config import SEEN_IDS_FILE

# Сколько дней хранить историю ID, чтобы файл не рос бесконечно
RETENTION_DAYS = 90


def load_seen_ids() -> dict[str, str]:
    """Возвращает {entry_id: iso_date_added}."""
    path = Path(SEEN_IDS_FILE)
    if not path.exists():
        return {}
    with open(path, "r") as f:
        data = json.load(f)
    # поддержка старого формата (просто список без дат)
    if isinstance(data, list):
        return {eid: datetime.now(timezone.utc).isoformat() for eid in data}
    return data


def save_seen_ids(seen: dict[str, str]) -> None:
    """Сохраняет ID с датами, попутно вычищая записи старше RETENTION_DAYS."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=RETENTION_DAYS)
    pruned = {}
    for eid, added_at in seen.items():
        try:
            if datetime.fromisoformat(added_at) >= cutoff:
                pruned[eid] = added_at
        except ValueError:
            pruned[eid] = added_at  # на всякий случай не теряем странные записи

    with open(SEEN_IDS_FILE, "w") as f:
        json.dump(pruned, f, indent=2, ensure_ascii=False, sort_keys=True)


def mark_seen(seen: dict[str, str], entry_ids: list[str]) -> dict[str, str]:
    now = datetime.now(timezone.utc).isoformat()
    for eid in entry_ids:
        seen[eid] = now
    return seen

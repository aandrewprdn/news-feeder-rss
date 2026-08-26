import hashlib
import feedparser

from config import FEEDS


def _entry_id(link: str) -> str:
    return hashlib.sha256(link.encode()).hexdigest()


def fetch_new_entries(seen_ids: dict[str, str]) -> list[dict]:
    """Возвращает список новых статей (которых ещё нет в seen_ids)."""
    new_entries = []

    for url in FEEDS:
        try:
            feed = feedparser.parse(url)
        except Exception as e:
            print(f"Не удалось спарсить {url}: {e}")
            continue

        if feed.bozo and not feed.entries:
            print(f"Проблема с фидом {url}: {feed.bozo_exception}")
            continue

        source_name = getattr(feed.feed, "title", url)

        for entry in feed.entries:
            link = getattr(entry, "link", None)
            if not link:
                continue

            eid = _entry_id(link)
            if eid in seen_ids:
                continue

            new_entries.append({
                "id": eid,
                "title": getattr(entry, "title", "Без названия"),
                "link": link,
                "summary": getattr(entry, "summary", "")[:600],
                "source": source_name,
            })

    return new_entries

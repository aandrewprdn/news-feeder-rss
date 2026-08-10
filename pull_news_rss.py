import feedparser
import hashlib
import json
from pathlib import Path

FEEDS = [
    "https://www.getdbt.com/blog/rss.xml",
    "https://airflow.apache.org/blog/index.xml",
    "https://seattledataguy.substack.com/feed",
    "https://blog.bytebytego.com/feed",
    "https://medium.com/feed/tag/data-engineering"
]

def fetch_new_entries(seen_ids: set[str]) -> list[dict]:
    new_entries = []
    for url in FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            entry_id = hashlib.sha256(entry.link.encode()).hexdigest()
            if entry_id not in seen_ids:
                new_entries.append({
                    "id": entry_id,
                    "title": entry.title,
                    "link": entry.link,
                    "summary": getattr(entry, "summary", ""),
                    "source": feed.feed.title,
                })
    return new_entries

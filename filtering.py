from google import genai

from config import (
    DE_KEYWORDS,
    KEYWORD_FILTER_MAX,
    LLM_FILTER_THRESHOLD,
    FINAL_MAX_ARTICLES,
    GEMINI_MODEL,
)


def _keyword_score(entry: dict) -> int:
    text = (entry["title"] + " " + entry["summary"]).lower()
    return sum(1 for kw in DE_KEYWORDS if kw in text)


def keyword_filter(entries: list[dict]) -> list[dict]:
    scored = [(e, _keyword_score(e)) for e in entries]
    scored = [(e, s) for e, s in scored if s >= 1]
    scored.sort(key=lambda x: x[1], reverse=True)
    return [e for e, _ in scored[:KEYWORD_FILTER_MAX]]


def llm_filter(entries: list[dict], client: genai.Client) -> list[dict]:
    """Просит дешёвую модель отобрать номера релевантных статей."""
    listing = "\n".join(
        f"{i}: {e['title']} — {e['summary'][:150]}"
        for i, e in enumerate(entries)
    )

    prompt = f"""Вот список статей. Верни ТОЛЬКО номера статей (через запятую),
которые релевантны теме Data Engineering (ETL/ELT, orchestration, data
warehousing, streaming, data infrastructure, dbt/Airflow/Spark/Kafka и т.п.).
Игнорируй общие AI/ML новости, если они не про data-инфраструктуру.
Если ни одна статья не подходит — верни пустую строку.

{listing}

Ответ строго в формате: 0,3,7,12 (без пояснений)"""

    response = client.interactions.create(
        model=GEMINI_MODEL,
        input=prompt,
    )

    raw = response.output_text.strip()
    if not raw:
        return []

    indices = []
    for part in raw.split(","):
        part = part.strip()
        if part.isdigit():
            idx = int(part)
            if 0 <= idx < len(entries):
                indices.append(idx)

    return [entries[i] for i in indices]


def select_relevant(entries: list[dict], client: genai.Client) -> list[dict]:
    filtered = keyword_filter(entries)

    if len(filtered) > LLM_FILTER_THRESHOLD:
        filtered = llm_filter(filtered, client)

    return filtered[:FINAL_MAX_ARTICLES]
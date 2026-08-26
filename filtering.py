DE_KEYWORDS = [
    "data engineering", "etl", "elt", "airflow", "dbt", "spark",
    "kafka", "bigquery", "snowflake", "data pipeline", "data warehouse",
    "orchestration", "dagster", "data lake", "lakehouse", "dataframe",
    "batch processing", "streaming", "data modeling", "sql",
]

def relevance_score(entry: dict) -> int:
    text = (entry["title"] + " " + entry["summary"]).lower()
    return sum(1 for kw in DE_KEYWORDS if kw in text)

def filter_relevant(entries: list[dict], min_score=1, max_count=15) -> list[dict]:
    scored = [(e, relevance_score(e)) for e in entries]
    scored = [(e, s) for e, s in scored if s >= min_score]
    scored.sort(key=lambda x: x[1], reverse=True)
    return [e for e, s in scored[:max_count]]
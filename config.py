FEEDS = [
    "https://www.getdbt.com/blog/rss.xml",
    "https://airflow.apache.org/blog/index.xml",
    "https://netflixtechblog.com/feed",
    "https://eng.uber.com/feed/",
    "https://medium.com/feed/airbnb-engineering",
    "https://www.databricks.com/feed",
    "https://aws.amazon.com/blogs/big-data/feed/",
]

DE_KEYWORDS = [
    "data engineering", "etl", "elt", "airflow", "dbt", "spark",
    "kafka", "bigquery", "snowflake", "data pipeline", "data warehouse",
    "orchestration", "dagster", "data lake", "lakehouse", "dataframe",
    "batch processing", "streaming", "data modeling", "data infrastructure",
    "iceberg", "delta lake", "flink", "redshift", "data mesh",
]

# Сколько статей максимум пропускаем через keyword-фильтр дальше по пайплайну
KEYWORD_FILTER_MAX = 30

# Если после keyword-фильтра статей больше этого порога — включаем LLM-классификатор
LLM_FILTER_THRESHOLD = 15

FINAL_MAX_ARTICLES = 15

SEEN_IDS_FILE = "seen_ids.json"

GEMINI_MODEL = "gemini-3.5-flash"


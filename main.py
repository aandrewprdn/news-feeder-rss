import sys
from google import genai

from json_file_connector import mark_seen
from filtering import select_relevant
from json_file_connector import load_seen_ids, save_seen_ids
from llm_summarize import summarize_batch
from pull_news_rss import fetch_new_entries
from telegram import send_telegram


def main() -> None:
    client = genai.Client()

    seen_ids = load_seen_ids()
    print(f"Analyzed ID: {len(seen_ids)}")

    new_entries = fetch_new_entries(seen_ids)
    print(f"New articles: {len(new_entries)}")

    if not new_entries:
        print("No new articles -> no LLM and Telegram request")
        return

    relevant_entries = select_relevant(new_entries, client)
    print(f"Relevant after filtering: {len(relevant_entries)}")

    # В любом случае помечаем все увиденные статьи, чтобы не проверять их снова
    all_ids = [e["id"] for e in new_entries]

    if not relevant_entries:
        print("No relevant article")
        seen_ids = mark_seen(seen_ids, all_ids)
        save_seen_ids(seen_ids)
        return

    digest = summarize_batch(relevant_entries, client)

    if not digest or len(digest.strip()) < 20:
        print("Too short/incorrect summary from LLM -> skip")
        seen_ids = mark_seen(seen_ids, all_ids)
        save_seen_ids(seen_ids)
        return

    send_telegram(digest)
    print("Summary sent")

    seen_ids = mark_seen(seen_ids, all_ids)
    save_seen_ids(seen_ids)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Exception: {e}", file=sys.stderr)
        raise

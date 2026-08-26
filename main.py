from filtering import filter_relevant
from json_file_connector import load_seen_ids, save_seen_ids
from llm_summarize import summarize_batch
from pull_news_rss import fetch_new_entries
from to_telegram_bot_send import send_telegram


def main():
    seen_ids = load_seen_ids()
    new_entries = fetch_new_entries(seen_ids)
    
    # Проверка №1: нет новых статей вообще
    if not new_entries:
        print("Нет новых статей, пропускаю запуск")
        return  # выходим без вызова LLM и Telegram
    
    relevant_entries = filter_relevant(new_entries)
    
    # Проверка №2: после фильтрации ничего релевантного не осталось
    if not relevant_entries:
        print(f"Было {len(new_entries)} статей, но ни одна не прошла фильтр релевантности")
        save_seen_ids(seen_ids | {e["id"] for e in new_entries})  # всё равно помечаем как обработанные
        return
    
    digest = summarize_batch(relevant_entries)
    
    # Проверка №3: LLM вернул пустой/бессмысленный ответ
    if not digest or len(digest.strip()) < 20:
        print("LLM вернул пустой дайджест, пропускаю отправку")
        return
    
    send_telegram(digest)
    save_seen_ids(seen_ids | {e["id"] for e in new_entries})
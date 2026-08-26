from google import genai

from config import GEMINI_MODEL


def summarize_batch(entries: list[dict], client: genai.Client) -> str:
    articles_text = "\n\n".join(
        f"[{i + 1}] {e['title']} ({e['source']})\n{e['summary']}\nСсылка: {e['link']}"
        for i, e in enumerate(entries)
    )

    prompt = f"""Ты готовишь дайджест новостей Data Engineering на русском языке.
Вот список статей:

{articles_text}

Для каждой статьи дай:
- Заголовок на русском (жирным)
- 2-3 предложения сути
- Почему это важно для DE-инженера
- Ссылку на источник

Формат вывода — обычный текст для Telegram с *bold* (Markdown-разметка
Telegram, не используй заголовки #, не используй таблицы).
Начни с короткого вступления вида "Дайджест DE-новостей за {{дата}}" —
дату не пиши, просто "Дайджест DE-новостей:"."""

    response = client.interactions.create(
        model=GEMINI_MODEL,
        input=prompt,
    )

    return response.output_text.strip()

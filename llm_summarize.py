from google import genai

client = genai.Client()

def summarize_batch(entries: list[dict]) -> str:
    articles_text = "\n\n".join(
        f"[{i+1}] {e['title']} ({e['source']})\n{e['summary'][:500]}\nLink: {e['link']}"
        for i, e in enumerate(entries)
    )
    
    prompt = f"""Ты готовишь дайджест новостей Data Engineering на русском.
Вот список статей:

{articles_text}

Для каждой значимой статьи (пропускай неважные/рекламные) дай:
- Заголовок на русском (1 строка)
- 15-20 предложения сути
- Почему это важно для DE-инженера

Формат вывода — Markdown для Telegram (используй *bold*, не используй заголовки #)."""

    response = client.interactions.create(
      model="gemini-3.5-flash",
      input=prompt
    )
    return response.output_text

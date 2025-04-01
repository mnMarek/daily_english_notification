import openai
import requests
import random
import asyncio
from telegram import Bot
import os
from openai import OpenAI
from telegram.constants import ParseMode

# Konfiguracja
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
WORDS_GIST_URL = "https://gist.githubusercontent.com/mnMarek/89e786a51976316ae21be640645a87c8/raw/2edef0aebfc5d30dae45679f338ecf9ff6e338b7/words.json"

# Inicjalizacja klienta OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

def escape_markdown(text):
    escape_chars = '_*[]()~`>#+-=|{}.!'
    return ''.join(f'\\{char}' if char in escape_chars else char for char in text)

async def get_random_word():
    response = requests.get(WORDS_GIST_URL)
    words = response.json()
    return random.choice(words)

async def generate_polish_sentence(word):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Jesteś pomocnym asystentem do nauki angielskiego. Generuj zdania po polsku, które można przetłumaczyć na angielski używając konkretnych zwrotów."},
            #{"role": "user", "content": f"Wygeneruj naturalne zdanie po polsku, które będzie można przetłumaczyć na angielski używając zwrotu '{word}'. W zdaniu polskim NIE używaj angielskiego zwrotu."}
            {"role": "user", "content": f"Ułóż proste zdanie w języku polskim ze słowem: '{word}' tak, abym mógł je sobie przetłumaczyć na język angielski na poziomie B2/B2+. W zdaniu polskim NIE używaj angielskiego zwrotu."}
        ]
    )
    return response.choices[0].message.content

async def translate_to_english(polish_sentence, word):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"Jesteś tłumaczem polsko-angielskim. W tłumaczeniu musisz użyć dokładnie frazy '{word}'."},
            {"role": "user", "content": f"Przetłumacz na angielski używając dokładnie frazy '{word}': '{polish_sentence}'"}
        ]
    )
    translation = response.choices[0].message.content
    
    # Dodatkowa weryfikacja
    if word.lower() not in translation.lower():
        translation = f"{translation} (must include: {word})"
    
    return translation

async def send_telegram_notification(word, polish_sentence, english_translation):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    escaped_polish = escape_markdown(polish_sentence)
    escaped_english = escape_markdown(english_translation)
    message = f"**Tłumaczenie:**\n\nPL: *{escaped_polish}*\n\nKliknij poniżej, aby zobaczyć odpowiedź 👇\n||EN: {escaped_english}||"
    await bot.send_message(
        chat_id=TELEGRAM_CHAT_ID,
        text=message,
        parse_mode=ParseMode.MARKDOWN_V2
    )

async def main():
    word = await get_random_word()
    polish_sentence = await generate_polish_sentence(word)
    english_translation = await translate_to_english(polish_sentence, word)
    await send_telegram_notification(word, polish_sentence, english_translation)

if __name__ == "__main__":
    asyncio.run(main())
import openai
import requests
import random
import asyncio
from telegram import Bot
import os
from openai import OpenAI  # Dodaj tę linię

# Konfiguracja
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
WORDS_GIST_URL = "https://gist.githubusercontent.com/mnMarek/89e786a51976316ae21be640645a87c8/raw/2edef0aebfc5d30dae45679f338ecf9ff6e338b7/words.json"  # Zmień na swój URL

# Inicjalizacja klienta OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)  # Nowy sposób inicjalizacji

# Pobierz słowa/frazy z Gist
def get_random_word():
    response = requests.get(WORDS_GIST_URL)
    words = response.json()
    return random.choice(words)

# Generuj zdanie po polsku (OpenAI)
def generate_polish_sentence(word):
    response = client.chat.completions.create(  # Nowa składnia
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Jesteś pomocnym asystentem do nauki angielskiego."},
            {"role": "user", "content": f"Wygeneruj przykładowe zdanie po polsku zawierające słowo/frazę '{word}', które użytkownik będzie tłumaczył na angielski. Nie podawaj tłumaczenia."}
        ]
    )
    return response.choices[0].message.content  # Nowa ścieżka dostępu

# Wyślij powiadomienie na Telegram
def send_telegram_notification(word, sentence):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    message = f"**Tłumaczenie:**\n\nPL: *{sentence}*\n\nKliknij poniżej, aby zobaczyć odpowiedź 👇\n||EN: {word}||"
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message, parse_mode="MarkdownV2")

async def send_telegram_notification(word, sentence):
    bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
    message = f"**Tłumaczenie:**\n\nPL: *{sentence}*\n\nKliknij poniżej, aby zobaczyć odpowiedź 👇\n||EN: {word}||"
    await bot.send_message(chat_id=os.getenv("TELEGRAM_CHAT_ID"), text=message, parse_mode="MarkdownV2")

if __name__ == "__main__":
    word = get_random_word()
    sentence = generate_polish_sentence(word)
    asyncio(send_telegram_notification(word, sentence))
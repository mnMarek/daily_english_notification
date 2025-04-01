from deepseek_api import Chat  # Wymaga instalacji biblioteki
import random
from telegram import Bot
import os
import json

# Konfiguracja
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")  # Dodaj nowy secret w GitHub!
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def get_random_word():
    with open('words.json', 'r') as f:
        words = json.load(f)
    return random.choice(words)

def generate_polish_sentence(word):
    response = Chat.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "Jesteś pomocnym asystentem do nauki angielskiego."},
            {"role": "user", "content": f"Wygeneruj przykładowe zdanie po polsku zawierające słowo/frazę '{word}'. Nie podawaj tłumaczenia."}
        ]
    )
    return response.choices[0].message.content

def send_telegram_notification(word, sentence):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    message = f"**Tłumaczenie:**\n\nPL: *{sentence}*\n\nKliknij poniżej, aby zobaczyć odpowiedź 👇\n||EN: {word}||"
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message, parse_mode="MarkdownV2")

if __name__ == "__main__":
    word = get_random_word()
    sentence = generate_polish_sentence(word)
    send_telegram_notification(word, sentence)
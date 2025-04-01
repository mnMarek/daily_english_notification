import openai
import pandas as pd
import gspread
from telegram import Bot
import random
import os

# Konfiguracja
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
GOOGLE_SHEETS_URL = os.getenv("GOOGLE_SHEETS_URL")

# Pobierz słowo/frazę z Google Sheets
def get_random_word():
    gc = gspread.service_account(filename="credentials.json")  # Wymaga wcześniejszej autoryzacji
    sheet = gc.open_by_url(GOOGLE_SHEETS_URL).sheet1
    records = sheet.get_all_records()
    return random.choice(records)["Word/Phrase"]

# Wygeneruj przykładowe zdanie po polsku
def generate_polish_sentence(word):
    openai.api_key = OPENAI_API_KEY
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Jesteś pomocnym asystentem do nauki angielskiego."},
            {"role": "user", "content": f"Wygeneruj przykładowe zdanie po polsku zawierające słowo/frazę '{word}', które użytkownik będzie tłumaczył na angielski. Nie podawaj tłumaczenia."}
        ]
    )
    return response.choices[0].message["content"]

# Wyślij powiadomienie przez Telegram
def send_telegram_notification(word, sentence):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    message = f"**Tłumaczenie:**\n\nPL: *{sentence}*\n\nKliknij poniżej, aby zobaczyć odpowiedź 👇\n||EN: {word}||"
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message, parse_mode="MarkdownV2")

if __name__ == "__main__":
    word = get_random_word()
    sentence = generate_polish_sentence(word)
    send_telegram_notification(word, sentence)
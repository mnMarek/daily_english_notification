import openai
import requests
import random
import asyncio
from telegram import Bot
import os
from openai import OpenAI
from telegram.constants import ParseMode
import pandas as pd


# Konfiguracja
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
GITHUB_URL = "https://github.com/mnMarek/daily_english_notification/raw/refs/heads/main/Daily%20English%20Notification.xlsx"
INDEX_FILE = "word_index.txt"


# Inicjalizacja klienta OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)


def escape_markdown(text):
    escape_chars = '_*[]()~`>#+-=|{}.!'
    return ''.join(f'\\{char}' if char in escape_chars else char for char in text)


def load_current_index():
    """Wczytuje aktualny indeks z pliku lub zwraca 0 jeśli plik nie istnieje."""
    if os.path.exists(INDEX_FILE):
        try:
            with open(INDEX_FILE, 'r') as f:
                return int(f.read().strip())
        except (ValueError, FileNotFoundError):
            return 0
    return 0


def save_current_index(index):
    """Zapisuje aktualny indeks do pliku."""
    with open(INDEX_FILE, 'w') as f:
        f.write(str(index))


def get_words_from_github():
    response = requests.get(GITHUB_URL)
    
    # Zapisz plik tymczasowo
    with open("Daily_English_Notification.xlsx", "wb") as f:
        f.write(response.content)
    
    # Odczytaj plik Excel
    df = pd.read_excel("Daily_English_Notification.xlsx", engine="openpyxl")
    words = df["WORDS / PHRASE"].tolist()
    
    return words


async def get_random_word():
    try:
        words = get_words_from_github()
        
        # Wczytaj aktualny indeks
        current_index = load_current_index()
        
        # Pobierz słowo z aktualnego indeksu
        word = words[current_index % len(words)]
        
        # Zapisz następny indeks
        next_index = (current_index + 1) % len(words)
        save_current_index(next_index)
        
        print(f"Pobrano słowo #{current_index + 1}/{len(words)}: {word}")
        
        return word
    except Exception as e:
        print(f"Błąd: {e}. Używam listy zapasowej.")
        
        # Dla listy zapasowej też używamy sekwencyjnego pobierania
        backup_words = ["Error1", "Error2"]
        current_index = load_current_index()
        word = backup_words[current_index % len(backup_words)]
        next_index = (current_index + 1) % len(backup_words)
        save_current_index(next_index)
        
        return word


async def generate_polish_sentence(word):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Jesteś pomocnym asystentem do nauki angielskiego oraz eksperterm językowym, który potrafi tłumaczyć zachowując naturalność, idiomy i styl oryginału. Generuj zdania po polsku, które można przetłumaczyć na angielski używając konkretnych zwrotów."},
            {"role": "user", "content": f"Ułóż proste zdanie w języku polskim ze słowem: '{word}' tak, abym mógł je sobie przetłumaczyć na język angielski na poziomie B1. W zdaniu polskim NIE używaj angielskiego zwrotu."}
        ]
    )
    return response.choices[0].message.content


async def translate_to_english(polish_sentence, word):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"Jesteś ekspertem językowym, który tłumaczy z polskiego na angielski, zachowując naturalność, idiomy i styl oryginału. W tłumaczeniu musisz użyć dokładnie frazy '{word}'."},
            {"role": "user", "content": f"Jesteś ekspertem językowym, który tłumaczy z polskiego na angielski, zachowując naturalność, idiomy i styl oryginału. Przetłumacz na angielski używając dokładnie frazy '{word}': '{polish_sentence}'"}
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

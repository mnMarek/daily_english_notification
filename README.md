# 🧠 Daily English Notification

**daily_english_notification** is an automated English learning assistant that uses Telegram and the OpenAI API to send you translation tasks at random times during the day.

<p align="center">
  <img src="icon.png" alt="Daily English Notification Icon" width="150"/>
</p>

## 🔍 How It Works

1. You maintain a list of English words or phrases you want to learn in an Excel file (`Daily English Notification.xlsx`).
2. The script randomly selects one word or phrase from the list and sends a request to OpenAI to generate an example sentence in Polish and its English translation.
3. The Polish sentence is sent to your Telegram as a message.
4. The English translation is included in the message but temporarily hidden (using spoiler formatting), encouraging you to translate the sentence yourself before checking the answer.
5. Messages are sent every 2 hours between 8:00 AM and 8:00 PM.

## 🛠️ Automation with GitHub Actions

You don't need to run this script manually. The project is fully automated using **GitHub Actions**.  
Once set up with your environment variables and Excel file, the scheduler will trigger automatically on GitHub's servers.

This allows the notification system to function autonomously, without requiring any action from your side.

## 🧰 Requirements

- Python 3.10 or later (for local testing or development)
- OpenAI API Key
- Telegram Bot Token and your Telegram Chat ID

### Dependencies

Install required packages with:

```bash
pip install -r requirements.txt
```
Main libraries used:
- openai
- python-telegram-bot
- pandas
- apscheduler
- requests

## 🚀 How to Run Locally (Optional)
This is only necessary if you want to test or develop the script on your own machine.
1. Clone the repository:
```bash
git clone https://github.com/mnMarek/daily_english_notification.git
cd daily_english_notification
```

3. Create a .env file and fill in your credentials:
```env
OPENAI_API_KEY=your_openai_api_key
TELEGRAM_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
```
3. Prepare a 'Daily English Notification.xlsx' file with one column (with a header) containing the English words/phrases you want to learn.
4. Run the script:
```bash
python main.py
```

## 📊 Project Structure
```bash
daily_english_notification/
│
├── Daily English Notification.xlsx  # Excel file with learning phrases
├── send_notification.py             # Main script
├── .github/workflows/               # GitHub Actions configuration (daily_notification.yml)
└── requirements.txt                 # Python dependencies
```

## 📄 License
This project is licensed under the MIT License.

## 🙋 Author
Created by mnMarek

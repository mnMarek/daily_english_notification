# 🧠 Daily English Notification  

**daily_english_notification** is an automated English learning assistant that uses Telegram and the OpenAI API to send you translation tasks at random times during the day.  

<p align="center">  
  <img src="icon.png" alt="Daily English Notification Icon" width="150"/>  
</p>  

---

## 🔍 How It Works  

1. **You maintain** a list of English words or phrases in an Excel file (`Daily English Notification.xlsx`).  
2. **The script**:  
   - Randomly selects one word/phrase from your list  
   - Uses OpenAI API to generate:  
     - A **Polish example sentence** (sent to your Telegram)  
     - The **English translation** (hidden under spoiler formatting)  
3. **Schedule**: Messages are sent every 2 hours between **8:00 AM and 8:00 PM** (fully automated via GitHub Actions).  

---

## ⚙️ Prerequisites  

### 1. **OpenAI Account & API Key**  
- You need a **paid OpenAI account** ([sign up here](https://platform.openai.com/signup))  
- **Steps**:  
  1. Create API key in [OpenAI Dashboard](https://platform.openai.com/account/api-keys)  
  2. **Enable billing** (typical cost for this project: <$1/month)  

### 2. **Telegram Bot Setup**  
- **Create a Bot**:  
  1. Talk to [@BotFather](https://t.me/BotFather)  
  2. Use `/newbot` command and save the **bot token**  
- **Get Your Chat ID**:  
  1. Send any message to your new bot  
  2. Visit:  
     ```  
     https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates  
     ```  
  3. Find `"chat":{"id":...}` in the JSON response  

---

## 🛠️ Setup  

### 1. **GitHub Secrets Configuration**  
1. Go to your repository → **Settings** → **Secrets and variables** → **Actions**  
2. Add these secrets:  
   - `OPENAI_API_KEY`: Your OpenAI API key  
   - `TELEGRAM_TOKEN`: Your bot token from @BotFather  
   - `TELEGRAM_CHAT_ID`: Your personal chat ID  

### 2. **Excel File Preparation**  
- Create `Daily English Notification.xlsx` with one column (header required)  
- Example format:  
  | Words         |  
  |---------------|  
  | procrastinate |  
  | resilience    |  

---

## 🚀 How to Use  

### **Option 1: Fully Automated (Recommended)**  
1. Fork this repository  
2. Add your Excel file and configure GitHub Secrets  
3. **Done!** The bot will run automatically  

### **Option 2: Local Testing/Development**  
```bash  
git clone https://github.com/mnMarek/daily_english_notification.git  
cd daily_english_notification
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run manually
```bash
python send_notification.py
```

## 📊 Project Structure
```
daily_english_notification/  
├── .github/workflows/               # GitHub Actions config  
│   └── daily_notification.yml       # Automation schedule  
├── Daily English Notification.xlsx  # Your vocabulary  
├── send_notification.py             # Main script  
├── requirements.txt                 # Python dependencies
```

## ❓ FAQ
🔍 Why am I not receiving messages?\
📌 Check:
- GitHub Actions logs for errors
- OpenAI billing is active
- Correct Telegram Chat ID in secrets

🔍 How much does OpenAI API cost?\
📌 Typically <$1/month for this usage scale

🔍 Can I change the notification schedule?\
📌 Yes! Edit the cron job in .github/workflows/daily_notification.yml

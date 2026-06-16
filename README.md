# Minijob Auto-Apply Agent 🤖☕

This is a Python-based automation agent designed to help you find and apply for part-time jobs (minijobs) at cafes and restaurants in Berlin.

## Features

- **Location Discovery**: Uses the Overpass API to find local amenities (cafes, restaurants, bars) in Berlin.
- **Smart Crawling**: Uses Playwright to navigate websites, wait for Javascript to render, and extract text and forms.
- **AI Decision Making**: Sends the website content to a large language model (LLM) via the Groq API (LLaMA3) to decide if it's better to send an email or fill out a web form.
- **Automated Application**: 
  - **Email**: Sends a localized German cover letter and attaches your CV via Gmail SMTP.
  - **Form Fill**: Uses Playwright to automatically fill and submit job application forms.
- **Telegram Notifications**: Sends you a real-time message via Telegram for every attempt, success, and failure.
- **Rate Limiting & Deduplication**: Avoids applying to the same place twice and stops after a configurable quota.

---

## 🚀 Setup & Installation

### 1. Prerequisites
- Python 3.11+
- A [Groq API Key](https://console.groq.com/keys)
- A Telegram Bot Token & Chat ID
- A Gmail account with an [App Password](https://support.google.com/accounts/answer/185833?hl=en)

### 2. Install Dependencies
Clone the repository and install the required packages:

```bash
pip install -r requirements.txt
playwright install chromium
```

### 3. Environment Variables
Create a `.env` file in the root directory (you can copy `.env.example`) and fill it in:

```env
GROQ_API_KEY=your_groq_api_key_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_telegram_chat_id_here
GMAIL_ADDRESS=your_email@gmail.com
GMAIL_APP_PASSWORD=your_gmail_app_password_here
```

### 4. Setup Profile and CV
- Edit `profile.json` to include your actual details (Name, Address, Languages, etc.)
- Place your CV PDF inside the `cv/` directory and ensure the path matches in `profile.json`.

---

## 💻 Usage

Run the agent locally:

```bash
python main.py
```

The script will:
1. Discover places in Berlin.
2. Visit their websites.
3. Apply to up to 10 places (configurable in `config.py`).
4. Log everything to `logs/agent.log`.
5. Send you Telegram updates.

---

## ☁️ Running on GitHub Actions

This project includes a `.github/workflows/daily_apply.yml` file, which runs the agent every day automatically.

To enable this:
1. Push this repository to GitHub.
2. Go to **Settings > Secrets and variables > Actions**.
3. Add the following Repository Secrets:
   - `GROQ_API_KEY`
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
   - `GMAIL_ADDRESS`
   - `GMAIL_APP_PASSWORD`
4. The agent will now run automatically at 09:00 AM UTC every day. You can also trigger it manually from the "Actions" tab.

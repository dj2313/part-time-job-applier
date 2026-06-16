# Minijob Auto-Apply Agent

An autonomous agent that discovers cafes and restaurants in Berlin using OpenStreetMap, crawls their websites to find job/contact pages, uses Groq LLM to decide on the best application method, generates a personalized German cover letter, and automatically submits the application via web forms (Playwright) or email (Gmail SMTP). Sends status notifications via Telegram.

## Setup Instructions

1. **Clone the repository** and navigate to the folder.

2. **Install requirements:**
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

3. **Configure Environment Variables:**
   Copy `.env.example` to `.env` and fill in the values:
   ```bash
   cp .env.example .env
   ```
   - `GROQ_API_KEY`: Get from [Groq Console](https://console.groq.com/).
   - `TELEGRAM_BOT_TOKEN` & `TELEGRAM_CHAT_ID`: Create a bot via BotFather on Telegram and get your chat ID.
   - `GMAIL_ADDRESS` & `GMAIL_APP_PASSWORD`: Use a Google App Password, not your main account password.

4. **Update Profile & CV:**
   - Edit `profile.json` with your real details, skills, and availability.
   - Place your CV PDF file at `cv/CV.pdf` (or update the path in `profile.json`).

5. **Run the script locally:**
   ```bash
   python main.py
   ```

## Automated Daily Run (GitHub Actions)
The project includes a `.github/workflows/run.yml` file to run daily.
If you host this on GitHub, make sure to add the following to your **Repository Secrets** (Settings > Secrets and variables > Actions):
- `GROQ_API_KEY`
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`
- `GMAIL_ADDRESS`
- `GMAIL_APP_PASSWORD`

## Limitations & Warnings
- **OSM Coverage:** Not all cafes/restaurants have a `website` tag on OpenStreetMap. The agent only processes those that do.
- **Form Filling:** The AI does a "best-effort" to map form fields, but web forms are highly diverse. Some submissions might fail.
- **Spam Prevention:** The script includes a 2-second delay between sites and skips already-processed sites to avoid spamming the same business.

*Disclaimer: Use this tool responsibly. Unsolicited automated messages can sometimes be marked as spam.*

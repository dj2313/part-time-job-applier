import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
load_dotenv()

# Base directories
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
CV_DIR = BASE_DIR / "cv"
LOG_DIR = BASE_DIR / "logs"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
CV_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

# Application Quotas
MAX_APPLICATIONS_PER_RUN = 10

# Overpass API Configuration
# Berlin Bounding Box
BBOX = "52.34,13.09,52.68,13.76"
AMENITIES = ["cafe", "restaurant", "fast_food", "bar", "ice_cream"]
OVERPASS_URL = "http://overpass-api.de/api/interpreter"

# File Paths
PROFILE_PATH = BASE_DIR / "profile.json"
PLACES_PATH = DATA_DIR / "places.json"
APPLIED_PATH = DATA_DIR / "applied.json"
CV_PATH = CV_DIR / "CV.pdf"

# API Keys and Credentials
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

# Scraping / Crawling
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
DELAY_BETWEEN_SITES = 2  # seconds

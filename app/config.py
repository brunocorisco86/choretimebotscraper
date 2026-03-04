import os
from dotenv import load_dotenv

load_dotenv()

CHORE_USER = os.getenv("CHORE_USER", "Junior")
CHORE_PASS = os.getenv("CHORE_PASS", "Junior1281")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
DB_PATH = os.getenv("DB_PATH", "data/chore_data.db")
PG_URI = os.getenv("PG_URI")

from dotenv import load_dotenv
import os

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not TELEGRAM_CHAT_ID:
    raise ValueError("TELEGRAM_CHAT_ID не задан")                                                                

KEYWORDS = [
    "python",
    "backend",
    "fastapi"
]

LOCATIONS = [
    "remote",
    "удаленно"
]
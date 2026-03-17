from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")


KEYWORDS = [
    "python",
    "backend",
    "fastapi"
]

LOCATIONS = [
    "remote",
    "удаленно"
]
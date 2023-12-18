import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ["BOT_TOKEN"]
ADMIN_ID = os.environ["ADMIN_ID"]

API_HASH = os.environ["API_HASH"]
API_ID = int(os.environ["API_ID"])


POSTGRES_USER = os.environ["POSTGRES_USER"]
POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
POSTGRES_DB_NAME = os.environ["POSTGRES_DB"]
POSTGRES_DB_HOST = os.environ["POSTGRES_HOST"]

DB_URI = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_DB_HOST}/{POSTGRES_DB_NAME}"

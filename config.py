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

# DATABASE_URI = os.environ["DATABASE_URL"].split("/")
# POSTGRES_DB_NAME = DATABASE_URI[-1]
# POSTGRES_DB_HOST = DATABASE_URI[-2].split("@")[-1]
# POSTGRES_PASSWORD = DATABASE_URI[-2].split("@")[-2].split(":")[-1]
# POSTGRES_USER = DATABASE_URI[-2].split("@")[-2].split(":")[-2]

DB_URI: str = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_DB_HOST}/{POSTGRES_DB_NAME}"

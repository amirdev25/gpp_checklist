import os
from dotenv import load_dotenv
from sqlalchemy.engine.url import URL
import psycopg2

load_dotenv()

# Telegram
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
ADMIN_GROUP_ID = int(os.getenv("ADMIN_GROUP_ID"))
PDF_FILE_PATH = "checklist.pdf"

# Database connection params
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# SQLAlchemy URL (for SQLAlchemy engine)
SUPABASE_DB_URL = URL.create(
    drivername="postgresql+psycopg2",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME
)

# Test connection via psycopg2
try:
    conn = psycopg2.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME
    )
    print("✅ Ulandi")
    conn.close()
except Exception as e:
    print("❌ Ulanmadi:", e)

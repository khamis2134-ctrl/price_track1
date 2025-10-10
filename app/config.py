# app/config.py
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = Path(os.getenv("DATA_DIR", str(ROOT / "data")))
RAW_DIR = DATA_DIR / "raw"
CLEAN_DIR = DATA_DIR / "clean"
DB_PATH = Path(os.getenv("DB_PATH", str(CLEAN_DIR / "prices.db")))
LOG_PATH = Path(os.getenv("LOG_PATH", str(ROOT / "logs" / "app.log")))

# If OFFLINE_MODE is "1" or "true", the project will load sample CSV instead of attempting HTTP scraping.
OFFLINE_MODE = os.getenv("OFFLINE_MODE", "true").lower() in ("1", "true", "yes")

# Default local sample file (initial ingestion)
SAMPLE_CSV = RAW_DIR / "sample_prices.csv"

# Default user agent, headers, and retry settings for live scraping
DEFAULT_HEADERS = {
    "User-Agent": "price_track1-bot/1.0 (+https://github.com/yourname/price_track1)"
}
REQUEST_TIMEOUT = float(os.getenv("REQUEST_TIMEOUT", "10"))
REQUEST_RETRIES = int(os.getenv("REQUEST_RETRIES", "2"))

# Placeholders for configured sources (can be extended or loaded from a JSON/YAML)
DEFAULT_SOURCES = [
    # Example: {"name": "example", "url": "https://example.com/products", "type": "html", "enabled": False}
]

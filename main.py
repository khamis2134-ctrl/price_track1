# main.py
import argparse
from app.config import DEFAULT_SOURCES, OFFLINE_MODE
from app.db import init_db
from app.scrapers import run_sources, load_offline_sample
from app.utils import log_event

def main(args):
    log_event("Starting price_track1...")
    init_db()

    if args.offline or OFFLINE_MODE:
        # initial offline ingestion
        count = load_offline_sample()
        log_event(f"Loaded {count} offline records.")
    if args.url:
        # run targeted scrape
        log_event(f"Scraping URL: {args.url}")
        run_sources([{"url": args.url, "name": args.name or args.url, "selectors": None, "enabled": True}])
    else:
        # run configured sources
        log_event("Running configured sources...")
        run_sources(DEFAULT_SOURCES)

    log_event("All done ✅")

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="price_track1 runner")
    p.add_argument("--offline", action="store_true", help="Force offline sample ingestion")
    p.add_argument("--url", help="Scrape this single URL")
    p.add_argument("--name", help="Optional label for the URL source")
    args = p.parse_args()
    main(args)

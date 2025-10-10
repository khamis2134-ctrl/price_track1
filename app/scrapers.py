# app/scrapers.py
import csv
import time
import requests
from bs4 import BeautifulSoup
from app.config import OFFLINE_MODE, SAMPLE_CSV, DEFAULT_HEADERS, REQUEST_TIMEOUT, REQUEST_RETRIES
from app.db import insert_price, bulk_insert
from pathlib import Path
from app.utils import log_event

def load_offline_sample():
    """Load initial data from sample CSV and insert to DB (idempotent for first run)."""
    path = Path(SAMPLE_CSV)
    if not path.exists():
        log_event(f"[scrapers] No sample CSV at {path}. Nothing loaded.")
        return 0
    rows = []
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            source = r.get("source") or "sample"
            item = r.get("item")
            price = try_float(r.get("price"))
            currency = r.get("currency") or "USD"
            extra = {k: v for k, v in r.items() if k not in ("item", "price", "currency", "source")}
            rows.append((source, item, price, currency, extra))
    if rows:
        bulk_insert(rows)
    log_event(f"[scrapers] Loaded {len(rows)} records from sample CSV.")
    return len(rows)

def try_float(x):
    try:
        return float(x)
    except Exception:
        return None

def scrape_from_url(url, source_name=None, selectors=None):
    """
    Basic HTML scraper template.
    - url: page to fetch
    - source_name: label inserted in DB
    - selectors: dict mapping { 'product': 'css selector', 'price': '...', 'title': '...' }
    This function is deliberately generic: when you provide site-specific selectors, it will try to extract.
    """
    headers = DEFAULT_HEADERS
    attempts = 0
    while attempts <= REQUEST_RETRIES:
        try:
            r = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
            r.raise_for_status()
            html = r.text
            break
        except Exception as e:
            attempts += 1
            log_event(f"[scrapers] Request error for {url}: {e} (attempt {attempts})")
            time.sleep(1)
            if attempts > REQUEST_RETRIES:
                raise
    soup = BeautifulSoup(html, "html.parser")

    # Minimal generic extraction: if selectors are provided, use them; otherwise try simple heuristics
    rows = []
    if selectors and "product" in selectors:
        product_nodes = soup.select(selectors["product"])
        for node in product_nodes:
            title = node.select_one(selectors.get("title")) if selectors.get("title") else node.get_text(strip=True)
            price_node = node.select_one(selectors.get("price")) if selectors.get("price") else None
            price = None
            if price_node:
                price_text = price_node.get_text()
                price = extract_price(price_text)
            title_text = title.get_text(strip=True) if hasattr(title, "get_text") else str(title)
            rows.append((source_name or url, title_text, price, "USD", None))
    else:
        # Fallback simplistic: find elements with price-like patterns
        possible = soup.find_all(text=lambda t: t and ("$" in t or "USD" in t))
        for t in possible[:50]:
            text = t.strip()
            price = extract_price(text)
            parent = t.parent
            title = parent.find_previous(string=True) or parent.get_text(separator=" ", strip=True)
            rows.append((source_name or url, title[:200], price, "USD", None))

    # Insert only non-empty items
    good_rows = [(s, i, p, c, e) for s, i, p, c, e in rows if i and p is not None]
    if good_rows:
        bulk_insert(good_rows)
        log_event(f"[scrapers] Inserted {len(good_rows)} items from {url}")
    else:
        log_event(f"[scrapers] No valid items found for {url}")
    return len(good_rows)

def extract_price(text):
    import re
    # simple regex to get a number like 1,234.56 or 1234 or $1234.56
    if not text:
        return None
    m = re.search(r"([0-9]{1,3}(?:[,\s][0-9]{3})*(?:\.[0-9]+)?|[0-9]+(?:\.[0-9]+)?)", text.replace(",", ""))
    if m:
        try:
            return float(m.group(1))
        except:
            return None
    return None

def run_sources(sources):
    total = 0
    for s in sources:
        if s.get("enabled", True) is False:
            continue
        url = s.get("url")
        selectors = s.get("selectors")
        source_name = s.get("name", url)
        try:
            if OFFLINE_MODE:
                log_event("[scrapers] OFFLINE_MODE enabled. Use sample CSV instead of live scraping.")
                # offline sample load only once outside loop, but keep it safe here
                total += load_offline_sample()
            else:
                total += scrape_from_url(url, source_name=source_name, selectors=selectors)
        except Exception as exc:
            log_event(f"[scrapers] Error scraping {url}: {exc}")
    return total

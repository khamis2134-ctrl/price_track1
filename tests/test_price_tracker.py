import json
import pytest
from app.price_tracker import scrape_example, scrape_site

def test_scrape_site(monkeypatch):
    with open("data/selectors.json") as f:
        site = json.load(f)["sites"][0]

    def fake_get(url, timeout):
        class Response:
            text = """
            <html>
                <div class='thumbnail'>
                    <a class='title'>Test Product</a>
                    <span class='price'>19.99</span>
                </div>
                <div class='thumbnail'>
                    <a class='title'>Another Product</a>
                    <span class='price'>29.99</span>
                </div>
            </html>
            """
            def raise_for_status(self):
                pass
        return Response()

    import requests
    monkeypatch.setattr(requests, "get", fake_get)

    # Run scrape_site with patched requests.get
    scrape_site(site)

    # Run scrape_example as fallback or additional test
    scrape_example()


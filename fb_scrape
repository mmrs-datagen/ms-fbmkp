from playwright.sync_api import sync_playwright
import time
import csv

def scrape_marketplace():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Go to Facebook Marketplace Seattle
        page.goto("https://www.facebook.com/marketplace/seattle")
        input("Log in manually, then press Enter...")

        # Scroll to load more listings
        for _ in range(30):
            page.mouse.wheel(0, 1500)
            time.sleep(3)

        listings = page.query_selector_all('a[href*="/marketplace/item/"]')
        results = []

        for item in listings:
            # Try getting all <span dir="auto">, pick the one with longest text
            spans = item.query_selector_all('span[dir="auto"]')
            title = None
            if spans:
                texts = [s.inner_text().strip() for s in spans if s.inner_text().strip()]
                if texts:
                    title = max(texts, key=len)

            img_el = item.query_selector("img")
            img_url = img_el.get_attribute("src") if img_el else None

            if title and img_url:
                results.append({
                    "title": title,
                    "image_url": img_url
                })

        # Write to CSV
        with open("marketplace_seattle.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["title", "image_url"])
            writer.writeheader()
            writer.writerows(results)

        print(f"✅ {len(results)} items saved to 'marketplace_seattle.csv'")
        browser.close()

if __name__ == "__main__":
    scrape_marketplace()

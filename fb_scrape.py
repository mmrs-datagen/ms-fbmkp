from playwright.sync_api import sync_playwright
import time
import csv

def scrape_marketplace(city, category):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Go to Facebook Marketplace Seattle
        page.goto(f"https://www.facebook.com/marketplace/{city}/{category}")
        input("Log in manually, then press Enter...")

        # Scroll to load more listings
        listings = set()
        for _ in range(50):
            page.mouse.wheel(0, 1000)
            time.sleep(3)
            listings_tmp = page.query_selector_all('a[href*="/marketplace/item/"]')
            for l in listings_tmp:
                listings.add(l)

        results = []

        setImg = set()
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

            if title and img_url and (img_url not in setImg):
                results.append({
                    "title": title.replace('\n', '').replace('\r', ''),
                    "image_url": img_url
                })
                setImg.add(img_url)

        # results.sort(key= lambda r: r[1])

        # Write to CSV
        with open(f"marketplace_{city}_{category}.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["title", "image_url"])
            writer.writeheader()
            writer.writerows(results)

        print(f"✅ {len(results)} items saved to 'marketplace_{city}_{category}.csv'")
        browser.close()

if __name__ == "__main__":
    city = "seattle"
    category = "electronics"
    scrape_marketplace(city, category)

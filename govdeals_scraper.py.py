import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

# ========== CONFIGURATION ==========
BASE_URL = "https://www.govdeals.com/index.cfm?fa=Main.AdvSearchResultsNew"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"
}
PARAMS = {
    "kWord": "",  # Keyword search if needed
    "whichForm": "item",  # Default form for items
    "searchPg": "Main",   # Default search page
    "sortOption": "a",    # Sort by auction ending soonest
}
OUTPUT_FILE = "govdeals_listings.csv"
# ===================================

def scrape_govdeals():
    print(f"[{datetime.now()}] Scraping: {BASE_URL}")
    try:
        response = requests.get(BASE_URL, headers=HEADERS, params=PARAMS, timeout=15)
        response.raise_for_status()
    except Exception as e:
        print(f"[ERROR] Failed to fetch URL: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    listings = soup.select(".searchResultsTbl tr")

    scraped_data = []

    for row in listings:
        title_tag = row.select_one(".listingTitle a")
        price_tag = row.select_one(".price")

        if title_tag and price_tag:
            title = title_tag.text.strip()
            link = "https://www.govdeals.com" + title_tag["href"]
            price = price_tag.text.strip()

            scraped_data.append({
                "Title": title,
                "Price": price,
                "Link": link
            })

    return scraped_data

def save_to_csv(data, filename):
    if not data:
        print("[INFO] No data to save.")
        return

    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"[SUCCESS] Saved {len(df)} items to {filename}")

def main():
    data = scrape_govdeals()
    save_to_csv(data, OUTPUT_FILE)

if __name__ == "__

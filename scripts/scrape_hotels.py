from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import os

# Setup Chrome options
options = Options()
options.add_argument("--headless")  # Run headless for speed (optional)
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Path to ChromeDriver (adjust if necessary)
driver = webdriver.Chrome(options=options)

# URL to scrape (Swiss hotels)
BASE_URL = "https://www.tripadvisor.com/Hotels-g188045-Switzerland-Hotels.html"

def scrape_hotels(page_url):
    print(f"Scraping: {page_url}")
    driver.get(page_url)
    time.sleep(5)  # Wait for JavaScript to load

    hotels = []

    # Find hotel cards
    cards = driver.find_elements(By.CSS_SELECTOR, "div[data-automation='hotel-card-title']")
    print(f"Found {len(cards)} hotels on page.")

    for card in cards:
        try:
            name = card.text
            link = card.find_element(By.TAG_NAME, "a").get_attribute("href")
            hotels.append({"name": name, "link": link})
        except Exception as e:
            print(f"Error parsing card: {e}")
            continue

    return hotels

# Scrape multiple pages
all_hotels = []
pages_to_scrape = 3
for page in range(pages_to_scrape):
    offset = page * 30
    page_url = BASE_URL if page == 0 else BASE_URL.replace("Hotels.html", f"oa{offset}-Hotels.html")
    all_hotels.extend(scrape_hotels(page_url))
    time.sleep(2)

driver.quit()

# Save to CSV
os.makedirs("../data", exist_ok=True)
df = pd.DataFrame(all_hotels)
df.to_csv("../data/hotels_selenium.csv", index=False)
print(f"Scraped {len(df)} hotels and saved to ../data/hotels_selenium.csv")
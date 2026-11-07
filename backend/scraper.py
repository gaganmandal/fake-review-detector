# scrapper.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time


def get_flipkart_reviews(url):
    options = webdriver.ChromeOptions()

    # Performance options
    options.add_argument("--headless=new")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    print("🌐 Opening Flipkart page...")
    driver.get(url)
    time.sleep(3)

    # Scroll to load reviews
    print("📜 Scrolling page...")
    for _ in range(8):
        driver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(1)

    reviews = []

    # ==============================
    # PRIMARY SELECTOR
    # ==============================
    print("🔍 Trying primary selector...")
    elements = driver.find_elements(By.XPATH, "//div[contains(@class,'ZmyHeo')]")

    for e in elements:
        try:
            text = e.text.strip()
            if text and len(text) > 5:
                reviews.append(text)
        except:
            continue

    print("Primary reviews:", len(reviews))

    # ==============================
    # FALLBACK SELECTOR
    # ==============================
    if len(reviews) == 0:
        print("⚠️ Using fallback selector...")
        elements = driver.find_elements(By.XPATH, "//div[@dir='auto']")

        for e in elements:
            try:
                text = e.text.strip()
                if text and len(text) > 5:
                    reviews.append(text)
            except:
                continue

    driver.quit()

    # Remove duplicates
    reviews = list(set(reviews))

    print("✅ Unique reviews:", len(reviews))

    if len(reviews) == 0:
        print("❌ No reviews found!")
        return []

    # Sample output (for demo)
    print("\n📌 Sample Reviews:")
    for r in reviews[:3]:
        print("-", r)

    return reviews[:30]


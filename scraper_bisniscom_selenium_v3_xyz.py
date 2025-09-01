
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)
driver.set_window_size(1920, 1080)

articles = []
max_pages = 100

def parse_date(text):
    try:
        return pd.to_datetime(text.strip(), dayfirst=True).strftime("%Y-%m-%d")
    except:
        return None

for page in range(1, max_pages + 1):
    print(f"🔄 Halaman {page}")
    url = f"https://bisnis.tempo.co/tag/ihsg?page={page}"
    driver.get(url)

    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.media-body"))
        )
    except:
        print("⛔ Timeout tunggu konten, lanjut halaman berikutnya.")
        with open(f"debug_page_{page}.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        driver.save_screenshot(f"debug_page_{page}.png")
        continue

    items = driver.find_elements(By.CSS_SELECTOR, "div.media-body")
    if not items:
        print("⛔ Tidak ada artikel ditemukan, berhenti.")
        break

    for item in items:
        try:
            title = item.find_element(By.TAG_NAME, "h3").text.strip()
            date = item.find_element(By.CLASS_NAME, "date").text.strip()
            articles.append({
                "Date": parse_date(date),
                "Title": title,
                "Source": "Bisnis"
            })
        except:
            continue

    time.sleep(2)

driver.quit()

df = pd.DataFrame(articles)
if not df.empty:
    df.to_csv("bisnis_news_2020_2025.csv", index=False)
    print(f"✅ Tersimpan {len(df)} artikel dari Bisnis.com")
else:
    print("❌ Tidak ada data yang cocok.")

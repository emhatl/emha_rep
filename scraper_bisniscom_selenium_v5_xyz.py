import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
import time

# Setup browser
options = uc.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--headless")  # opsional, bisa dicopot agar terlihat
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36")

driver = uc.Chrome(options=options)

# Inisialisasi
articles = []
max_pages = 50  # bisa diubah
base_url = "https://www.bisnis.com/tag/ihsg?page="

def parse_date(text):
    try:
        return pd.to_datetime(text.strip(), dayfirst=True).strftime("%Y-%m-%d")
    except:
        return None

# Loop scraping
for page in range(1, max_pages + 1):
    print(f"🔄 Halaman {page}")
    url = base_url + str(page)
    try:
        driver.get(url)
        time.sleep(3)  # jeda awal

        # Scroll down untuk trigger lazy load
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.media-body"))
        )

        items = driver.find_elements(By.CSS_SELECTOR, "div.media-body")

        if not items:
            print("⛔ Tidak ada artikel ditemukan.")
            continue

        for item in items:
            try:
                title = item.find_element(By.TAG_NAME, "h4").text.strip()
                date = item.find_element(By.CLASS_NAME, "media-date").text.strip()
                articles.append({
                    "Date": parse_date(date),
                    "Title": title,
                    "Source": "Bisnis"
                })
            except Exception as e:
                continue

    except TimeoutException:
        print("⛔ Timeout halaman, lanjut berikutnya.")
        continue

    time.sleep(2)

driver.quit()

# Simpan hasil
df = pd.DataFrame(articles)
if not df.empty:
    df.to_csv("bisnis_news_2020_2025.csv", index=False)
    print(f"✅ Selesai! Disimpan {len(df)} artikel dari Bisnis.com")
else:
    print("❌ Tidak ada data yang disimpan.")

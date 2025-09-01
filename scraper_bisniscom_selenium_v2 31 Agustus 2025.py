from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import time

def parse_date(text):
    text = text.strip().lower()
    today = datetime.date.today()
    if "jam" in text:
        return today.strftime("%Y-%m-%d")
    elif "hari" in text:
        num = int(text.split()[0])
        return (today - datetime.timedelta(days=num)).strftime("%Y-%m-%d")
    elif "minggu" in text:
        num = int(text.split()[0])
        return (today - datetime.timedelta(weeks=num)).strftime("%Y-%m-%d")
    elif "bulan" in text:
        num = int(text.split()[0])
        return (today - datetime.timedelta(days=30*num)).strftime("%Y-%m-%d")
    elif "tahun" in text:
        num = int(text.split()[0])
        return (today - datetime.timedelta(days=365*num)).strftime("%Y-%m-%d")
    else:
        return None

# Setup Chrome headless
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=options)

articles = []
max_pages = 100
min_year = 2020

for page in range(1, max_pages + 1):
    print(f"🔄 Halaman {page}")
    url = f"https://www.bisnis.com/search/ihsg?page={page}"
    driver.get(url)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.media-body"))
        )
    except:
        print("⛔ Timeout tunggu konten, lanjut halaman berikutnya.")
        continue

    soup = BeautifulSoup(driver.page_source, "html.parser")
    items = soup.select("div.media-body")
    if not items:
        print("⛔ Tidak ada artikel ditemukan, berhenti.")
        break

    for item in items:
        title_tag = item.select_one("h2.media-heading a")
        date_tag = item.select_one("span.date")
        if not title_tag or not date_tag:
            continue
        title = title_tag.get_text(strip=True)
        raw_date = date_tag.get_text(strip=True)
        parsed_date = parse_date(raw_date)
        if not parsed_date or int(parsed_date[:4]) < min_year or parsed_date > "2025-07-24":
            continue
        articles.append({
            "Date": parsed_date,
            "Title": title,
            "Summary": "",
            "Source": "Bisnis"
        })
    time.sleep(1)

driver.quit()

df = pd.DataFrame(articles)
if not df.empty:
    df.to_csv("bisnis_news_2020_2025.csv", index=False)
    print(f"✅ Tersimpan {len(df)} artikel dari Bisnis.com.")
else:
    print("❌ Tidak ada data yang cocok.")

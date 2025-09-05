import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

base_url = "https://www.kontan.co.id/search/?search=ihsg&per_page="
step = 20
max_offset = 500  # Ubah sesuai kebutuhan, 500 artinya 25 halaman (20 berita per halaman)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
}

def parse_date(text):
    text = text.strip().replace("|", "").replace("WIB", "").strip()
    try:
        return pd.to_datetime(text, dayfirst=True).strftime("%Y-%m-%d")
    except:
        return None

all_articles = []

for offset in range(0, max_offset + 1, step):
    print(f"🔄 Mengambil halaman offset: {offset}")
    url = f"{base_url}{offset}"
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        print("⛔ Gagal akses, berhenti.")
        break

    soup = BeautifulSoup(resp.text, "html.parser")
    items = soup.select("li.search--list")

    if not items:
        print("❌ Tidak ada data ditemukan, berhenti.")
        break

    for item in items:
        try:
            title_tag = item.find("h2") or item.find("h1")
            date_tag = item.find("span", class_="font-gray")
            title = title_tag.get_text(strip=True)
            date = parse_date(date_tag.get_text(strip=True)) if date_tag else None
            link = title_tag.find("a")["href"]

            all_articles.append({
                "Date": date,
                "Title": title,
                "URL": link,
                "Source": "Kontan"
            })
        except Exception as e:
            continue

    time.sleep(1)

# Simpan ke CSV
df = pd.DataFrame(all_articles)
df.to_csv("kontan_news_scraped.csv", index=False)
print(f"✅ Selesai! Disimpan {len(df)} berita.")

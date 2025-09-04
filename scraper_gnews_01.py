import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime

def get_google_news(keyword, start_year=2020, end_year=2025):
    results = []
    for year in range(start_year, end_year + 1):
        print(f"🔄 Tahun: {year}")
        for month in range(1, 13):
            time.sleep(2)
            q = f"{keyword} after:{year}-{month:02d}-01 before:{year}-{month+1:02d}-01"
            url = f"https://www.google.com/search?q={q}&tbm=nws&hl=id"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
            }

            r = requests.get(url, headers=headers)
            soup = BeautifulSoup(r.text, "html.parser")
            articles = soup.select("div.dbsr")

            for article in articles:
                try:
                    title = article.find("div", class_="JheGif nDgy9d").text
                    source = article.find("div", class_="XTjFC WF4CUc").text
                    date = article.find("span", class_="WG9SHc").text.strip()
                    link = article.a["href"]
                    snippet = article.find("div", class_="Y3v8qd").text.strip()

                    results.append({
                        "Date": date,
                        "Title": title,
                        "Source": source,
                        "Link": link,
                        "Snippet": snippet
                    })
                except:
                    continue
    return pd.DataFrame(results)

df_news = get_google_news("IHSG")
df_news.to_csv("google_news_ihsg_2020_2025.csv", index=False)
print(f"✅ Selesai! Disimpan {len(df_news)} artikel.")

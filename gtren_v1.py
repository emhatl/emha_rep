from pytrends.request import TrendReq
import pandas as pd

# Inisialisasi koneksi
pytrends = TrendReq(hl='id-ID', tz=420)

# Payload
pytrends.build_payload(kw_list=["IHSG"], timeframe="2020-07-24 2025-07-23", geo="ID")

# Ambil data interest over time
data = pytrends.interest_over_time()

# Simpan ke CSV
if 'isPartial' in data.columns:
    data = data.drop(columns=['isPartial'])

data.to_csv("google_trends_ihsg_2020_2025.csv")
print("✅ Data Google Trends IHSG berhasil disimpan.")

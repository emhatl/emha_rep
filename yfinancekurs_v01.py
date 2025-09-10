import yfinance as yf

kurs = yf.download("USDIDR=X", start="2020-07-24", end="2025-07-24")
kurs[["Close"]].rename(columns={"Close": "USDIDR"}).to_csv("usd_idr_2020_2025.csv")

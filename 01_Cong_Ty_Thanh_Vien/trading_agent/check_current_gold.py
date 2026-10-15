import json
import yfinance as yf

ticker = "GC=F"
tk = yf.Ticker(ticker)

# 1. Info / Current Quote
info = tk.info
current_price = info.get("regularMarketPrice") or info.get("currentPrice") or info.get("open")
day_high = info.get("dayHigh") or info.get("regularMarketDayHigh")
day_low = info.get("dayLow") or info.get("regularMarketDayLow")
prev_close = info.get("previousClose") or info.get("regularMarketPreviousClose")

print(f"=== CURRENT LIVE QUOTE FOR {ticker} ===")
print(f"Current Price: {current_price}")
print(f"Day High: {day_high}")
print(f"Day Low: {day_low}")
print(f"Previous Close: {prev_close}")

# 2. Intraday History (1d with 1h / 15m intervals or 5d)
hist_1d = tk.history(period="2d", interval="1h")
print("\n=== RECENT 1-HOUR INTRADAY CANDLES ===")
print(hist_1d.tail(8)[["Open", "High", "Low", "Close", "Volume"]])

# 3. SPDR Gold Shares (GLD) Check
gld = yf.Ticker("GLD")
info_gld = gld.info
print("\n=== GLD ETF CURRENT STATUS ===")
print(f"GLD Price: {info_gld.get('regularMarketPrice') or info_gld.get('currentPrice')}")
print(f"GLD Day High: {info_gld.get('dayHigh')}, Day Low: {info_gld.get('dayLow')}")

# 4. Check Dollar Index (DX-Y.NYB) and US 10Y Yield (^TNX)
dxy = yf.Ticker("DX-Y.NYB")
tnx = yf.Ticker("^TNX")
dxy_price = dxy.info.get("regularMarketPrice") or (dxy.history(period="1d")["Close"].iloc[-1] if not dxy.history(period="1d").empty else None)
tnx_yield = tnx.info.get("regularMarketPrice") or (tnx.history(period="1d")["Close"].iloc[-1] if not tnx.history(period="1d").empty else None)
print(f"\n=== MACD / BOND / CURRENCY INTRA-DAY ===")
print(f"DXY (USD Index): {dxy_price}")
print(f"US 10Y Yield (^TNX): {tnx_yield}")

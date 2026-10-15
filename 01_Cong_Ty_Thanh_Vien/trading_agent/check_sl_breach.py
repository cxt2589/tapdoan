import yfinance as yf
import pandas as pd

tk = yf.Ticker('GC=F')
# Fetch full daily history covering Oct 04 to Oct 12
hist = tk.history(start='2026-10-04', end='2026-10-13')

print("=== DAILY SESSIONS FROM 2026-10-04 TO 2026-10-12 ===")
for idx, row in hist.iterrows():
    date_str = idx.strftime('%Y-%m-%d (%A)')
    print(f"{date_str} | Open: {row['Open']:8.2f} | High: {row['High']:8.2f} | Low: {row['Low']:8.2f} | Close: {row['Close']:8.2f}")

min_low = hist['Low'].min()
min_date = hist['Low'].idxmin().strftime('%Y-%m-%d (%A)')
print(f"\n---> Lowest point of the entire period: {min_low:.2f} on {min_date}")

# Check with SL 4,135 and SL 4,145
print("\n=== SL BREACH VERIFICATION ===")
for sl in [4145.0, 4135.0]:
    breached = hist[hist['Low'] < sl]
    if not breached.empty:
        print(f"SL ${sl:.2f}: BREACHED (Thủng) on the following days:")
        for idx, row in breached.iterrows():
            print(f"  - {idx.strftime('%Y-%m-%d (%A)')}: Low was {row['Low']:.2f} (cách SL {row['Low'] - sl:+.2f}$)")
    else:
        print(f"SL ${sl:.2f}: SAFE (KHÔNG THỦNG). Điểm thấp nhất tuần qua là {min_low:.2f} (vẫn cao hơn SL {min_low - sl:+.2f}$)")

# Now let's also fetch 1-hour intraday candles if available
try:
    hist_1h = tk.history(start='2026-10-05', end='2026-10-12', interval='1h')
    if not hist_1h.empty:
        print(f"\n=== 1-HOUR INTRADAY VERIFICATION ({len(hist_1h)} candles) ===")
        min_1h = hist_1h['Low'].min()
        min_1h_time = hist_1h['Low'].idxmin()
        print(f"Lowest 1H candle low: {min_1h:.2f} at {min_1h_time}")
except Exception as e:
    print(f"1h check notice: {e}")

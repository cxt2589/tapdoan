import yfinance as yf
import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

tk = yf.Ticker('GC=F')
hist = tk.history(start='2026-10-05', end='2026-10-12')

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

print("=== BANG GIA NEN CHI TIET TU 05/10 DEN 11/10/2026 ===")
print(hist[['Open', 'High', 'Low', 'Close', 'Volume']])

print("\n=== DOI CHIEU VOI MUC STOP LOSS ===")
sl_35 = 4135.0
sl_45 = 4145.0

for idx, row in hist.iterrows():
    d_str = idx.strftime('%d/%m/%Y (%A)')
    low_val = row['Low']
    hit_35 = "CO (Dinh SL)" if low_val <= sl_35 else "Khong"
    hit_45 = "CO (Dinh SL)" if low_val <= sl_45 else "Khong"
    print(f"- {d_str}: Low = ${low_val:.2f} | So voi SL $4,145: {hit_45} | So voi SL $4,135: {hit_35}")

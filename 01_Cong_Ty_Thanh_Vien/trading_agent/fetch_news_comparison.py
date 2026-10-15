import json
import yfinance as yf
from tradingagents.agents.utils.news_data_tools import get_news, get_global_news

print("=== 1. TICKER SPECIFIC NEWS FOR GOLD (GLD / GC=F) ===")
try:
    gld_news = get_news.invoke({"ticker": "GLD", "start_date": "2026-09-18", "end_date": "2026-09-29"})
    print(gld_news[:1500])
except Exception as e:
    print(f"Error fetching get_news: {e}")

print("\n=== 2. GLOBAL MACRO NEWS HEADLINES ===")
try:
    global_news = get_global_news.invoke({"curr_date": "2026-09-29", "look_back_days": 10, "limit": 8})
    print(global_news[:1500])
except Exception as e:
    print(f"Error fetching get_global_news: {e}")

print("\n=== 3. MACRO ASSETS COMPARISON (DX-Y.NYB / TNX / CL=F) ===")
for sym in ["DX-Y.NYB", "^TNX", "CL=F"]: # USD Index, 10-Yr Yield, Crude Oil
    try:
        t = yf.Ticker(sym)
        hist = t.history(period="10d")
        if not hist.empty:
            p_prev = hist["Close"].iloc[-5] if len(hist) >= 5 else hist["Close"].iloc[0]
            p_latest = hist["Close"].iloc[-1]
            chg = ((p_latest - p_prev) / p_prev) * 100
            print(f"- {sym}: Previous={p_prev:.2f} -> Latest={p_latest:.2f} (Change: {chg:+.2f}%)")
    except Exception as e:
        print(f"Error fetching {sym}: {e}")

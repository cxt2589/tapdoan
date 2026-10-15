import json
import yfinance as yf
from tradingagents.agents.utils.agent_utils import get_verified_market_snapshot

ticker = "GC=F"
tk = yf.Ticker(ticker)

# 1. Historical data for the past 10 sessions
hist = tk.history(period="1mo")
print("=== SESSIONS OHLCV FROM LATE SEPTEMBER TO OCTOBER 2026 ===")
print(hist.tail(8)[["Open", "High", "Low", "Close", "Volume"]])

latest_date = hist.index[-1].strftime("%Y-%m-%d")
print(f"\nLatest session date in history: {latest_date}")

# 2. Latest Verified Snapshot
snapshot = get_verified_market_snapshot.invoke({"symbol": ticker, "curr_date": latest_date})
print("\n=== LATEST VERIFIED SNAPSHOT ===")
print(snapshot)

# 3. Current Live Info
info = tk.info
print("\n=== CURRENT LIVE STATS ===")
print(f"Price: {info.get('regularMarketPrice') or info.get('currentPrice')}")
print(f"Day High: {info.get('dayHigh') or info.get('regularMarketDayHigh')}")
print(f"Day Low: {info.get('dayLow') or info.get('regularMarketDayLow')}")
print(f"Previous Close: {info.get('previousClose') or info.get('regularMarketPreviousClose')}")

# 4. News
tk_gld = yf.Ticker("GLD")
news = tk.news[:5] if tk.news else tk_gld.news[:5]
print("\n=== LATEST NEWS (OCTOBER 2026) ===")
for n in news:
    title = n.get("content", {}).get("title") or n.get("title")
    pub = n.get("content", {}).get("pubDate") or n.get("providerPublishTime")
    print(f"- {title} [{pub}]")

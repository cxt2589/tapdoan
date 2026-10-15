import json
import yfinance as yf
from tradingagents.agents.utils.agent_utils import get_verified_market_snapshot

ticker = "GC=F"
tk = yf.Ticker(ticker)
hist = tk.history(period="5d")
print("=== RECENT 5 SESSIONS OHLCV FOR GOLD (GC=F) ===")
print(hist[["Open", "High", "Low", "Close", "Volume"]])

latest_date = hist.index[-1].strftime("%Y-%m-%d")
print(f"\nLatest session date: {latest_date}")

# Snapshot
snapshot = get_verified_market_snapshot.invoke({"symbol": ticker, "curr_date": latest_date})
print("\n=== LATEST VERIFIED SNAPSHOT ===")
print(snapshot)

# News
print("\n=== LATEST NEWS (TODAY / YESTERDAY) ===")
tk_gld = yf.Ticker("GLD")
news = tk.news[:7] if tk.news else tk_gld.news[:7]
for n in news:
    title = n.get("content", {}).get("title") or n.get("title")
    pub = n.get("content", {}).get("pubDate") or n.get("providerPublishTime")
    print(f"- {title} [{pub}]")

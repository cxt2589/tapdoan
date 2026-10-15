import json
import yfinance as yf
from tradingagents.agents.utils.agent_utils import (
    get_verified_market_snapshot,
    get_indicators,
)

ticker = "GC=F"
tk = yf.Ticker(ticker)
hist = tk.history(period="1mo")
latest_date = hist.index[-1].strftime("%Y-%m-%d")
print(f"Latest trading date available for {ticker}: {latest_date}")

# Snapshot
snapshot = get_verified_market_snapshot.invoke({"symbol": ticker, "curr_date": latest_date})
print("\n=== VERIFIED MARKET SNAPSHOT (GOLD - GC=F) ===")
print(snapshot)

# News
print("\n=== RECENT GOLD NEWS ===")
tk_gld = yf.Ticker("GLD")
news = tk.news[:5] if tk.news else tk_gld.news[:5]
for n in news:
    title = n.get("content", {}).get("title") or n.get("title")
    pub = n.get("content", {}).get("pubDate") or n.get("providerPublishTime")
    print(f"- {title} ({pub})")

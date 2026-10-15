import json
import yfinance as yf
from tradingagents.agents.utils.agent_utils import (
    get_verified_market_snapshot,
    get_indicators,
)

ticker = "GC=F" # Gold Futures
tk = yf.Ticker(ticker)
hist = tk.history(period="1mo")
latest_date = hist.index[-1].strftime("%Y-%m-%d")
print(f"Latest trading date available for {ticker}: {latest_date}")

# 1. Snapshot
snapshot = get_verified_market_snapshot.invoke({"symbol": ticker, "curr_date": latest_date})
print("\n=== VERIFIED MARKET SNAPSHOT (GOLD FUTURES - GC=F) ===")
print(snapshot)

# Also check GLD for ETF context
tk_gld = yf.Ticker("GLD")
info_gld = tk_gld.info
gld_summary = {
    "symbol": "GLD",
    "regularMarketPrice": info_gld.get("regularMarketPrice") or info_gld.get("navPrice"),
    "fiftyTwoWeekHigh": info_gld.get("fiftyTwoWeekHigh"),
    "fiftyTwoWeekLow": info_gld.get("fiftyTwoWeekLow"),
    "totalAssets": info_gld.get("totalAssets"),
}
print("\n=== GLD ETF SUMMARY ===")
print(json.dumps(gld_summary, indent=2))

# 2. News on Gold
print("\n=== RECENT GOLD NEWS ===")
news = tk.news[:5] if tk.news else tk_gld.news[:5]
for n in news:
    title = n.get("content", {}).get("title") or n.get("title")
    pub = n.get("content", {}).get("pubDate") or n.get("providerPublishTime")
    print(f"- {title} ({pub})")

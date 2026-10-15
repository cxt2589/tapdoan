import json
import yfinance as yf
from tradingagents.agents.utils.agent_utils import (
    get_verified_market_snapshot,
    get_indicators,
)

ticker = "NVDA"
# Fetch latest data from yfinance
tk = yf.Ticker(ticker)
hist = tk.history(period="1mo")
latest_date = hist.index[-1].strftime("%Y-%m-%d")
print(f"Latest trading date available: {latest_date}")

# 1. Snapshot
snapshot = get_verified_market_snapshot.invoke({"symbol": ticker, "curr_date": latest_date})
print("\n=== VERIFIED MARKET SNAPSHOT ===")
print(snapshot)

# 2. Key stats
info = tk.info
fundamentals_summary = {
    "symbol": ticker,
    "shortName": info.get("shortName"),
    "currentPrice": info.get("currentPrice") or info.get("regularMarketPrice"),
    "marketCap": info.get("marketCap"),
    "trailingPE": info.get("trailingPE"),
    "forwardPE": info.get("forwardPE"),
    "pegRatio": info.get("pegRatio"),
    "profitMargins": info.get("profitMargins"),
    "revenueGrowth": info.get("revenueGrowth"),
    "operatingMargins": info.get("operatingMargins"),
    "totalDebt": info.get("totalDebt"),
    "freeCashflow": info.get("freeCashflow"),
    "targetMeanPrice": info.get("targetMeanPrice"),
    "recommendationKey": info.get("recommendationKey"),
}
print("\n=== FUNDAMENTALS SUMMARY ===")
print(json.dumps(fundamentals_summary, indent=2))

# 3. News
print("\n=== RECENT NEWS ===")
news = tk.news[:5]
for n in news:
    title = n.get("content", {}).get("title") or n.get("title")
    pub = n.get("content", {}).get("pubDate") or n.get("providerPublishTime")
    print(f"- {title} ({pub})")

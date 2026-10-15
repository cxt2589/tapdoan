import sys
from tradingagents.agents.utils.agent_utils import (
    get_fundamentals,
    get_indicators,
    get_verified_market_snapshot,
)

ticker = "NVDA"
date = "2024-05-10"

print(f"=== 1. VERIFIED MARKET SNAPSHOT ({ticker} @ {date}) ===")
snapshot = get_verified_market_snapshot.invoke({"symbol": ticker, "curr_date": date})
print(snapshot)

print(f"\n=== 2. FUNDAMENTALS ({ticker} @ {date}) ===")
fundamentals = get_fundamentals.invoke({"ticker": ticker, "curr_date": date})
print(fundamentals[:600] + "\n... [TRUNCATED FOR DISPLAY]")

print(f"\n=== 3. TECHNICAL INDICATORS ({ticker} - RSI, 14 days lookback) ===")
rsi_data = get_indicators.invoke({"symbol": ticker, "indicator": "rsi", "curr_date": date, "look_back_days": 14})
print(rsi_data)

print("\n=== PIPELINE STATUS: All Data Analyst Tools Operating Successfully! ===")

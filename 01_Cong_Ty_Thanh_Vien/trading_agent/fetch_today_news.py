import yfinance as yf

# Check news on gold and commodities
for ticker in ["GC=F", "GLD", "DX-Y.NYB", "CL=F"]:
    t = yf.Ticker(ticker)
    print(f"=== NEWS FOR {ticker} ===")
    try:
        news = t.news
        for n in news[:3]:
            title = n.get("title") or n.get("content", {}).get("title")
            pub = n.get("providerPublishTime") or n.get("content", {}).get("pubDate")
            print(f"- {title} [{pub}]")
    except Exception as e:
        print(f"Err: {e}")

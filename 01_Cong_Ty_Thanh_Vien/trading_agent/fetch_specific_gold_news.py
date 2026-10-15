import yfinance as yf

# Search news specifically for Gold
gld = yf.Ticker("GLD")
gc = yf.Ticker("GC=F")
print("=== GC=F NEWS ===")
for item in gc.news[:10]:
    title = item.get("title") or item.get("content", {}).get("title")
    pub = item.get("providerPublishTime") or item.get("content", {}).get("pubDate")
    print(f"- {title} [{pub}]")

print("\n=== GLD NEWS ===")
for item in gld.news[:10]:
    title = item.get("title") or item.get("content", {}).get("title")
    pub = item.get("providerPublishTime") or item.get("content", {}).get("pubDate")
    print(f"- {title} [{pub}]")

import yfinance as yf

meta = yf.Ticker("META")
tesla = yf.Ticker("TESLA")

meta_price = meta.info['regularMarketPrice']
tesla_price = tesla.info['regularMarketPrice']

print("META current price:", meta_price)
print("TESLA current price:", tesla_price)
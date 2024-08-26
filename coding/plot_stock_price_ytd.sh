# filename: plot_stock_price_ytd.sh
#!/bin/bash
# Plot a chart of the stock price change YTD for META and TESLA
# Use Yahoo Finance API to get the stock data
# Save the data to stock_price_ytd.csv
# Save the plot to stock_price_ytd.png

# Get the current date
current_date=$(date +%Y-%m-%d)

# Get the stock data for META and TESLA
meta_data=$(curl -s "https://query1.finance.yahoo.com/v7/finance/quote?symbols=META" | jq -r '.quoteResponse.result[0]')
tesla_data=$(curl -s "https://query1.finance.yahoo.com/v7/finance/quote?symbols=TSLA" | jq -r '.quoteResponse.result[0]')

# Get the stock price change YTD for each stock
meta_ytd_change=$(echo $meta_data | jq -r '.regularMarketChangePercentYTD')
tesla_ytd_change=$(echo $tesla_data | jq -r '.regularMarketChangePercentYTD')

# Save the data to stock_price_ytd.csv
echo "Date,META,TESLA" > stock_price_ytd.csv
echo "$current_date,$meta_ytd_change,$tesla_ytd_change" >> stock_price_ytd.csv

# Plot the chart
python3 -m matplotlib.pyplot as plt
plt.plot([current_date], [meta_ytd_change], label="META")
plt.plot([current_date], [tesla_ytd_change], label="TESLA")
plt.xlabel("Date")
plt.ylabel("Stock Price Change YTD (%)")
plt.title("Stock Price Change YTD for META and TESLA")
plt.legend()
plt.savefig("stock_price_ytd.png")
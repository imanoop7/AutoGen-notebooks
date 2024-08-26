# filename: get_stock_data.sh
#!/bin/bash
# Get the year-to-date gain for META and TESLA
# Use Yahoo Finance API to get the stock data
# Print the year-to-date gain for each stock

# Get the current date
current_date=$(date +%Y-%m-%d)

# Get the stock data for META and TESLA
meta_data=$(curl -s "https://query1.finance.yahoo.com/v7/finance/quote?symbols=META" | jq -r '.quoteResponse.result[0]')
tesla_data=$(curl -s "https://query1.finance.yahoo.com/v7/finance/quote?symbols=TSLA" | jq -r '.quoteResponse.result[0]')

# Get the year-to-date gain for each stock
meta_ytd_gain=$(echo $meta_data | jq -r '.regularMarketChangePercent')
tesla_ytd_gain=$(echo $tesla_data | jq -r '.regularMarketChangePercent')

# Print the year-to-date gain for each stock
echo "META year-to-date gain: $meta_ytd_gain%"
echo "TESLA year-to-date gain: $tesla_ytd_gain%"
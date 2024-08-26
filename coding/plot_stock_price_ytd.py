# filename: plot_stock_price_ytd.py
import matplotlib.pyplot as plt
import pandas as pd

# Get the stock data for META and TESLA
try:
    meta_data = pd.read_csv('stock_data/META.csv')
    tesla_data = pd.read_csv('stock_data/TSLA.csv')
except FileNotFoundError:
    print("The stock data files do not exist. Please make sure that the files exist and are in the correct location.")
    exit()

# Calculate the year-to-date gain for each stock
meta_ytd_gain = (meta_data['Close'][-1] - meta_data['Close'][0]) / meta_data['Close'][0] * 100
tesla_ytd_gain = (tesla_data['Close'][-1] - tesla_data['Close'][0]) / tesla_data['Close'][0] * 100

# Create a dataframe with the year-to-date gain for each stock
ytd_gain = pd.DataFrame({
    'Stock': ['META', 'TESLA'],
    'Year-to-Date Gain': [meta_ytd_gain, tesla_ytd_gain]
})

# Plot the year-to-date gain for each stock
plt.bar(ytd_gain['Stock'], ytd_gain['Year-to-Date Gain'])
plt.xlabel('Stock')
plt.ylabel('Year-to-Date Gain (%)')
plt.title('Year-to-Date Stock Price Change')
plt.savefig('stock_price_ytd.png')

# Save the data to a CSV file
ytd_gain.to_csv('stock_price_ytd.csv', index=False)
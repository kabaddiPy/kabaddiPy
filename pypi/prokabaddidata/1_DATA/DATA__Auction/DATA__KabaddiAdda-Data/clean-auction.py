import pandas as pd

df = pd.read_csv('kabaddiadda_auctiondata_FINAL_Capital.csv')

df = df.dropna(subset=['Price'])

df.to_csv('cleaned_kabaddi_auction_data.csv', index=False)

print("Data processing complete. New file 'cleaned_kabaddi_data.csv' has been created.")
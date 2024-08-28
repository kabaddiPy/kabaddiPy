import os
import pandas as pd

# Define the directory containing the CSV files
directory = './s9_csv_allskilldone/csvs'

# Loop through each file in the directory
for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        file_path = os.path.join(directory, filename)
        print(file_path)
        
        # Read the CSV file
        df = pd.read_csv(file_path, header=None)
        
        # Delete the first row
        df = df.drop(index=0)
        
        # Set the new header to be the second row (now the first row after drop)
        df.columns = df.iloc[0]
        
        # Drop the new header row from the DataFrame
        df = df[1:]
        
        # Reset index after the operations
        df.reset_index(drop=True, inplace=True)
        
        # Save the modified DataFrame back to the CSV file
        df.to_csv(file_path, index=False)

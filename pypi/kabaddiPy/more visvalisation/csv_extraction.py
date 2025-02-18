import pandas as pd
import os

root = 'pypi/kabaddiPy'
output_file_path = 'output_csv/combined_data.csv'  # Specify the output file for combined data
os.makedirs(os.path.dirname(output_file_path), exist_ok=True)  # Create the output directory if it doesn't exist

combined_df = pd.DataFrame()  # Initialize an empty DataFrame to hold all data

for dirpath, dirnames, filenames in os.walk(root):
    for file in filenames:
        if file.endswith('.csv'):
            csv_file_path = os.path.join(dirpath, file)  # Get the full path of the CSV file
            print(f"Found CSV: {csv_file_path}")
            df = pd.read_csv(csv_file_path)  # Read the CSV file into a DataFrame
            combined_df = pd.concat([combined_df, df], ignore_index=True)  # Concatenate the DataFrames

# Save the combined DataFrame to a single CSV file
combined_df.to_csv(output_file_path, index=False)  
print(f"All data saved to: {output_file_path}")  # Confirm saving the combined file

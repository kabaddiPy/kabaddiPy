import pandas as pd
import os

# Define the base directory where all season folders are located
base_dir = "./players/"

# List to store all dataframes
all_dfs = []

# Iterate through all directories in the base directory
for season_dir in os.listdir(base_dir):
    
    if season_dir.startswith("season"):
        season_path = os.path.join(base_dir, season_dir)
        
        if os.path.isdir(season_path):
            csv_path = os.path.join(season_path, "merged_player_stats_all.csv")
            
            if os.path.exists(csv_path):
                
                # Read the CSV file
                df = pd.read_csv(csv_path)

                # Add a 'season' column
                season_number = season_dir.replace("season", "")
                df["season"] = season_number

                # Append to the list of dataframes
                all_dfs.append(df)

# Concatenate all dataframes
merged_df = pd.concat(all_dfs, ignore_index=True)

# Save the merged dataframe to a new CSV file
merged_df.to_csv("all_seasons_player_stats.csv", index=False)

print("Merged CSV file created: all_seasons_player_stats.csv")

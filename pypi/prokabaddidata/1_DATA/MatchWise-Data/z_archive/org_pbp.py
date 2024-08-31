import os
import json
import shutil
import re

# Define the parent directory containing JSON files
json_parent_dir = './eight_nine_ten'

# Create a new directory for organized files
organized_dir = 'Organized_Matches_eight_nine_ten'
os.makedirs(organized_dir, exist_ok=True)


# Function to sanitize filename
def sanitize_filename(filename):
    return re.sub(r'[^\w\-_\. ]', '_', filename)


# Function to extract season from series name
def extract_season(series_name):
    if 'Season' in series_name:
        return series_name.split('Season')[1].split(',')[0].strip()
    elif 'PKL' in series_name:
        return series_name.split('PKL')[1].split(',')[0].strip()
    else:
        return 'Unknown'

# Iterate through all subdirectories and JSON files
for root, dirs, files in os.walk(json_parent_dir):
    for file in files:
        if file.endswith('.json'):
            file_path = os.path.join(root, file)
            
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            print(file)

            if data.get("err"):
                continue
            
            
            # print(data["title"])

            data = data.get('gameData')

            # Extract season and match number
            season = data.get('match_detail').get('series').get('name')
            season.replace(",", "")
            season.replace(" ", "_")
            season.replace("-", "_")

            match_id = data['match_detail']['match_id']
            match_number = sanitize_filename(data['match_detail']['match_number'].replace(' ', '_'))
            
            # Create season directory if it doesn't exist
            season_dir = os.path.join(organized_dir, f'Season_{season}')
            os.makedirs(season_dir, exist_ok=True)
            
            # Create new filename
            new_filename = f'{match_number}_ID_{match_id}.json'
            new_file_path = os.path.join(season_dir, new_filename)
            
            # Copy the file to the new location
            shutil.copy2(file_path, new_file_path)

print("Files have been organized successfully.")

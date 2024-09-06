import os
import json

# Set the paths for the two folders
folder1 = r"C:\Users\KIIT\Documents\ProKabaddi_API\pypi\prokabaddidata\MatchData_pbp\Season_PKL_Season_7_2019"
folder2 = r"C:\Users\KIIT\Documents\ProKabaddi_API\pypi\prokabaddidata\MatchData_pbp\other-data\old_data\Season_PKL_Season_7_2019"

# Iterate through the files in Folder 1
for filename in os.listdir(folder1):
    if filename.endswith('.json'):
        # Extract the match number from the filename
        match_no = filename

        # Load the JSON file from Folder 1
        with open(os.path.join(folder1, filename), 'r') as f:
            data1 = json.load(f)

        # Load the corresponding JSON file from Folder 2
        match_file = None
        for f2_filename in os.listdir(folder2):
            if f2_filename.endswith(f'{match_no}.json'):
                match_file = os.path.join(folder2, f2_filename)
        with open(match_file, 'r') as f:
            data2 = json.load(f)
        # Replace the 4 elements under "gameData" in data1 with the corresponding elements from data2
        data1['gameData'] = data2

        # Write the updated data back to the file in Folder 1
        with open(os.path.join(folder1, filename), 'w') as f:
            json.dump(data1, f, indent=4)
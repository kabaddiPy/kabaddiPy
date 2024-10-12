import os
import json
import csv

def extract_player_data(pypi_folder):
    player_data = []

    def process_file(file_path):
        try:
            if file_path.endswith('.json'):
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    if isinstance(data, list):
                        return [extract_player_info(item) for item in data]
                    else:
                        return [extract_player_info(data)]
            elif file_path.endswith('.csv'):
                with open(file_path, 'r') as file:
                    reader = csv.DictReader(file)
                    return [extract_player_info(row) for row in reader]
        except Exception as e:
            print(f"Error processing file {file_path}: {str(e)}")
        return []

    def extract_player_info(data):
        if not isinstance(data, dict):
            print(f"Warning: Unexpected data format: {data}")
            return None
        
        # Look for various possible keys for the player name
        name_keys = ['name', 'player_name', 'player', 'Name', 'PlayerName']
        name = next((str(data.get(key, '')) for key in name_keys if key in data), '')
        
        return {
            'name': name,
            'total_raid_points': float(data.get('total_raid_points', 0)),
            'total_tackle_points': float(data.get('total_tackle_points', 0)),
            'team': str(data.get('team', '')),
            'successful_raid_points': float(data.get('successful_raid_points', 0)),
            'successful_tackle_points': float(data.get('successful_tackle_points', 0)),
            'season': str(data.get('season', ''))
        }

    for root, dirs, files in os.walk(pypi_folder):
        for file in files:
            if file.endswith(('.json', '.csv')):
                file_path = os.path.join(root, file)
                player_data.extend(process_file(file_path))

    return [p for p in player_data if p is not None]

# Usage
pypi_folder = "pypi"
extracted_data = extract_player_data(pypi_folder)

# Save the extracted data to a CSV file
output_file = "player_data.csv"
fieldnames = ['name', 'total_raid_points', 'total_tackle_points', 'team', 
              'successful_raid_points', 'successful_tackle_points', 'season']

with open(output_file, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for player in extracted_data:
        writer.writerow(player)

print(f"Data has been saved to {output_file}")

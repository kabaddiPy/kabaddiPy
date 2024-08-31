import os
import json
import pandas as pd


# Function to load JSON files from a directory
def load_json_files(folder_path):
    json_files = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.json'):
            with open(os.path.join(folder_path, file_name)) as f:
                json_files.append(json.load(f))
    return json_files


# Function to query match overview
def get_match_overview(folder_path, match_id, season):
    json_files = load_json_files(folder_path)

    # Filtering based on season and match_id
    match_details = None
    for data in json_files:
        if data['matches'][0]['tour_name'] == season:
            for match in data['matches']:
                if match['game_id'] == match_id:
                    match_details = match
                    break

    if match_details:
        # General Details DataFrame
        general_details = {
            'tour_name': match_details['tour_name'],
            'series_id': match_details['series_id'],
            'start_date': match_details['start_date'],
            'end_date': match_details['end_date'],
            'venue_name': match_details['venue_name'],
            'event_status': match_details['event_status'],
            'winning_margin': match_details['winning_margin']
        }
        general_df = pd.DataFrame([general_details])

        # Participants DataFrame
        participants_data = []
        for participant in match_details['participants']:
            team_name = participant['name']
            team_id = participant['id']
            for player in participant['players_involved']:
                player_data = {
                    'team_name': team_name,
                    'team_id': team_id,
                    'player_name': player['name'],
                    'player_id': player['id'],
                    'player_value': player['value'],
                    'player_type': player['type']
                }
                participants_data.append(player_data)

        participants_df = pd.DataFrame(participants_data)

        return general_df, participants_df
    else:
        print(f"No match found for match_id {match_id} in season {season}")
        return None, None


# Example Usage
# folder_path = r"C:\Users\KIIT\Documents\ProKabaddi_API\pypi\prokabaddidata\1_DATA\MatchWise-Data\Matches-Overview"

folder_path = "../1_DATA/MatchWise-Data/Matches-Overview"

match_id = "60"
season = "Pro Kabaddi League Season 1, 2014"

general_df, participants_df = get_match_overview(folder_path, match_id, season)

print("General Details:")
print(general_df)

print("\nParticipants:")
print(participants_df)

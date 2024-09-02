import os
import json
import pandas as pd

def build_team_roster(team_id, season_number):
    roster = []  # Initialize the roster list
    
    for i in os.listdir("./MatchData_pbp"):
        if f"Season_{season_number}" in i:
            break

    directory_path = os.path.join("./MatchData_pbp", i)
    
    print(f"Starting to build the roster for Team ID: {team_id}, Season: {season_number}...\n")
    
    # Iterate over all files in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith(".json"):  # Process only JSON files
            file_path = os.path.join(directory_path, filename)
            print(f"Loading file: {filename}")
            
            with open(file_path, 'r') as f:
                match_data = json.load(f)
                
                # Check if the match belongs to the specified season
                if match_data['match_detail']['series']['id'] == season_number:
                    
                    print(f"Processing match ID: {match_data['match_detail']['match_id']}")
                    
                    teams = match_data['teams']['team']
                    for team in teams:
                        if team['id'] == team_id:
                            print(f"Found team {team['name']} (ID: {team_id}) in the match.")
                            squad = team['squad']
                            for player in squad:
                                player_id = player['id']
                                player_name = player['name']

                                # Check if player is already in the roster
                                if player_id not in [p['Player ID'] for p in roster]:
                                    player_details = {
                                        'Player ID': player_id,
                                        'Name': player_name,
                                        'Jersey Number': player.get('jersey', None),
                                        'Captain': player.get('captain', False),
                                        'Played': player.get('played', False),
                                        'Starter': player.get('starter', False),
                                        'Top Raider': player.get('top_raider', False),
                                        'Top Defender': player.get('top_defender', False)
                                    }

                                    roster.append(player_details)
                                    print(f"Added player: {player_name} (ID: {player_id}) to the roster.")
                                else:
                                    print(f"Player: {player_name} (ID: {player_id}) is already in the roster.")
    
    # Convert the roster list into a DataFrame
    roster_df = pd.DataFrame(roster)
    print("\nRoster building complete.\n")
    return roster_df

# Example usage:
team_id = '6'
season_number = 4

# Build the roster and get it as a DataFrame
roster_df = build_team_roster(team_id, season_number)

# Display the resulting DataFrame
print(roster_df)

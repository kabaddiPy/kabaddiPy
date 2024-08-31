import json
import pandas as pd
from pathlib import Path


def get_pkl_standings(season=None, team_id=None, matches=True):
    if season is None:
        season=10
    team_info_list = []
    matches_list = []
    file_path = Path(f"../1_DATA/Team-Wise-Data/standings_json/json_s{season}.json")

    with open(file_path, 'r') as f:
        data = json.load(f)

    standings = data['standings']
    print("hello")
    for group in standings['groups']:
        for team in group['teams']['team']:
            if team_id is None or int(team['team_id']) == team_id:
                team_info = {
                    'Season': season,
                    'Team_Name': team['team_name'],
                    'Team_Id': team['team_id'],
                    'team_short_name': team['team_short_name'],
                    'League_position': team['position'],
                    'Matches_played': team['played'],
                    'Wins': team['wins'],
                    'Lost': team['lost'],
                    'Tied': team['tied'],
                    'Draws': team['draws'],
                    'No Result': team['noresult'],
                    'League_points': team['points'],
                    'Score_diff': team['score_diff'],
                    'Qualified': team['is_qualified'],
                }
                team_info_list.append(team_info)

                if matches:
                    # Extract match results
                    for match in team['match_result']['match']:
                        match_info = {
                            'Team_Id': team['team_id'],
                            'match_id': match['id'],
                            'date': match['date'],
                            'result': match['result'],
                            'opponent': match['teama_short_name'] if int(match['teamb_id']) == int(team['team_id']) else
                            match['teamb_short_name'],
                            'team_score': match['teamb_score'] if int(match['teamb_id']) == int(team['team_id']) else
                            match['teama_score'],
                            'opponent_score': match['teama_score'] if int(match['teamb_id']) == int(
                                team['team_id']) else match['teamb_score'],
                            'match_result': match['match_result']
                        }
                        matches_list.append(match_info)

    # Create dataframes
    team_info_df = pd.DataFrame(team_info_list)
    if matches_list:
        matches_df = pd.DataFrame(matches_list)
        return team_info_df, matches_df
    else:
        return team_info_df


def get_team_info(team_id, season='overall'):
    file_path_5_plus = "../1_DATA/Team-Wise-Data/seasons_5_plus_and_all_rounded.csv"
    file_path_1_to_4 = "../1_DATA/Team-Wise-Data/seasons_1_to_4_final.csv"

    if season != 'overall':
        season = int(season)

    if season == 'overall' or 5 <= season <= 10:
        df = pd.read_csv(file_path_5_plus)
    elif 1 <= season <= 4:
        df = pd.read_csv(file_path_1_to_4)
    else:
        print(f"Invalid season: {season}")
        return None, None, None

    df['team_id'] = pd.to_numeric(df['team_id'], errors='coerce')

    team_id = int(team_id)

    if season == 'overall':
        all_row = df[(df['team_id'] == team_id) & (df['season'] == 'all')]
        other_rows = df[(df['team_id'] == team_id) & (df['season'] != 'all')]
        filtered_df = pd.concat([all_row, other_rows]).reset_index(drop=True)
    else:
        filtered_df = df[(df['team_id'] == team_id) & (df['season'] == season)]

    if filtered_df.empty:
        print(f"No data found in CSV for team_id {team_id} in season {season}")
        return None, None, None

    try:
        if season == 'overall':
            latest_season = df[df['season'] != 'all']['season'].max()
            pkl_standings, pkl_matches = get_pkl_standings(latest_season, team_id)
        else:
            pkl_standings, pkl_matches = get_pkl_standings(season, team_id)
    except Exception as e:
        print(f"Error occurred while calling get_pkl_standings: {e}")
        pkl_standings, pkl_matches = None, None

    return filtered_df, pkl_standings, pkl_matches


if __name__ == '__main__':

    # team_info, _, matches = get_team_info(4, 5, simple=False)  # For Bengal Warriors (team_id: 4) in season 5
    # print(matches)
    #print(matches)
    # team = get_pkl_standings(matches=False)
    # print(team)
    #print(matches)

    # team_info, standings, matches = get_team_info(team_id=1,season=9)
    # print(matches)
    test_team_id = 1  # Replace with a valid team_id

    # Test for a specific season (1-4)
    csv_data, standings_data, matches_data = get_team_info(test_team_id)
    print(csv_data)
    #print("Season 3 data:", csv_data.shape if csv_data is not None else "No data")
    #greetings = analyze_team(4, 5, simple=False)
    #print(greetings)

'''if not simple:
        csv_file_path = Path(f"../1_DATA/DATA__ProKabaddi-Data/Team-Wise-Data/teams/seasons_5_plus_and_all_rounded.csv")
        df = pd.read_csv(csv_file_path)

        # Filter the dataframe for the s
        team_info = df[(df['team_id'] == team_id) & (df['season'] == season)]

        if team_info.empty:
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()  # Return empty dataframes if team not found

        # Separate rank headers
        rank_columns = [col for col in team_info.columns if col.endswith('_rank')]
        rank_df = team_info[rank_columns]

        # Remove rank columns from team_info
        team_info = team_info.drop(columns=rank_columns)

        return team_info, pd.DataFrame,rank_df'''
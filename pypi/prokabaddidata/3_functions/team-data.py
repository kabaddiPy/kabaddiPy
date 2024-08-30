import json
import pandas as pd
from pathlib import Path


def get_team_info(team_id, season, simple=False):
    if simple:
        team_info_list = []
        matches_list = []
        file_path = Path(f"../1_DATA/DATA__ProKabaddi-Data/Team-Wise-Data/improved_standings/standings_json/json_s{season}.json")

        with open(file_path, 'r') as f:
            data = json.load(f)

        standings = data['standings']

        for group in standings['groups']:
            for team in group['teams']['team']:
                if int(team['team_id']) == team_id:
                    # Extract team info
                    team_info = {
                        'Season': season,
                        'Team_Name': team['team_name'],
                        'Team_Id': team['team_id'],
                        'League_position': team['position'],
                        'Matches_played': team['played'],
                        'Wins': team['wins'],
                        'Lost': team['lost'],
                        'Tied': team['tied'],
                        'League_points': team['points'],
                        'Score_diff': team['score_diff'],
                        'Qualified': team['is_qualified'],
                    }
                    team_info_list.append(team_info)

                    # Extract match results
                    for match in team['match_result']['match']:
                        match_info = {
                            'match_id': match['id'],
                            'date': match['date'],
                            'result': match['result'],
                            'opponent': match['teama_short_name'] if int(match['teamb_id']) == team_id else match[
                                'teamb_short_name'],
                            'team_score': match['teamb_score'] if int(match['teamb_id']) == team_id else match[
                                'teama_score'],
                            'opponent_score': match['teama_score'] if int(match['teamb_id']) == team_id else match[
                                'teamb_score'],
                            'match_result': match['match_result']
                        }
                        matches_list.append(match_info)

        # Create dataframes
        team_info_df = pd.DataFrame(team_info_list)
        matches_df = pd.DataFrame(matches_list)

        return team_info_df, matches_df
    if not simple:
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

        return team_info, pd.DataFrame,rank_df

if __name__ == '__main__':

    team_info, _, matches = get_team_info(4, 5, simple=False)  # For Bengal Warriors (team_id: 4) in season 5
    print(matches)
    #print(matches)
    #df = pd.read_csv(r"C:\Users\KIIT\Documents\ProKabaddi_API\pypi\prokabaddidata\1_DATA\DATA__ProKabaddi-Data\Team-Wise-Data\teams\seasons_5_plus_and_all_rounded.csv")
    #print(df.columns)

    #greetings = analyze_team(4, 5, simple=False)
    #print(greetings)
import json
from pathlib import Path
import pandas as pd



def create_team_info(team, season, group_name):
    return {
        'Group': group_name,
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

def create_matches_list(team, group_name):
    matches = []
    for match in team['match_result']['match']:
        match_info = {
            'Group': group_name,
            'match_id': match['id'],
            'date': match['date'],
            'teama_id': match['teama_id'],
            'result': match['result'],
            'teama_short_name': match['teama_short_name'],
            'teama_score': match['teama_score'],
            'teamb_id': match['teamb_id'],
            'teamb_short_name': match['teamb_short_name'],
            'teamb_score': match['teamb_score'],
            'match_result': match['match_result']
        }
        matches.append(match_info)
    return matches

def process_matches(matches_list):
    matches_df = pd.DataFrame(matches_list)
    matches_df = matches_df[(matches_df['result'].isin(['W', 'T'])) | (matches_df['result'].isnull())]
    matches_df = matches_df.sort_values(by='date', ascending=True)
    matches_df = matches_df.set_index('match_id').rename_axis('match id')
    return matches_df


def get_pkl_standings(season=None, team_id=None, matches=False):
    if season is None:
        season = 10
    

    #TODO: have to fix this...
    file_path = Path(f"/Users/annimukh/Documents/acode/_CMUAPI/ProKabaddi_API/pypi/prokabaddidata/PKL_Standings/json_s{season}.json")

    with open(file_path, 'r') as f:
        data = json.load(f)

    standings = data['standings']

    team_info_list = []
    matches_list = []

    for group in standings['groups']:
        group_name = group['name'] if 'name' in group else 'Main'
        for team in group['teams']['team']:
            if team_id is None or int(team['team_id']) == team_id:
                team_info = create_team_info(team, season, group_name)
                team_info_list.append(team_info)

                if matches:
                    matches_list.extend(create_matches_list(team, group_name))

    team_info_df = pd.DataFrame(team_info_list)

    if matches:
        matches_df = process_matches(matches_list)
        return team_info_df, matches_df
    else:
        return team_info_df


if __name__ == "__main__":



    t,m = get_pkl_standings("8", matches=True)
    
    
    print(t)
    print(m)
    print(len(m))
import json
from pathlib import Path
import pandas as pd
import json
import pandas as pd

import json
import pandas as pd
import glob


class KabaddiDataAPI:
    
    # for a season - display the standings


    def create_team_info(self, team, season, group_name):
        """Create a dictionary with team information for a given season and group."""
        
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

    def create_matches_list(self, team, group_name):
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

    def process_matches(self, matches_list):
        matches_df = pd.DataFrame(matches_list)
        matches_df = matches_df[(matches_df['result'].isin(['W', 'T'])) | (matches_df['result'].isnull())]
        matches_df = matches_df.sort_values(by='date', ascending=True)
        matches_df = matches_df.set_index('match_id').rename_axis('match id')
        return matches_df


    def get_pkl_standings(self, season=None, team_id=None, matches=False):
        
        if season is None:
            season = 10
        

        #TODO: have to fix this...
        file_path = Path(f"./PKL_Standings/pkl_standings_s{season}.json")

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



    def match_data(self, season="all"):
        matches_list = []
        
        # Determine the file(s) to load based on the season input
        if season == "all":
            files = glob.glob('./Matches-Overview/S*_PKL_MatchData.json')
        else:
            files = [f'./Matches-Overview/S{season}_PKL_MatchData.json']
        
        for file in files:
            with open(file) as f:
                data = json.load(f)

            # Loop over each match in the file
            for match in data['matches']:
                match_details = {
                    "Match Name": match['event_name'],
                    "Tour Name": match['tour_name'],
                    "Venue": match['venue_name'],
                    "Date": match['start_date'],
                    "Result": match['event_sub_status'],
                    "Winning Margin": match['winning_margin']
                }

                for participant in match['participants']:
                    match_details[f"{participant['name']} Score"] = participant['value']

                matches_list.append(match_details)

        # Convert the list of dictionaries into a DataFrame
        df = pd.DataFrame(matches_list)

        df.to_csv("matches_data.csv", index=False)

        # Display the DataFrame
        return df






# Usage example
if __name__ == "__main__":
    api = KabaddiDataAPI()
    


    df = api.match_data(season=4)
    print(df)






    # for a season -> display all the match ids for that season along with some basic info about the match (matches overview)
    # for a given match-id -> get play-by-play data

    

    # for a given team in a given season return aggregated stats for that team
    # for a given team in a season, return the defender skills and raider skills for that team

    # return all matches played by that team


    # get team roster with player-ids
    # for a given player-id return aggregated stats about that player
    
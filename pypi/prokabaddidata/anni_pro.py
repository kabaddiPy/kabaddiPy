import json
from pathlib import Path
import pandas as pd
import json
import pandas as pd

import json
import pandas as pd
import glob

import os


class KabaddiDataAPI:
    
    # for a season - display the standings


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

            print(match_info)   
            matches.append(match_info)
        return matches

    def process_matches(self, matches_list):
        matches_df = pd.DataFrame(matches_list)
        matches_df = matches_df[(matches_df['result'].isin(['W', 'T'])) | (matches_df['result'].isnull())]
        matches_df = matches_df.sort_values(by='date', ascending=True)
        matches_df = matches_df.set_index('match_id').rename_axis('match id')
        return matches_df


    def get_pkl_standings(self, season=None, qualified=False, team_id=None, matches=False):
        
        if season is None:
            season = 10
        

        file_path = Path(f"./PKL_Standings/pkl_standings_s{season}.json")

        with open(file_path, 'r') as f:
            data = json.load(f)

        standings = data['standings']

        team_standings_info_list, qualified_teams_info_df, matches_list,  = [], [], []

        season_name = standings['series_name']
        champion_team_id = standings['champion_id']


        if len(standings['groups']) == 0:
            return pd.DataFrame()
    
        if len(standings['groups']) == 1:

            group = standings['groups'][0]
            if 'name' in group and group['name'] != "":
                group_name = group['name']
            else:
                group_name = 'Main'
            
            for team in group['teams']['team']:
                if team_id is None or int(team['team_id']) == team_id:
                    team_standings_info =  {
                        'Group': group_name,
                        'Season': season,
                        'Team_Id': team['team_id'],
                        'Team_Name': team['team_name'],
                        # 'team_short_name': team['team_short_name'],
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
                    
                    if qualified and team['is_qualified']:
                        qualified_teams_info_df.append(team_standings_info)
                    
                    team_standings_info_list.append(team_standings_info)

                    if matches:
                        matches_list.extend(self.create_matches_list(team, group_name))

        else:

            for group in standings['groups']:

                if 'name' in group and group['name'] != "":
                    group_name = group['name']
                else:
                    group_name = 'Main'
                
                for team in group['teams']['team']:
                    if team_id is None or int(team['team_id']) == team_id:
                        team_info =  {
                            'Group': group_name,
                            'Season': season,
                            'Team_Id': team['team_id'],
                            'Team_Name': team['team_name'],
                            # 'team_short_name': team['team_short_name'],
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
                        
                        if qualified and team['is_qualified']:
                            qualified_teams_info_df.append(team_info)
                        
                        team_standings_info_list.append(team_info)

                        if matches:
                            matches_list.extend(self.create_matches_list(team, group_name))

        team_info_df = pd.DataFrame(team_standings_info_list)

        if qualified:
            qualified_teams_df = pd.DataFrame(qualified_teams_info_df)
            return qualified_teams_df, team_info_df

        if matches:
            matches_df = self.process_matches(matches_list)
            return team_info_df, matches_df
        
        else:
            return team_info_df



        



    def get_match_overview(self, match_id, season):
        
        folder_path = "./Matches-Overview/"

        json_files = []

        files = os.listdir(folder_path)
        csv_files = [f for f in files if f.endswith('.json') and 'PKL_MatchData' in f]
        csv_files_sorted = sorted(csv_files, key=lambda x: int(x.split('_')[0][1:]))

        for file in csv_files_sorted:
            if file.endswith('.json'):
                
                with open(os.path.join(folder_path, file)) as f:
                    json_files.append(json.load(f))

        print(len(json_files))
        # print(json_files[0])

        all_matches = []


        data = json_files[season-1]
        print(data['matches'][0]['tour_name'])

        
        if f"Pro Kabaddi League Season {season}" in data['matches'][0]['tour_name']:
            for match in data['matches']:
            # General Details DataFrame

                team_name = []
                team_id = []

                for p in match['participants']:
                    print(p['name'])
                    team_name.append(p['name'])
                    team_id.append(p['id'])




                general_details = {
                    'match_id': match['game_id'],
                    'event_name': match['event_name'],
                    'tour_name': match['tour_name'],
                    'result_code': match['result_code'],
                    'season_id': match['series_id'],
                    'start_date': match['start_date'],
                    'end_date': match['end_date'],
                    'venue_name': match['venue_name'],
                    'venue_id': match['venue_id'],
                    'event_status': match['event_status'],
                    'event_sub_status': match['event_sub_status'],
                    'winning_margin': match['winning_margin'],
                    'event_stage': match['event_stage'],
                    'team_name_1': team_name[0],
                    'team_id_1': team_id[0],
                    'team_name_2': team_name[1],
                    'team_id_2': team_id[1]
                }

                all_matches.append(general_details)

            general_df = pd.DataFrame([general_details])

            # Participants DataFrame
            participants_data = []
            for participant in match['participants']:
                team_name = participant['name']
                team_id = participant['id']
                for player in participant['players_involved']:
                    player_data = {
                        'team_name': team_name,
                        'team_id': team_id,
                        'player_name': player['name'],
                        'player_id': player['id'],
                        'player_points': player['value'],
                        'player_type': player['type']
                    }
                    
                    participants_data.append(player_data)

            participants_df = pd.DataFrame(participants_data)

            return general_df, participants_df
        else:
            print(f"No match found for match_id {match_id} in season {season}")
            return None, None




    



    # def match_data(self, season="all"):
    #     matches_list = []
        
    #     # Determine the file(s) to load based on the season input
    #     if season == "all":
    #         files = glob.glob('./Matches-Overview/S*_PKL_MatchData.json')
    #     else:
    #         files = [f'./Matches-Overview/S{season}_PKL_MatchData.json']
        
    #     for file in files:
    #         with open(file) as f:
    #             data = json.load(f)

    #         # Loop over each match in the file
    #         for match in data['matches']:
    #             match_details = {
    #                 "Match Name": match['event_name'],
    #                 "Tour Name": match['tour_name'],
    #                 "Venue": match['venue_name'],
    #                 "Date": match['start_date'],
    #                 "Result": match['event_sub_status'],
    #                 "Winning Margin": match['winning_margin']
    #             }

    #             for participant in match['participants']:
    #                 match_details[f"{participant['name']} Score"] = participant['value']

    #             matches_list.append(match_details)

    #     # Convert the list of dictionaries into a DataFrame
    #     df = pd.DataFrame(matches_list)

    #     df.to_csv("matches_data.csv", index=False)

    #     # Display the DataFrame
    #     return df



if __name__ == "__main__":

    api = KabaddiDataAPI()

    # x = api.get_pkl_standings(season=6, qualified=False)
    # print(x)
    

    # print("-"*100, "test--", "-"*10,"\n\n")

    # x,y = api.get_pkl_standings(season=1, qualified=True)
    # print(x)
    # print("-"*100)
    # print(y)

    print("-"*100)

    x,y = api.get_match_overview(season=1, match_id=1)

    print(x)
    print("-"*100)
    print(y)

    # print(x.to_latex())

 
    # print(m)

    


    # df = api.match_data(season=4)
    # print(df)






    # for a season -> display all the match ids for that season along with some basic info about the match (matches overview)
    # for a given match-id -> get play-by-play data

    

    # for a given team in a given season return aggregated stats for that team
    # for a given team in a season, return the defender skills and raider skills for that team

    # return all matches played by that team


    # get team roster with player-ids
    # for a given player-id return aggregated stats about that player
    
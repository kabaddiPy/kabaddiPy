import json
import os
from pathlib import Path
from typing import List, Tuple, Dict, Any

import numpy as np
import pandas as pd
import json
import pandas as pd

import json
import pandas as pd
import glob
import re

from pandas import DataFrame


class KabaddiDataAPI:
    def __init__(self):
        self.base_path = "./MatchData_pbp"
    # for a season - display the standings

    def internal_create_matches_list(self, team, group_name):
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

    def internal_process_matches(self, matches_list):
        matches_df = pd.DataFrame(matches_list)
        matches_df = matches_df[(matches_df['result'].isin(['W', 'T'])) | (matches_df['result'].isnull())]
        matches_df = matches_df.sort_values(by='date', ascending=True)
        matches_df = matches_df.set_index('match_id').rename_axis('match id')
        return matches_df





    # DEPRECIATED
    def get_pkl_standings_matches(self, season=None, qualified=False, team_id=None, matches=False):

        if season is None:
            season = 10

        file_path = Path(f"./PKL_Standings/pkl_standings_s{season}.json")

        with open(file_path, 'r') as f:
            data = json.load(f)

        standings = data['standings']

        team_standings_info_list, qualified_teams_info_df, matches_list, = [], [], []

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
                    team_standings_info = {
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
                        matches_list.extend(self.internal_create_matches_list(team, group_name))

        else:

            for group in standings['groups']:

                if 'name' in group and group['name'] != "":
                    group_name = group['name']
                else:
                    group_name = 'Main'

                for team in group['teams']['team']:
                    if team_id is None or int(team['team_id']) == team_id:
                        team_info = {
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
                            matches_list.extend(self.internal_create_matches_list(team, group_name))

        team_info_df = pd.DataFrame(team_standings_info_list)

        if qualified:
            qualified_teams_df = pd.DataFrame(qualified_teams_info_df)
            return qualified_teams_df, team_info_df

        if matches:
            matches_df = self.internal_process_matches(matches_list)
            return team_info_df, matches_df

        else:
            return team_info_df


    def get_pkl_standings(self, season=None, qualified=False, team_id=None):
        
        if season is None:
            season = 10

        file_path = Path(f"./PKL_Standings/pkl_standings_s{season}.json")

        with open(file_path, 'r') as f:
            data = json.load(f)

        standings = data['standings']
        team_standings_info_list, qualified_teams_standings_info_list = [], []

        if len(standings['groups']) == 0:
            return pd.DataFrame()

        def process_team(group_name, team):
            team_info = {
                'Group': group_name,
                'Season': season,
                'Team_Id': team['team_id'],
                'Team_Name': team['team_name'],
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

            if (team_id is None or int(team['team_id']) == team_id):
                team_standings_info_list.append(team_info)
                if qualified and team['is_qualified']:
                    qualified_teams_standings_info_list.append(team_info)

        for group in standings['groups']:
            if 'name' in group and group['name'] != "":
                group_name = group['name']
            else:
                group_name = 'Main'
            for team in group['teams']['team']:
                process_team(group_name, team)

        team_info_df = pd.DataFrame(team_standings_info_list)

        if qualified:
            qualified_teams_df = pd.DataFrame(qualified_teams_standings_info_list)
            return qualified_teams_df, team_info_df

        return team_info_df


    def get_season_matches(self, season="all"):
        
        matches_list = []

        # Determine the file(s) to load based on the season input
        if season == "all":
            files = glob.glob('./Matches-Overview/S*_PKL_MatchData.json')
            # Sort the files based on the season number
            files = sorted(files, key=lambda x: int(re.search(r'S(\d+)', x).group(1)))
            print(files)

        else:
            files = [f'./Matches-Overview/S{season}_PKL_MatchData.json']

        for file in files:
            
            with open(file) as f:
                data = json.load(f)


            for match in data['matches']:

                team_name, team_id, team_score = [], [], []

                for p in match['participants']:
                    # print(p['name'])
                    team_name.append(p['name'])
                    team_id.append(p['id'])
                    team_score.append(p['value'])


                match_details = {
                    "Season": match['tour_name'].split(",")[0].split(" ")[-1],
                    'Match_ID': match['game_id'],
                    "Match_Name": match['event_name'],
                    "League_Stage": match['event_stage'],
                    "Year": match['tour_name'].split(",")[1].strip(),
                    "Venue": match['venue_name'].lower().title().strip(),
                    'Match_Outcome': match['event_sub_status'],
                    "Start_Date": match['start_date'],
                    "End_Date": match['end_date'],
                    "Result": match['result_code'],
                    "Winning Margin": match['winning_margin'],
                    'team_score_1': team_score[0],
                    'team_score_2': team_score[1],
                    'team_name_1': team_name[0],
                    'team_id_1': team_id[0],
                    'team_name_2': team_name[1],
                    'team_id_2': team_id[1],
                }

                

                matches_list.append(match_details)

        # Convert the list of dictionaries into a DataFrame
        df = pd.DataFrame(matches_list)

        df.to_csv("matches_data.csv")

        # Display the DataFrame
        return df


    def get_team_info(self, team_id, season='overall'):

        if season != 'overall':
            season = int(season)
        
        df_team_aggregated_stats = pd.read_csv("./Team-Wise-Data/PKL_AggregatedTeamStats.csv")
        df_team_raider_skills = pd.read_csv("./Team-Wise-Data/ALL_Raider_Skills_Merged.csv")
        df_team_defender_skills = pd.read_csv("./Team-Wise-Data/ALL_Defensive_Skills_Merged.csv")

        team_id = int(team_id)

        def find_team_column(dataframe, team_id):
            for col in dataframe.columns:
                if f"({team_id})" in col:
                    return col
            return None
        team_column_team_raider_skills = find_team_column(df_team_raider_skills, team_id)
        team_column_team_defender_skills = find_team_column(df_team_defender_skills, team_id)
        
        

        if season == 'overall':

            filtered_team_aggregated_stats = df_team_aggregated_stats[df_team_aggregated_stats['team_id'] == team_id]
            
            rows_overall = filtered_team_aggregated_stats[filtered_team_aggregated_stats['season'] == 'all']
            other_rows = filtered_team_aggregated_stats[filtered_team_aggregated_stats['season'] != 'all']

            filtered_team_aggregated_stats = pd.concat([rows_overall, other_rows]).reset_index(drop=True)
            filtered_team_raider_skills = None
            filtered_team_defender_skills = None

        
        else:

            df_team_aggregated_stats['team_id'] = pd.to_numeric(df_team_aggregated_stats['team_id'], errors='coerce')
            df_team_aggregated_stats['season'] = pd.to_numeric(df_team_aggregated_stats['season'], errors='coerce')
            
            filtered_team_aggregated_stats = df_team_aggregated_stats[df_team_aggregated_stats['season'] == season]
            filtered_team_aggregated_stats = filtered_team_aggregated_stats[filtered_team_aggregated_stats['team_id'] == team_id]

            if team_column_team_raider_skills:            
                filtered_team_raider_skills = df_team_raider_skills[df_team_raider_skills['Season'] == season]
                filtered_team_raider_skills = filtered_team_raider_skills[['Season','Skill Type','Skill Name',team_column_team_raider_skills]].reset_index(drop=True)
            else:
                filtered_team_raider_skills = None


            if team_column_team_defender_skills:
                filtered_team_defender_skills = df_team_defender_skills[df_team_defender_skills['Season'] == season]
                filtered_team_defender_skills = filtered_team_defender_skills[['Season','Skill Type','Skill Name',team_column_team_defender_skills]].reset_index(drop=True)
            else:
                filtered_team_defender_skills = None

        if filtered_team_aggregated_stats.empty:
            print(f"No data found in CSV for team_id {team_id} in season {season}")
            return None, None, None, None, None
        

        rank_columns = [col for col in filtered_team_aggregated_stats.columns if col.endswith('_rank')]
        value_columns = [col for col in filtered_team_aggregated_stats.columns if col.endswith('_value')]
        per_match_columns = [col for col in filtered_team_aggregated_stats.columns if col.endswith('_per-match')]

        # print(f"len rank cols: {len(rank_columns)}")
        # print(f"len value cols: {len(value_columns)}")
        # print(f"len per match cols: {len(per_match_columns)}")

        df_rank = filtered_team_aggregated_stats[['season', 'team_id', 'team_name' , 'matches_played'] + rank_columns]
        df_value = filtered_team_aggregated_stats[['season', 'team_id', 'team_name' , 'matches_played'] + value_columns]
        df_per_match = filtered_team_aggregated_stats[['season', 'team_id', 'team_name' , 'matches_played'] + per_match_columns]


        if season == 'overall':
            return df_rank, df_value, df_per_match, filtered_team_raider_skills, filtered_team_defender_skills
        else:
            return df_rank.T, df_value.T, df_per_match.T, filtered_team_raider_skills, filtered_team_defender_skills
            


    def get_team_matches(self, season, team_id :str):

        # pass

        df = self.get_season_matches(season=season)

        team_id = str(team_id)
        df = df[(df['team_id_1'] == team_id) | (df['team_id_2'] == team_id)]


        # print(df.columns)
        return df

        # matches_list = []

        # # Determine the file(s) to load based on the season input
        # if season == "all":
        #     files = glob.glob('./Matches-Overview/S*_PKL_MatchData.json')
        # else:
        #     files = [f'./Matches-Overview/S{season}_PKL_MatchData.json']

        # for file in files:
        #     with open(file) as f:
        #         data = json.load(f)

        #     # Loop over each match in the file
        #     for match in data['matches']:
        #         if match['participants'][0]['id']==team_id or  match['participants'][1]['id']==team_id:
        #             match_details = {
        #                 "Match Name": match['event_name'],
        #                 'Match ID': match['game_id'],
        #                 "Tour Name": match['tour_name'],
        #                 "Venue": match['venue_name'],
        #                 'Match_Outcome': match['event_sub_status'],
        #                 "Date": match['start_date'],
        #                 "Result": match['event_sub_status'],
        #                 "Winning Margin": match['winning_margin']
        #             }
        #             matches_list.append(match_details)
        #     df = pd.DataFrame(matches_list)
        #     return df
    

    def build_team_roster(self, team_id, season):
        roster = {}
        team_id = int(team_id)
        team_name = ""
        total_matches = 0

        for folder_name in os.listdir("./MatchData_pbp"):
            if f"Season_{season}" in folder_name:
                directory_path = os.path.join("./MatchData_pbp", folder_name)
                break
        else:
            print(f"No data found for season {season}")
            return pd.DataFrame()

        for filename in os.listdir(directory_path):
            if filename.endswith(".json"):
                file_path = os.path.join(directory_path, filename)
                with open(file_path, 'r') as f:
                    match_data = json.load(f)

                if 'gameData' in match_data:
                    match_data = match_data['gameData']

                series_dict = {10: '44', 9: '25', 8: '20', 7: '11', 6: '10', 5: '8', 3: '3', 2: '2', 1: '1', 4: '4'}
                season_id = series_dict.get(int(season))

                if int(match_data['match_detail']['series']['id']) == int(season_id):
                    for team in match_data['teams']['team']:
                        if int(team['id']) == team_id:
                            total_matches += 1
                            team_name = team['name']
                            for player in team['squad']:
                                player_id = player['id']
                                if player_id not in roster:
                                    roster[player_id] = {
                                        'Player ID': player_id,
                                        'Name': player['name'],
                                        'Jersey Number': player.get('jersey'),
                                        'Captain Count': 0,
                                        'Played Count': 0,
                                        'Green Card Count': 0,
                                        'Yellow Card Count': 0,
                                        'Red Card Count': 0,
                                        'Starter Count': 0,
                                        'Top Raider Count': 0,
                                        'Top Defender Count': 0,
                                        'Total Points': 0,
                                        'Team ID': team_id,
                                        'Team Name': team_name
                                    }
                                
                                roster[player_id]['Captain Count'] += int(player.get('captain', False))
                                roster[player_id]['Played Count'] += int(player.get('played', False))
                                roster[player_id]['Green Card Count'] += int(player.get('green_card', False))
                                roster[player_id]['Yellow Card Count'] += int(player.get('yellow_card', False))
                                roster[player_id]['Red Card Count'] += int(player.get('red_card', False))
                                roster[player_id]['Starter Count'] += int(player.get('starter', False))
                                roster[player_id]['Top Raider Count'] += int(player.get('top_raider', False))
                                roster[player_id]['Top Defender Count'] += int(player.get('top_defender', False))
                                roster[player_id]['Total Points'] += player.get('points', {}).get('total', 0)

        roster_df = pd.DataFrame(list(roster.values()))
        roster_df['Total Matches in Season'] = total_matches
        return roster_df


    def get_player_info(self, player_id, season=None):
        player_id = int(player_id)
        file_path = "./Player-Wise-Data/all_seasons_player_stats_rounded.csv"
        df = pd.read_csv(file_path)

        file_rvd = Path(r"./Player-Wise-Data/merged_raider_v_num_defenders_FINAL.csv")
        rvd_df = pd.read_csv(file_rvd)

        defend_file = "./Player-Wise-Data/AllSeasons_AllTeams_DefenderSuccessRate.csv"
        defend_df = pd.read_csv(defend_file)

        raider_file = "./Player-Wise-Data/AllSeasons_AllTeams_RaiderSuccessRate.csv"
        raider_df = pd.read_csv(raider_file)

        player_starts = "./Player-Wise-Data/Player_Team_Lineup_merged.csv"
        player_starts_df = pd.read_csv(player_starts)

        def to_numeric_or_nan(x):
            try:
                return pd.to_numeric(x)
            except ValueError:
                return np.nan

        df['player_id'] = df['player_id'].apply(to_numeric_or_nan)
        df['player_id'] = df['player_id'].fillna(-1)
        df['player_id'] = df['player_id'].astype(np.int64)

        rvd_df['player-id'] = rvd_df['player-id-pkdc-sanitised'].apply(to_numeric_or_nan)
        rvd_df['player-id'] = rvd_df['player-id'].fillna(-1)
        rvd_df['player-id'] = rvd_df['player-id'].astype(int)


        defend_df['player_id'] = defend_df['player_id_copy_backup'].apply(to_numeric_or_nan)
        defend_df['player_id'] = defend_df['player_id'].fillna(-1)
        defend_df['player_id'] = defend_df['player_id'].astype(np.int64)

        raider_df['player_id'] = raider_df['player-id-clean'].apply(to_numeric_or_nan)
        raider_df['player_id'] = raider_df['player_id'].fillna(-1)
        raider_df['player_id'] = raider_df['player_id'].astype(np.int64)

        player_starts_df['player_id'] = player_starts_df['player_id_clean'].apply(to_numeric_or_nan)
        player_starts_df['player_id'] = player_starts_df['player_id'].fillna(-1)
        player_starts_df['player_id'] = player_starts_df['player_id'].astype(np.int64)

        # If season is not specified, use the latest season
        if season is None:
            season = df['season'].max()

        # Player aggregated stats
        player_stats_df = df[(df['player_id'] == player_id) & (df['season'] == season)]

        if player_stats_df.empty:
            print(f"No data for player {player_id} for season {season} |  AGGREGATED")

        player_starts_df = player_starts_df[(player_starts_df['player_id'] == player_id) & (player_starts_df['season_num'] == season)]
        if player_starts_df.empty:
            print(f"No data for player {player_id} for season {season} |  STARTS")

        # Raiders v defenders
        rvd_data = rvd_df[rvd_df['player-id'] == player_id]
        if rvd_data.empty:
            print(f"No data for raiders v no of defenders for {player_id}")
        
        rvd_extracted_df = rvd_data[rvd_data['season'].str.extract(r'(\d+)')[0].astype(int) == season]
        if rvd_extracted_df.empty:
            print(f"No data for raiders v no of defenders for {player_id} for season {season}")


        defend_extracted_df = defend_df[(defend_df['player_id'] == player_id) & (defend_df['season'] == season)]
        if defend_extracted_df.empty:
            print(f"No data for defenders for {player_id} for season {season}")
        
        raider_extracted_df = raider_df[(raider_df['player_id'] == player_id) & (raider_df['season'] == season)]
        if raider_extracted_df.empty:
            print(f"No data for raiders for {player_id} for season {season}")
        
        player_stats_df_rank = player_stats_df[["season", "player_id", "player_name", "player_matches_played", "player_position_id", "player_position_name", "team_id", "team_full_name", "player-super-tackles_rank", "player-raid-points_rank", "player-super-raids_rank", "player-high-5s_rank", "player-tackle-points_rank", "player-avg-tackle-points_rank", "player-dod-raid-points_rank", "player-total-points_rank", "player-successful-tackles_rank", "player-successful-raids_rank", "super-10s_rank" ]].copy()
                                                
        player_stats_df_value = player_stats_df[["season", "player_id", "player_name", "player_matches_played", "player_position_id", "player_position_name", "team_id", "team_full_name", "player-super-tackles_value", "player-raid-points_value", "player-super-raids_value", "player-high-5s_value", "player-tackle-points_value", "player-avg-tackle-points_value", "player-dod-raid-points_value", "player-total-points_value", "player-successful-tackles_value", "player-successful-raids_value", "super-10s_value"]].copy()
                                    
        player_stats_df_per_match = player_stats_df[["season", "player_id", "player_name", "player_matches_played", "player_position_id", "player_position_name", "team_id", "team_full_name", "player-super-tackles_points_per_match", "player-raid-points_points_per_match", "player-super-raids_points_per_match", "high-5s_points_per_match", "player-tackle-points_points_per_match", "player-dod-raid-points_points_per_match", "player-total-points_points_per_match", "player-successful-tackles_points_per_match", "player-successful-raids_points_per_match", "super-10s_points_per_match"]].copy()


        if not defend_extracted_df.empty:
            defend_data = defend_extracted_df.iloc[0]
            player_stats_df_value['Total Tackles'] = defend_data.get('Total Tackles', np.nan)
            player_stats_df_value['Successful Tackles'] = defend_data.get('Successful Tackles', np.nan)
            player_stats_df_value['Defender Success Rate'] = defend_data.get('Defender Success rate', np.nan)


        if not raider_extracted_df.empty:
            raider_data = raider_extracted_df.iloc[0]
            player_stats_df_value['Total Raids'] = raider_data.get('Total Raids', np.nan)
            player_stats_df_value['Successful Raids'] = raider_data.get('Successful Raids', np.nan)
            player_stats_df_value['Raider Success Rate'] = raider_data.get('Raider Success Rate', np.nan)

        if not player_starts_df.empty:
            player_starts_data = player_starts_df.iloc[0]
            player_stats_df_value['Total Played'] = player_starts_data.get('Total Played', np.nan)
            player_stats_df_value['Total Starts'] = player_starts_data.get('Total Starts', np.nan)

        rvd_extracted_df = rvd_extracted_df[['Season_Number', 'Team Name',
                                            'player-id', 'Raider Name', 'Number of Defenders', 'Total Raids',
                                            'Percentage of Raids', 'Empty Raids Percentage',
                                            'Successful Raids Percentage']]
        
        

        return player_stats_df_rank.T, player_stats_df_value.T, player_stats_df_per_match.T, rvd_extracted_df.T


    def load_match_details(self, season, match_id) -> Tuple[DataFrame, DataFrame, DataFrame, DataFrame, DataFrame, DataFrame]:
        """
        Get the full data for a specific match.

        Args:
            season (str): The season name.
            match_id (str): The match ID.

        Returns:
            Tuple[DataFrame, DataFrame, DataFrame, DataFrame, DataFrame, DataFrame]:
            A tuple containing match detail, teams, events, zones, team1, and team2 DataFrames.
        """

        # print(f"Loading match details for season {season} and match ID {match_id}")

        for dir in os.listdir(self.base_path):
            if f"Season_PKL_Season_{season}" in dir:
                season_path = os.path.join(self.base_path, dir)
                break
        else:
            raise ValueError(f"No season data found for season {season}")
        
        file_name = next((f for f in os.listdir(season_path) if f.endswith(f'_ID_{match_id}.json')), None)

        if not file_name:
            raise FileNotFoundError(f"No match file found for season {season} and match ID {match_id}")

        file_path = os.path.join(season_path, file_name)

        try:
            with open(file_path, 'r') as file:
                temp = json.load(file)

            # Check if the data is nested under 'gameData'
            if 'gameData' in temp:
                temp = temp['gameData']

            match_detail = temp.get("match_detail", {})
            flattened_match_detail = self._flatten_match_detail(match_detail)
            # print(f"Flattened match detail: {flattened_match_detail}")
            # print(f"Flattened match detail columns: {flattened_match_detail.keys()}")
            # print("-"*100)
            # print(f"Match detail: {match_detail}")
            match_detail_df = pd.DataFrame([flattened_match_detail])

            events_df = pd.DataFrame(temp.get("events", {}).get("event", []))
            zones_df = pd.DataFrame(temp.get("zones", {}).get("zone", []))

            teams_data = temp.get("teams", {}).get("team", [])

            if len(teams_data) != 2:
                raise ValueError("Expected data for exactly two teams")

            team1_df, team2_df = self._process_team_data(teams_data)
            teams_df = pd.DataFrame(teams_data)

            return match_detail_df, teams_df, events_df, zones_df, team1_df, team2_df

        except Exception as e:
            print(f"Error loading data from {file_path}: {str(e)}")
            return None, None, None, None, None, None

    
    def load_pbp_data(self, season, match_id) -> DataFrame:
        """
        Get all events for a specific match.

        Args:
            season (str): The season name.
            match_id (str): The match ID.

        Returns:
            DataFrame: A DataFrame containing all events in the match.
        """
        _, _, events_df, _, _, _ = self.load_match_details(season, match_id)
        return events_df


    def _flatten_match_detail(self, match_detail: Dict[str, Any]) -> Dict[str, Any]:
        """
        Flatten nested dictionaries in match detail.

        Args:
            match_detail (Dict[str, Any]): The match detail dictionary.

        Returns:
            Dict[str, Any]: Flattened match detail dictionary.
        """
        flattened = {}
        for key, value in match_detail.items():
            if isinstance(value, dict):
                for subkey, subvalue in value.items():
                    flattened[f"{key}_{subkey}"] = subvalue

            elif isinstance(value, list):
                if key == "player_of_the_match":
                    flattened[f"{key}_id"] = value[0].get("id") if value else None
                    flattened[f"{key}_value"] = value[0].get("value") if value else None
                else:
                    flattened[key] = json.dumps(value)
            else:
                flattened[key] = value
        return flattened

    def _process_team_data(self, teams_data: List[Dict[str, Any]]) -> Tuple[DataFrame, DataFrame]:
        """
        Process team data into DataFrames.

        Args:
            teams_data (List[Dict[str, Any]]): List containing data for both teams.

        Returns:
            Tuple[DataFrame, DataFrame]: DataFrames for team1 and team2.
        """

        def process_squad(squad_data):
            processed_squad = []
            for player in squad_data:
                player_dict = {
                    'id': player['id'],
                    'name': player['name'],
                    'jersey': player.get('jersey', ''),
                    'played': player.get('played', False),
                    'captain': player.get('captain', False),
                    'on_court': player.get('on_court', False),
                    'starter': player.get('starter', False),
                    'red_card': player.get('red_card', False),
                    'yellow_card': player.get('yellow_card', False),
                    'green_card': player.get('green_card', False),
                    'red_card_count': player.get('red_card_count', 0),
                    'yellow_card_count': player.get('yellow_card_count', 0),
                    'green_card_count': player.get('green_card_count', 0),
                    'top_raider': player.get('top_raider', False),
                    'top_defender': player.get('top_defender', False),
                    'total_points': player.get('points', {}).get('total', 0),
                    'raid_points': player.get('points', {}).get('raid_points', {}).get('total', 0),
                    'tackle_points': player.get('points', {}).get('tackle_points', {}).get('total', 0),
                    'raids_total': player.get('raids', {}).get('total', 0),
                    'raids_successful': player.get('raids', {}).get('successful', 0),
                    'tackles_total': player.get('tackles', {}).get('total', 0),
                    'tackles_successful': player.get('tackles', {}).get('successful', 0),
                }
                for zone_type in ['strong_zones', 'weak_zones']:
                    for zone in player.get(zone_type, {}).get(zone_type.rstrip('s'), []):
                        player_dict[f"{zone_type}_zone_{zone['zone_id']}"] = zone['points']
                processed_squad.append(player_dict)
            return processed_squad

        team1_df = pd.DataFrame(process_squad(teams_data[0].get('squad', [])))
        team2_df = pd.DataFrame(process_squad(teams_data[1].get('squad', [])))

        for team_df, team_data in zip([team1_df, team2_df], teams_data):
            team_df['team_id'] = team_data['id']
            team_df['team_name'] = team_data['name']
            team_df['team_score'] = team_data['score']
            team_df['team_short_name'] = team_data['short_name']

        return team1_df, team2_df









# # Usage example
if __name__ == "__main__":
    api = KabaddiDataAPI()


    # print("get standings")
    # # x = api.get_pkl_standings(season=10)
    # # print(x)


    qualified_df , all_standings_df = api.get_pkl_standings_matches(season=9, qualified=True)
    print("qualified_df")
    print(qualified_df)
    print()

    # print("all_standings_df")
    # print(all_standings_df)
    # print(len(all_standings_df))

    print("season_matches")
    matches = api.get_season_matches(season=6)
    print(matches)
    # print(len(x))


    # print("-"*100)
    print("team_info")

    df_rank_, df_value_, df_per_match_, filtered_team_raider_skills_, filtered_team_defender_skills_ = api.get_team_info(season=6,team_id=29)

    print("Rank DFs")
    print(df_rank_)
    print("-"*100)
    print("Value DFs")
    print(df_value_)
    print("-"*100)
    print("Per Match DFs")
    print(df_per_match_)
    print("-"*100)
    print("Raider Skills")
    print(filtered_team_raider_skills_)
    print("-"*100)
    print("Defender Skills")
    print(filtered_team_defender_skills_)

    #TODO: Fix the order of the columns in the output
    # team-successful-tackle-percent_value
    # team-super-tackles_value
    # team-tackle-points_value
    # team-successful-tackles-per-match_value
    # team-average-tackle-points_value
    # team-successful-tackles_value
    # Total_touch_points_value
    # Total_bonus_points_value
    # team-raid-points_value
    # team-average-raid-points_value
    # team-successful-raids_value
    # team-super-raid_value
    # team-raid_value
    # team-successful-raid-percent_value
    # team-dod-raid-points_value
    # team-total-points_value
    # team-all-outs-conceded_value
    # team-all-outs-inflicted_value
    # team-avg-points-scored_value
    # team-total-points-conceded_value


    print("get_team_matches\n\n")

    df = api.get_team_matches(season=9, team_id=3)
    print(df)



    print("build build_team_roster")

    df = api.build_team_roster(season=9, team_id='3')
    print("-"*100)
    print(df)

    ## df.to_csv("team_roster.csv")


    print("build get_player_info")

    _player_stats_df_rank, _player_stats_df_value, _player_stats_df_per_match, _rvd_extracted_df = api.get_player_info(player_id=660, season=9)
    print("-"*100)
    print(_player_stats_df_rank)
    print("-"*100)
    print(_player_stats_df_value)
    print("-"*100)
    print(_player_stats_df_per_match)
    print("-"*100)
    print(_rvd_extracted_df)


    print("load_match_details-------\n\n\n")
    _match_detail_df, _teams_df, _events_df, _zones_df, _team1_df, _team2_df = api.load_match_details(season='9', match_id='2895')
    print("-"*100)
    print(_match_detail_df)
    print("-"*100)
    print(_teams_df)
    print("-"*100)
    print(_events_df)
    print("-"*100)
    print(_zones_df)
    print("-"*100)
    print(_team1_df)
    print("-"*100)
    print(_team2_df)


    print("load_pbp_data")
    _pbp_df = api.load_pbp_data(season=9, match_id='2895')
    print("-"*100)
    print(_pbp_df)























    # print(api.get_available_seasons())


    # match_detail_df, teams_df, events_df, zones_df, team1_df, team2_df = api.get_match_data('Season_PKL_Season_4_2016',
    #                                                                                         '194')
    # print(events_df)






    # x = api.build_team_roster('4',9)
    # print(x)
    # x = api.get_team_matches('5','4')
    # print(x)

    # x = api.get_season_matches('10')
    # print(x)

    # x = api.get_team_info(4)
    # print(x)

    # player_stats, rvd,defend_df= api.get_player_info(322,9)
    # print(player_stats)
    # print(rvd)
    # print(defend_df)


    # x = api.get_pkl_standings(season=7, qualified=False)
    # print(x)
    # # print("-"*100)
    # # print(y)
    ###########################################
    # print("-" * 100, "test--", "-" * 100)
    #
    # x, y = api.get_pkl_standings(season=1, qualified=True)
    # print(x)
    # print("-" * 100)
    # print(y)
    #
    # print("-" * 100)

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

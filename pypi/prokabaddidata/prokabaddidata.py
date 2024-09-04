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

        team_info_df = pd.DataFrame(team_standings_info_list)

        if qualified:
            qualified_teams_df = pd.DataFrame(qualified_teams_info_df)
            return qualified_teams_df, team_info_df

        else:
            return team_info_df


    def get_season_matches(self, season="all"):
        matches_list = []

        # Determine the file(s) to load based on the season input
        if season == "all":
            files = glob.glob('./Matches-Overview/S*_PKL_MatchData.json')
            print(files)
        else:
            files = [f'./Matches-Overview/S{season}_PKL_MatchData.json']

        for file in files:
            with open(file) as f:
                data = json.load(f)

            # Loop over each match in the file
            for match in data['matches']:
                match_details = {
                    "Match Name": match['event_name'],
                    'Match ID': match['game_id'],
                    "Tour Name": match['tour_name'],
                    "Venue": match['venue_name'],
                    'Match_Outcome': match['event_sub_status'],
                    "Date": match['start_date'],
                    "Result": match['event_sub_status'],
                    "Winning Margin": match['winning_margin']
                }

                for participant in match['participants']:
                    match_details[f"{participant['name']} Score"] = participant['value']

                matches_list.append(match_details)

        # Convert the list of dictionaries into a DataFrame
        df = pd.DataFrame(matches_list)

        #df.to_csv("matches_data.csv", index=False)

        # Display the DataFrame
        return df


    def get_team_matches(self,season,team_id :str):
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
                if match['participants'][0]['id']==team_id or  match['participants'][1]['id']==team_id:
                    match_details = {
                        "Match Name": match['event_name'],
                        'Match ID': match['game_id'],
                        "Tour Name": match['tour_name'],
                        "Venue": match['venue_name'],
                        'Match_Outcome': match['event_sub_status'],
                        "Date": match['start_date'],
                        "Result": match['event_sub_status'],
                        "Winning Margin": match['winning_margin']
                    }
                    matches_list.append(match_details)
            df = pd.DataFrame(matches_list)
            return df
    
    def get_team_info(self, team_id, season='overall'):

        if season != 'overall':
            season = int(season)
        df = pd.read_csv("../prokabaddidata/Team-Wise-Data/PKL_AggregatedTeamStats.csv")

        df['team_id'] = pd.to_numeric(df['team_id'], errors='coerce')
        df['season'] = pd.to_numeric(df['season'], errors='coerce')

        team_id = int(team_id)

        if season == 'overall':
            all_row = df[(df['team_id'] == team_id) & (df['season'] == 'all')]
            other_rows = df[(df['team_id'] == team_id) & (df['season'] != 'all')]
            filtered_df = pd.concat([all_row, other_rows]).reset_index(drop=True)
        else:
            filtered_df = df[(df['team_id'] == team_id) & (df['season'] == season)]

        if filtered_df.empty:
            print(f"No data found in CSV for team_id {team_id} in season {season}")
            return None, None, None, None, None
        if season == 'overall':
            standings_df, matches_df = self.get_pkl_standings(season=10, team_id=team_id, matches=True)
        else:
            standings_df, matches_df = self.get_pkl_standings(season, team_id=team_id, matches=True)
        standings_df = None
        matches_df = None
        # Separate the columns based on the suffixes
        rank_columns = [col for col in filtered_df.columns if col.endswith('_rank')]
        value_columns = [col for col in filtered_df.columns if col.endswith('_value')]
        per_match_columns = [col for col in filtered_df.columns if col.endswith('_per-match')]

        df_rank = filtered_df[['season', 'team_id', 'team_name'] + rank_columns]
        df_value = filtered_df[['season', 'team_id', 'team_name'] + value_columns]
        df_per_match = filtered_df[['season', 'team_id', 'team_name'] + per_match_columns]

        return df_rank, df_value, df_per_match, standings_df, matches_df

    def get_player_info(self, player_id, season=None):
        player_id = int(player_id)
        file_path = "./Player-Wise-Data/all_seasons_player_stats_rounded.csv"
        df = pd.read_csv(file_path)
        file_rvd = r"./Player-Wise-Data/merged_raider_v_num_defenders_FINAL.csv"
        rvd_df = pd.read_csv(file_rvd)

        # raid_file = "./Player-Wise-Data/AllSeasons_AllTeams_RaiderSuccessRate.csv"
        # raid_df = pd.read_csv(raid_file)

        defend_file = "./Player-Wise-Data/AllSeasons_AllTeams_DefenderSuccessRate.csv"
        defend_df = pd.read_csv(defend_file)

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

        # If season is not specified, use the latest season
        if season is None:
            season = df['season'].max()

        # Player aggregated stats
        player_stats_df = df[(df['player_id'] == player_id) & (df['season'] == season)]

        # Raiders v defenders
        rvd_data = rvd_df[rvd_df['player-id'] == player_id]
        if rvd_data.empty:
            print(f"No data for raiders v no of defenders for {player_id}")
        rvd_extracted_df = rvd_data[rvd_data['season'].str.extract(r'(\d+)')[0].astype(int) == season]

        defend_extracted_df = defend_df[(defend_df['player_id'] == player_id) & (defend_df['season'] == season)]

        if player_stats_df.empty:
            print(f"Data not available for player_id {player_id} for season {season}")

        if rvd_extracted_df.empty:
            print(f"Raiders vs defenders data not available for player_id {player_id} for season {season}")
        if defend_extracted_df.empty:
            print(f"successful defender rate not available for player_id {player_id} for season {season}")

        return player_stats_df, rvd_extracted_df, defend_extracted_df

    def build_team_roster(self,team_id, season_number):
        roster = []  # Initialize the roster list

        for i in os.listdir("./MatchData_pbp"):
            if f"Season_{season_number}" in i:
                break

        directory_path = os.path.join("./MatchData_pbp", i)

        # print(f"Starting to build the roster for Team ID: {team_id}, Season: {season_number}...\n")

        # Iterate over all files in the directory
        for filename in os.listdir(directory_path):
            if filename.endswith(".json"):  # Process only JSON files
                file_path = os.path.join(directory_path, filename)
                # print(f"Loading file: {filename}")

                with open(file_path, 'r') as f:
                    match_data = json.load(f)
                    if season_number == 4:

                        # Check if the match belongs to the specified season
                        if match_data['match_detail']['series']['id'] == season_number:

                            # print(f"Processing match ID: {match_data['match_detail']['match_id']}")

                            teams = match_data['teams']['team']
                            for team in teams:
                                if team['id'] == team_id:
                                    # print(f"Found team {team['name']} (ID: {team_id}) in the match.")
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
                    else:
                        series_dict = {
                            10: '44',
                            9: '25',
                            8: '20',
                            7: '11',
                            6: '10',
                            5: '8',
                            3: '3',
                            2: '2',
                            1: '1'
                        }
                        season = series_dict.get(season_number)

                        if int(match_data['gameData']['match_detail']['series']['id']) == int(season):

                            teams = match_data['gameData']['teams']['team']
                            for team in teams:
                                if team['id'] == team_id:
                                    squad = team['squad']
                                    for player in squad:
                                        player_id = player['id']
                                        player_name = player['name']

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
                        else:
                            print("season not found.")

        roster_df = pd.DataFrame(roster)
        return roster_df

    def get_available_seasons(self) -> List[str]:
        """
        Get a list of available seasons in the dataset.

        Returns:
            List[str]: A list of season names.
        """
        return [folder for folder in os.listdir(self.base_path)
                if os.path.isdir(os.path.join(self.base_path, folder))]

    def get_matches_for_season(self, season: str) -> List[str]:
        """
        Get a list of match IDs for a specific season.

        Args:
            season (str): The season name.

        Returns:
            List[str]: A list of match IDs.
        """
        season_path = os.path.join(self.base_path, season)
        return [file.split('_ID_')[1].split('.')[0] for file in os.listdir(season_path) if file.endswith('.json')]


    # def get_match_data(self, season: str, match_id: str) -> Tuple[DataFrame, DataFrame, DataFrame, DataFrame, DataFrame, DataFrame]:
    #     """
    #     Get the full data for a specific match.
    #
    #     Args:
    #         season (str): The season name.
    #         match_id (str): The match ID.
    #
    #     Returns:
    #         Tuple[DataFrame, DataFrame, DataFrame, DataFrame, DataFrame, DataFrame]:
    #         A tuple containing match detail, teams, events, zones, team1, and team2 DataFrames.
    #     """
    #     season_path = os.path.join(self.base_path, season)
    #     file_name = next((f for f in os.listdir(season_path) if f.endswith(f'_ID_{match_id}.json')), None)
    #
    #     if not file_name:
    #         raise FileNotFoundError(f"No match file found for season {season} and match ID {match_id}")
    #
    #     file_path = os.path.join(season_path, file_name)
    #
    #     try:
    #         with open(file_path, 'r') as file:
    #             temp = json.load(file)
    #             match_detail = temp.get("match_detail", {})
    #             match_detail = match_detail.get("match_detail",{})
    #         flattened_match_detail = self._flatten_match_detail(match_detail)
    #         match_detail_df = pd.DataFrame([flattened_match_detail])
    #
    #         events_df = pd.DataFrame(temp.get("events", {}).get("event", []))
    #         zones_df = pd.DataFrame(temp.get("zones", {}).get("zone", []))
    #
    #         teams_data = temp.get("teams", {}).get("team", [])
    #         if len(teams_data) != 2:
    #             raise ValueError("Expected data for exactly two teams")
    #
    #         team1_df, team2_df = self._process_team_data(teams_data)
    #         teams_df = pd.DataFrame(teams_data)
    #
    #         return match_detail_df, teams_df, events_df, zones_df, team1_df, team2_df
    #
    #     except Exception as e:
    #         print(f"Error loading data from {file_path}: {str(e)}")
    #         return None, None, None, None, None, None


    def get_match_data(self, season: str, match_id: str) -> Tuple[
        DataFrame, DataFrame, DataFrame, DataFrame, DataFrame, DataFrame]:
        """
        Get the full data for a specific match.

        Args:
            season (str): The season name.
            match_id (str): The match ID.

        Returns:
            Tuple[DataFrame, DataFrame, DataFrame, DataFrame, DataFrame, DataFrame]:
            A tuple containing match detail, teams, events, zones, team1, and team2 DataFrames.
        """
        season_path = os.path.join(self.base_path, season)
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
    
    def get_match_events(self, season: str, match_id: str) -> DataFrame:
        """
        Get all events for a specific match.

        Args:
            season (str): The season name.
            match_id (str): The match ID.

        Returns:
            DataFrame: A DataFrame containing all events in the match.
        """
        _, _, events_df, _, _, _ = self.get_match_data(season, match_id)
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

    x = api.get_pkl_standings(season=3)
    print(x)


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

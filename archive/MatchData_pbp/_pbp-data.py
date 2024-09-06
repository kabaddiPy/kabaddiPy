import os
import json
import pandas as pd
from typing import List, Dict, Any, Tuple
from pandas import DataFrame


class KabaddiAPI:
    def __init__(self, base_path: str):
        self.base_path = "../MatchData_pbp"

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

# api = KabaddiDataAPI("../MatchData_pbp")
# #
# # seasons = api.get_available_seasons() #works
# # matches = api.get_matches_for_season("Season_Pro Kabaddi League Season 1, 2014") #works
# # match_events = api.get_match_events('Season_Pro Kabaddi League Season 1, 2014', '60') #works
#
# match_detail_df, teams_df, events_df, zones_df, team1_df, team2_df = api.get_match_data('Season_PKL_Season_4_2016', '194')
#
#
# df2 = team1_df
# print(df2)
# print(df2.columns)
# print(api.get_match_events('Season_PKL_Season_5_2017','300'))
for i in
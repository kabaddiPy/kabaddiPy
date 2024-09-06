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

    def get_pkl_standings(self, season=None, qualified=False, team_id=None):
        """
        Retrieve the Pro Kabaddi League (PKL) standings for a specified season.

        Parameters:
        -----------
        season : int, optional
            The season number for which to retrieve standings. Defaults to 10 if not specified.
        qualified : bool, optional
            If True, returns an additional DataFrame with only qualified teams. Defaults to False.
        team_id : int, optional
            If specified, returns standings for only this team. Defaults to None (all teams).

        Returns:
        --------
        pandas.DataFrame or tuple of pandas.DataFrame
            If qualified is False:
                Returns a DataFrame containing standings for all teams.
            If qualified is True:
                Returns a tuple of two DataFrames:
                (qualified_teams_standings, all_teams_standings)

        The DataFrame(s) include the following columns:
        - Group: The group name (if applicable)
        - Season: The season number
        - Team_Id: Unique identifier for the team
        - Team_Name: Name of the team
        - League_position: Current position in the league
        - Matches_played: Number of matches played
        - Wins, Lost, Tied, Draws: Match outcomes
        - No Result: Number of matches with no result
        - League_points: Total points in the league
        - Score_diff: Score difference
        - Qualified: Boolean indicating if the team qualified

        Raises:
        -------
        FileNotFoundError: If the standings file for the specified season is not found.
        JSONDecodeError: If there's an issue parsing the JSON file.

        Note:
        -----
        If the standings data for the specified season is empty, an empty DataFrame is returned.
        """
    # ... (rest of the function implementation remains the same)
        
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
        """
        Retrieve match data for a specific season or all seasons.

        This function loads match data from JSON files and returns it as a pandas DataFrame.

        Parameters:
        -----------
        season : str or int, optional
            The season number for which to retrieve match data. 
            Use "all" to retrieve data for all seasons (default).
            If a specific season is desired, provide the season number as a string or integer.

        Returns:
        --------
        pandas.DataFrame
            A DataFrame containing match details with the following columns:
            - Season: The season number
            - Match_ID: Unique identifier for the match
            - Match_Name: Name of the match event
            - League_Stage: Stage of the league (e.g., group stage, playoffs)
            - Year: Year of the match
            - Venue: Location where the match was played
            - Match_Outcome: Outcome of the match
            - Start_Date: Start date and time of the match
            - End_Date: End date and time of the match
            - Result: Result code of the match
            - Winning Margin: Margin of victory
            - team_score_1: Score of the first team
            - team_score_2: Score of the second team
            - team_name_1: Name of the first team
            - team_id_1: ID of the first team
            - team_name_2: Name of the second team
            - team_id_2: ID of the second team

        Notes:
        ------
        - The function reads data from JSON files located in the './Matches-Overview/' directory.
        - For "all" seasons, it sorts the files based on the season number extracted from the filename.
        - Each row in the returned DataFrame represents a single match.
        """
        
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

        # df.to_csv("matches_data.csv")

        # Display the DataFrame
        return df


    def get_team_info(self, team_id=None, season='overall'):
        """
        Retrieve team information for a specific team and season.

        This function fetches aggregated statistics, raider skills, and defender skills
        for a given team in a specified season or across all seasons.

        Parameters:
        -----------
        team_id : int
            The unique identifier for the team.
        season : str or int, optional
            The season for which to retrieve data. Can be:
            - 'overall' (default): Retrieves data across all seasons.
            - int: A specific season number.

        Returns:
        --------
        tuple
            A tuple containing five elements:
            1. df_rank (DataFrame): Team rankings in various categories.
            2. df_value (DataFrame): Raw statistic values for the team.
            3. df_per_match (DataFrame): Per-match statistics for the team.
            4. filtered_team_raider_skills (DataFrame or None): Raider skills data for the team.
            5. filtered_team_defender_skills (DataFrame or None): Defender skills data for the team.

        Notes:
        ------
        - If season is 'overall', raider and defender skills data are not returned (set to None).
        - For a specific season, all DataFrames are transposed for easier reading.
        - If no data is found for the specified team and season, all return values will be None.

        Raises:
        -------
        ValueError: If the input types are incorrect or if the season is invalid.
        """
        if season != 'overall':
            season = int(season)
        
        df_team_aggregated_stats = pd.read_csv("./Team-Wise-Data/PKL_AggregatedTeamStats.csv")
        df_team_raider_skills = pd.read_csv("./Team-Wise-Data/ALL_Raider_Skills_Merged.csv")
        df_team_defender_skills = pd.read_csv("./Team-Wise-Data/ALL_Defensive_Skills_Merged.csv")
        
        if team_id:
            team_id = int(team_id)
        else:
            team_id=None

        def find_team_column(dataframe, team_id):
            for col in dataframe.columns:
                if f"({team_id})" in col:
                    return col
            return None
        
        if team_id:
            team_column_team_raider_skills = find_team_column(df_team_raider_skills, team_id)
            team_column_team_defender_skills = find_team_column(df_team_defender_skills, team_id)
        else:
            team_column_team_raider_skills = -1
            team_column_team_defender_skills = -1
        
        

        if season == 'overall':
            
            if team_id:
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
            
            if team_id:
                filtered_team_aggregated_stats = filtered_team_aggregated_stats[filtered_team_aggregated_stats['team_id'] == team_id]

            if team_column_team_raider_skills:            
                filtered_team_raider_skills = df_team_raider_skills[df_team_raider_skills['Season'] == season]
                
                if team_column_team_raider_skills == -1:
                    cols = filtered_team_raider_skills.columns.tolist()
                    filtered_team_raider_skills = filtered_team_raider_skills[[cols]].reset_index(drop=True)

                else:
                    filtered_team_raider_skills = filtered_team_raider_skills[['Season','Skill Type','Skill Name',team_column_team_raider_skills]].reset_index(drop=True)
            else:
                filtered_team_raider_skills = None


            if team_column_team_defender_skills:
                filtered_team_defender_skills = df_team_defender_skills[df_team_defender_skills['Season'] == season]
                
                if team_column_team_raider_skills == -1:
                    cols = filtered_team_defender_skills.columns.tolist()
                    filtered_team_defender_skills = filtered_team_defender_skills[[cols]].reset_index(drop=True)

                else:
                    filtered_team_defender_skills = filtered_team_defender_skills[['Season','Skill Type','Skill Name',team_column_team_raider_skills]].reset_index(drop=True)

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
            


    def get_team_ids(self, season):
        
        return pd.DataFrame(self.get_pkl_standings(season=season)[['Team_Id', 'Team_Name']].to_dict(orient='records'))

    

    def get_team_matches(self, season, team_id :str):
        """
        Retrieve all matches for a specific team in a given season.

        This function filters the season's matches to return only those involving the specified team.

        Parameters:
        -----------
        season : int or str
            The season number for which to retrieve matches.
        team_id : str
            The unique identifier for the team.

        Returns:
        --------
        pandas.DataFrame
            A DataFrame containing match details for the specified team, including:
            - Match_ID: Unique identifier for the match
            - Match_Name: Name of the match event
            - Start_Date: Start date and time of the match
            - Venue: Location where the match was played
            - team_name_1, team_id_1: Name and ID of the first team
            - team_name_2, team_id_2: Name and ID of the second team
            - team_score_1, team_score_2: Scores of both teams
            - And other relevant match information

        Notes:
        ------
        - The function internally calls `get_season_matches` to fetch all matches for the season.
        - Matches are filtered to include only those where the specified team_id appears as either team_id_1 or team_id_2.

        Raises:
        -------
        ValueError: If the season or team_id is invalid or not found in the data.
    """

        season_matches = self.get_season_matches(season=season)

        team_id = str(team_id)
        team_season_matches = season_matches[(season_matches['team_id_1'] == team_id) | (season_matches['team_id_2'] == team_id)]

        return team_season_matches


    def build_team_roster(self, team_id, season):
        """
        Build a roster for a specific team in a given season.

        This function aggregates player data across all matches for the specified team and season,
        creating a comprehensive roster with various statistics for each player.

        Parameters:
        -----------
        team_id : int
            The unique identifier for the team.
        season : int
            The season number for which to build the roster.

        Returns:
        --------
        pandas.DataFrame
            A DataFrame containing the team roster with the following columns:
            - Player ID: Unique identifier for the player
            - Name: Player's name
            - Jersey Number: Player's jersey number
            - Captain Count: Number of times the player was captain
            - Played Count: Number of matches played
            - Green Card Count: Number of green cards received
            - Yellow Card Count: Number of yellow cards received
            - Red Card Count: Number of red cards received
            - Starter Count: Number of times the player started a match
            - Top Raider Count: Number of times the player was top raider
            - Top Defender Count: Number of times the player was top defender
            - Total Points: Total points scored by the player
            - Team ID: The team's unique identifier
            - Team Name: The team's name
            - Total Matches in Season: Total number of matches played by the team in the season

        Notes:
        ------
        - The function reads match data from JSON files in the './MatchData_pbp' directory.
        - If no data is found for the specified season, an empty DataFrame is returned.
        - The function aggregates data across all matches, updating player statistics cumulatively.

        Raises:
        -------
        FileNotFoundError: If the directory for the specified season is not found.
        JSONDecodeError: If there's an issue parsing the JSON files.
        """
    # ... (rest of the function implementation remains the same)
        
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
        """
        Retrieve comprehensive player information for a specific season.

        This function aggregates data from multiple sources to provide a detailed
        overview of a player's performance in a given season.

        Parameters:
        -----------
        player_id : int
            The unique identifier for the player.
        season : int, optional
            The season number for which to retrieve data. If not specified,
            the latest season available in the data will be used.

        Returns:
        --------
        tuple
            A tuple containing four pandas DataFrames:
            1. player_stats_df_rank (DataFrame): Player's ranking statistics.
            2. player_stats_df_value (DataFrame): Player's value statistics.
            3. player_stats_df_per_match (DataFrame): Player's per-match statistics.
            4. rvd_extracted_df (DataFrame): Raider vs. Defender statistics.

        Each DataFrame is transposed (T) for easier reading.

        Notes:
        ------
        - The function aggregates data from various CSV files containing player statistics,
        raider vs. defender data, defender success rates, raider success rates, and lineup information.
        - If data is not available for the specified player or season in any of the source files,
        appropriate warning messages will be printed.
        - The function handles data type conversions and missing value imputations to ensure
        consistent processing across different data sources.

        Raises:
        -------
        FileNotFoundError: If any of the required data files are not found.
        ValueError: If there are issues with data type conversions.
        """

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


    def get_detailed_player_info(self, player_id, season):
        """
        Extract detailed player statistics from all matches in a given season.

        Args:
        player_id (int): The ID of the player.
        season (int): The season number.

        Returns:
        pandas.DataFrame: A DataFrame containing detailed player statistics for each match.
        """
        player_id = int(player_id)
        season = int(season)
        
        base_path = "./MatchData_pbp"
        season_folder = next((folder for folder in os.listdir(base_path) if f"Season_{season}" in folder), None)
        if not season_folder:
            print(f"No data found for season {season}")
            return pd.DataFrame()

        season_path = os.path.join(base_path, season_folder)
        # print(f"Processing data from: {season_path}")
        
        player_stats = []
        
        for filename in os.listdir(season_path):
            if filename.endswith(".json"):
                file_path = os.path.join(season_path, filename)
                
                try:
                    with open(file_path, 'r') as file:
                        match_data = json.load(file)
                    
                    # Handle different JSON structures
                    if "gameData" in match_data:
                        match_data = match_data["gameData"]
                    
                    match_id = match_data["match_detail"]["match_id"]
                    match_date = match_data["match_detail"]["date"]
                    
                    for team in match_data["teams"]["team"]:
                        for player in team["squad"]:
                            if int(player["id"]) == player_id:
                                try:
                                    opponent_team = next(t for t in match_data["teams"]["team"] if t["id"] != team["id"])
                                except StopIteration:
                                    print(f"Warning: Could not find opponent team in match {match_id}")
                                    continue

                                player_match_stats = {
                                    "match_id": match_id,
                                    "date": match_date,
                                    "team_name": team["name"],
                                    "team_score": team["score"],
                                    "opponent_name": opponent_team["name"],
                                    "opponent_score": opponent_team["score"],
                                    "played": player.get("played", False),
                                    "starter": player.get("starter", False),
                                    "on_court": player.get("on_court", False),
                                    "captain": player.get("captain", False),
                                    "total_points": player["points"]["total"],
                                    "raid_points": player["points"]["raid_points"]["total"],
                                    "tackle_points": player["points"]["tackle_points"]["total"],
                                    "raids_total": player["raids"]["total"],
                                    "raids_successful": player["raids"]["successful"],
                                    "raids_unsuccessful": player["raids"].get("unsuccessful", 0),
                                    "raids_empty": player["raids"].get("Empty", 0),
                                    "super_raids": player["raids"].get("super_raids", 0),
                                    "tackles_total": player["tackles"]["total"],
                                    "tackles_successful": player["tackles"]["successful"],
                                    "tackles_unsuccessful": player["tackles"].get("unsuccessful", 0),
                                    "super_tackles": player["tackles"].get("super_tackles", 0),
                                    "green_card_count": player.get("green_card_count", 0),
                                    "yellow_card_count": player.get("yellow_card_count", 0),
                                    "red_card_count": player.get("red_card_count", 0),
                                    "top_raider": player.get("top_raider", False),
                                    "top_defender": player.get("top_defender", False),
                                }
                                
                                # Extract substitution data
                                substitutions = player.get("substitute", [])
                                player_match_stats["substitutions"] = len(substitutions)
                                if substitutions:
                                    player_match_stats["first_substitution_time"] = substitutions[0].get("substitute_time")
                                
                                player_stats.append(player_match_stats)
                                break
                except Exception as e:
                    print(f"Error processing file {file_path}: {str(e)}")
        
        df = pd.DataFrame(player_stats)

        
        # Calculate additional statistics
        if not df.empty:
            df["matches_played"] = len(df)
            df["matches_started"] = df["starter"].sum()
            df["average_points_full_season"] = df["total_points"].mean()
            df["total_substitutions_full_season"] = df["substitutions"].sum()
        else:
            print(f"No data found for player {player_id} in season {season}")

        # if sort_date_asc:
        #     df = df.sort_values(['date'], ascending=True)
        # elif not sort_date_asc:
        #     df = df.sort_values(['date'], ascending=False)
        
        return df


    def load_match_details(self, season, match_id) -> Tuple[DataFrame, DataFrame, DataFrame, DataFrame, DataFrame, DataFrame]:
        """
        Load and process match details for a specific season and match ID.

        This function retrieves the match data from a JSON file, processes it, and returns
        various aspects of the match as separate DataFrames.

        Args:
            season (int): The season number.
            match_id (str): The unique identifier for the match.

        Returns:
            Tuple[DataFrame, DataFrame, DataFrame, DataFrame, DataFrame, DataFrame]: A tuple containing:
                - match_detail_df: DataFrame with overall match details.
                - events_df: DataFrame with all events that occurred during the match.
                - zones_df: DataFrame with information about different zones on the court.
                - team1_df: DataFrame with detailed information about the first team.
                - team2_df: DataFrame with detailed information about the second team.
                - breakdown_df: DataFrame with breakdown data of the game.

        Raises:
            ValueError: If no season data is found or if data for exactly two teams is not present.
            FileNotFoundError: If no match file is found for the given season and match ID.

        Note:
            If an error occurs during data loading or processing, the function will print an error
            message and return None for all DataFrames.
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
                # print(f"Processing file: {file_path}")
                temp = json.load(file)
                # print(f"File loaded successfully: {file_path}")
                temp2 = temp.copy()

            # Check if the data is nested under 'gameData'
            if 'gameData' in temp:
                temp = temp['gameData']

            match_detail = temp.get("match_detail", {})
            flattened_match_detail = self.internal_flatten_match_detail(match_detail)
            match_detail_df = pd.DataFrame([flattened_match_detail])

            match_detail_df = match_detail_df.drop(columns=["series_short_name", "series_parent_series_id", "status_id", "series_name", "result_outcome"])

            teams_data = temp.get("teams", {}).get("team", [])

            if len(teams_data) != 2:
                raise ValueError("Expected data for exactly two teams")

            team1_df, team2_df = self.internal_process_team_data(teams_data)
            
            events_df = pd.DataFrame(temp.get("events", {}).get("event", []))
            zones_df = pd.DataFrame(temp.get("zones", {}).get("zone", []))

            

            


            breakdown_data = temp2.get("breakdownData", {})
            # print(f"Breakdown data: {breakdown_data}")

            # print(breakdown_data)

            if season == 4 or not breakdown_data:
                breakdown_df = pd.DataFrame()
            
            else:
                
                teams_data = temp2.get("gameData", "").get("teams", "").get("team", "")
                # print(f"Teams data: {teams_data}")
                # print(teams_data[:100])

                team_name=[]
                for t in teams_data:
                    # print(f"Team Name: {t.get('name', '')}, Team ID: {t.get('id', '')}")
                    team_name.append((t.get("name", ""), t.get("id", "")))
                
                # print(team_name)
                
                breakdown_list = []
                # print("hi")
                for team_id, team_data in breakdown_data.items():
                    
                    # print(f"Team ID: {team_id}, Team Data: {team_data}")
                    # print("hi2")
                    # print("hi3")
                    # print(int(team_name[0][1]))
                    # print(int(team_id))

                    if int(team_id) == int(team_name[0][1]):
                        # print("hi4")
                        # print(f"Team Name: {team_name[0][0]}")
                        team_name_json = team_name[0][0]
                        # print(team_name_json)
                        # print(f"Team Name: {team_name}")
                    else:
                        team_name_json = team_name[1][0]
                        # print(team_name_json)
                    
                    # print(f"\n---\n-\n\nnn\Team Name: {team_name}")
                    team_breakdown = {
                        'team_id': team_id,
                        'team_name': team_name_json,
                        'raids_total': team_data['raids']['total'],
                        'raids_successful': team_data['raids']['successful'],
                        'raids_unsuccessful': team_data['raids']['unsuccessful'],
                        'raids_empty': team_data['raids']['Empty'],
                        'tackles_total': team_data['tackles']['total'],
                        'tackles_successful': team_data['tackles']['successful'],
                        'tackles_unsuccessful': team_data['tackles']['unsuccessful'],
                        'points_total': team_data['points']['total'],
                        'points_raid': team_data['points']['raid_points']['total'],
                        'points_tackle': team_data['points']['tackle_points']['total'],
                        'points_all_out': team_data['points']['all_out'],
                        'points_extras': team_data['points']['extras'],
                        'raid_success_rate': team_data.get('raid_success_rate', None),
                        'tackle_success_rate': team_data.get('tackle_success_rate', None),
                        'longest_streak': team_data.get('longest_streak', None),
                        'streak_percent': team_data.get('streak_percent', None),
                    }
                    breakdown_list.append(team_breakdown)
                breakdown_df = pd.DataFrame(breakdown_list)

            return match_detail_df, events_df, zones_df, team1_df, team2_df, breakdown_df

        except Exception as e:
            print(f"Error loading data from {file_path}: {str(e)}")
            return None, None, None, None, None, None


    def internal_process_team_data(self, teams_data: List[Dict[str, Any]]) -> Tuple[DataFrame, DataFrame]:
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

        team_dfs = []
        for team_data in teams_data:
            squad_df = pd.DataFrame(process_squad(team_data.get('squad', [])))
            team_df = pd.DataFrame({
                'team_id': [team_data['id']],
                'team_name': [team_data['name']],
                'team_score': [team_data['score']],
            })
            team_df = pd.concat([team_df, squad_df], axis=1)
            team_dfs.append(team_df)

        return tuple(team_dfs)

    
    def load_pbp(self, season, match_id) -> DataFrame:
        """
        Load the play-by-play (PBP) data for a specific match in a given season.

        This function calls the load_match_details method and extracts the events DataFrame,
        which contains the play-by-play data for the specified match.

        Args:
            season (int): The season number.
            match_id (str): The unique identifier for the match.

        Returns:
            DataFrame: A DataFrame containing the play-by-play events of the match.
                       Returns None if there was an error loading the match details.

        Note:
            This function relies on the load_match_details method to retrieve the full match data.
            It only returns the events DataFrame, discarding other match information.
        """
        _, _, events_df, _, _, _ = self.load_match_details(season, match_id)
        return events_df


    def internal_flatten_match_detail(self, match_detail: Dict[str, Any]) -> Dict[str, Any]:
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



if __name__ == "__main__":
    
    
    api = KabaddiDataAPI()




    # print("Testing get_detailed_player_info".center(100, "-"))
    # player_id = 94
    # season = 6
    
    # detailed_info = api.get_detailed_player_info(player_id, season)

    # print(detailed_info)
    # detailed_info.to_csv("detailed_info.csv")
    
    # if detailed_info is not None and not detailed_info.empty:
    #     print(f"Detailed info for player {player_id} in season {season}:")
    #     print(detailed_info)
        
    #     print("\nSummary statistics:")
    #     print(f"Matches played: {detailed_info['matches_played'].iloc[0]}")
    #     print(f"Matches started: {detailed_info['matches_started'].iloc[0]}")
    #     print(f"Average points: {detailed_info['average_points'].iloc[0]:.2f}")
    #     print(f"Total substitutions: {detailed_info['total_substitutions'].iloc[0]}")
        
    #     print("\nFirst few rows of detailed match data:")
    #     print(detailed_info.head())
    # else:
    #     print(f"No data found for player {player_id} in season {season}")

    # match_detail_df, events_df, zones_df, team1_df, team2_df, breakdown_df = api.load_match_details(season=10, match_id='3125')

    # print("Match Detail Data:")
    # print(match_detail_df.T)

    # print("\n\nEvents Data:")
    # print(events_df)

    # print("\n\nZones Data:")
    # print(zones_df)

    # print("\n\nTeam 1 Data:")
    # print(team1_df.T)

    # print("\n\nTeam 2 Data:")
    # print(team2_df.T)

    # print("\n\nBreakdown Data:")
    # print(breakdown_df.T)




    # # ACTUAL TESTING ------------------------------------------------------------------------

    # print("1. Testing get_pkl_standings".center(150,"-"))
    # qualified_df, all_standings_df = api.get_pkl_standings(season=9, qualified=True)
    # print("Qualified teams:")
    # print(qualified_df)
    # print("\nAll standings:")
    # print(all_standings_df)

    # print("\n2. Testing get_season_matches".center(150,"-"))
    # season_matches = api.get_season_matches(season=6)
    # print(season_matches.head())

    # print("\n3. Testing get_team_info".center(150,"-"))
    # df_rank, df_value, df_per_match, filtered_team_raider_skills, filtered_team_defender_skills = api.get_team_info(season=6, team_id=29)
    # print("Team Rank:")
    # print(df_rank)
    # print("\nTeam Value:")
    # print(df_value)
    # print("\nTeam Per Match:")
    # print(df_per_match)
    # print("\nTeam Raider Skills:")
    # print(filtered_team_raider_skills)
    # print("\nTeam Defender Skills:")
    # print(filtered_team_defender_skills)

    team_ids = api.get_team_ids(season=5)
    print("Team-IDs")
    print(team_ids)

    # print("\n4. Testing get_team_matches".center(150,"-"))
    # team_matches = api.get_team_matches(season=9, team_id=3)
    # print(team_matches.head())

    # print("\n5. Testing build_team_roster".center(150,"-"))
    # team_roster = api.build_team_roster(season=9, team_id=3)
    # print(team_roster)

    # print("\n6. Testing get_player_info".center(150,"-"))
    # player_stats_df_rank, player_stats_df_value, player_stats_df_per_match, rvd_extracted_df = api.get_player_info(player_id=660, season=9)
    # print("Player Rank:")
    # print(player_stats_df_rank)
    # print("\nPlayer Value:")
    # print(player_stats_df_value)
    # print("\nPlayer Per Match:")
    # print(player_stats_df_per_match)
    # print("\nPlayer RVD:")
    # print(rvd_extracted_df)

    # print("\n7. Testing load_match_details".center(150,"-"))
    # match_detail_df, events_df, zones_df, team1_df, team2_df, breakdown_df = api.load_match_details(season=9, match_id='2895')
    # print("Match Detail:")
    # print(match_detail_df)
    # print("\nEvents (first 5 rows):")
    # if not events_df:
    #     print("No events data found for this match")
    # else:
    #     print(events_df.head())
    # print("\nZones:")
    # print(zones_df)
    # print("\nTeam 1 (first 5 rows):")
    # if not team1_df:
    #     print("No team 1 data found for this match")
    # else:
    #     print(team1_df.head())
    # print("\nTeam 2 (first 5 rows):")
    # if not team2_df:
    #     print("No team 2 data found for this match")
    # else:
    #     print(team2_df.head())
    # print("\nBreakdown Data:")
    # print(breakdown_df)

    # print("\n8. Testing load_pbp".center(150,"-"))
    # pbp_df = api.load_pbp(season=9, match_id='2895')
    # print("Play-by-Play Data (first 5 rows):")
    # if not pbp_df:
    #     print("No play-by-play data found for this match")
    # else:
    #     print(pbp_df.head())

    # # END OF ACTUAL TESTING ------------------------------------------------------------------------


    # # MY OLD TESTING ------------------------------------------------------------------------
    # print("=="*100)
    # print("=="*100)
    # print("MY OLD TESTING".center(150,"-"))
    # print("=="*100)
    # print("=="*100)

    # # matches = api.get_season_matches(season=10)
    # # result = matches[(matches['League_Stage'] == 'Semi Final')]
    # # print(result)

    # # df = api.load_pbp(season=10, match_id=3164)
    # # # df.to_csv("pbp.csv")
    # # print(df.tail())



    # # print("get standings")
    # # # x = api.get_pkl_standings(season=10)
    # # # print(x)


    # qualified_df , all_standings_df = api.get_pkl_standings(season=9, qualified=True)
    # print("qualified_df")
    # print(qualified_df)
    # print()

    # # print("all_standings_df")
    # # print(all_standings_df)
    # # print(len(all_standings_df))

    # print("season_matches")
    # matches = api.get_season_matches(season=6)
    # print(matches)
    # # print(len(x))


    # # print("-"*100)
    # print("team_info")

    # df_rank_, df_value_, df_per_match_, filtered_team_raider_skills_, filtered_team_defender_skills_ = api.get_team_info(season=6,team_id=29)

    # print("Rank DFs")
    # print(df_rank_)
    # print("-"*100)
    # print("Value DFs")
    # print(df_value_)
    # print("-"*100)
    # print("Per Match DFs")
    # print(df_per_match_)
    # print("-"*100)
    # print("Raider Skills")
    # print(filtered_team_raider_skills_)
    # print("-"*100)
    # print("Defender Skills")
    # print(filtered_team_defender_skills_)

    # #TODO: Fix the order of the columns in the output
    # # team-successful-tackle-percent_value
    # # team-super-tackles_value
    # # team-tackle-points_value
    # # team-successful-tackles-per-match_value
    # # team-average-tackle-points_value
    # # team-successful-tackles_value
    # # Total_touch_points_value
    # # Total_bonus_points_value
    # # team-raid-points_value
    # # team-average-raid-points_value
    # # team-successful-raids_value
    # # team-super-raid_value
    # # team-raid_value
    # # team-successful-raid-percent_value
    # # team-dod-raid-points_value
    # # team-total-points_value
    # # team-all-outs-conceded_value
    # # team-all-outs-inflicted_value
    # # team-avg-points-scored_value
    # # team-total-points-conceded_value


    # print("get_team_matches\n\n")

    # df = api.get_team_matches(season=9, team_id=3)
    # print(df)



    # print("build build_team_roster")

    # df = api.build_team_roster(season=9, team_id='3')
    # print("-"*100)
    # print(df)

    # ## df.to_csv("team_roster.csv")


    # print("build get_player_info")

    # _player_stats_df_rank, _player_stats_df_value, _player_stats_df_per_match, _rvd_extracted_df = api.get_player_info(player_id=660, season=9)
    # print("-"*100)
    # print(_player_stats_df_rank)
    # print("-"*100)
    # print(_player_stats_df_value)
    # print("-"*100)
    # print(_player_stats_df_per_match)
    # print("-"*100)
    # print(_rvd_extracted_df)


    # print("load_match_details-------\n\n\n")
    # _match_detail_df, _events_df, _zones_df, _team1_df, _team2_df, _breakdown_df = api.load_match_details(season='9', match_id='2895')
    # print("-"*100)
    # print(_match_detail_df)
    # print("-"*100)
    # print(_events_df)
    # print("-"*100)
    # print(_zones_df)
    # print("-"*100)
    # print(_team1_df)
    # print("-"*100)
    # print(_team2_df)
    # print("-"*100)
    # print(_breakdown_df)


    # print("load_pbp")
    # _pbp_df = api.load_pbp(season=9, match_id='2895')
    # print("-"*100)
    # print(_pbp_df)























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

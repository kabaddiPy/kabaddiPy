@ -1,281 +1,327 @@
import json
import re
from pathlib import Path
import pandas as pd
import os
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
                        matches_list.extend(self.create_matches_list(team, group_name))

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

    def get_team_info(self, team_id, season='overall'):

        if season != 'overall':
            season = int(season)
        df = pd.read_csv("../prokabaddidata/Team-Wise-Data/PKL_AggregatedTeamStats.csv")

        df2 = pd.read_csv("../prokabaddidata/Team-Wise-Data/ALL_Raider_Skills_Merged.csv")
        df3 = pd.read_csv("../prokabaddidata/Team-Wise-Data/ALL_Defensive_Skills_Merged.csv")
        df['team_id'] = pd.to_numeric(df['team_id'], errors='coerce')
        df['season'] = pd.to_numeric(df['season'], errors='coerce')

        team_id = int(team_id)

        def find_team_column(dataframe, team_id):
            for col in dataframe.columns:
                if f"({team_id})" in col:
                    return col
            return None

        # Find the relevant column names for df2 and df3
        team_column_df2 = find_team_column(df2, team_id)
        team_column_df3 = find_team_column(df3, team_id)

        if season == 'overall':
            all_row = df[(df['team_id'] == team_id) & (df['season'] == 'all')]
            other_rows = df[(df['team_id'] == team_id) & (df['season'] != 'all')]
            filtered_df = pd.concat([all_row, other_rows]).reset_index(drop=True)
            filtered_df2 = None
            filtered_df3 = None
            print("Raider and Defender skills are not available for 'overall' season.")
        else:
            filtered_df = df[(df['team_id'] == team_id) & (df['season'] == season)]

            if team_column_df2:
                filtered_df2 = df2[df2['Season'] == season][
                    [team_column_df2, 'Season'] + [col for col in df2.columns if col != 'Season' and '(' not in col]]
            else:
                filtered_df2 = None
                print(f"No raider skills data found for team_id {team_id}")

            if team_column_df3:
                filtered_df3 = df3[df3['Season'] == season][
                    [team_column_df3, 'Season'] + [col for col in df3.columns if col != 'Season' and '(' not in col]]
            else:
                filtered_df3 = None
                print(f"No defender skills data found for team_id {team_id}")

            if filtered_df2 is not None:
                filtered_df2 = filtered_df2.reset_index(drop=True)
            if filtered_df3 is not None:
                filtered_df3 = filtered_df3.reset_index(drop=True)
        if filtered_df.empty:
            print(f"No data found in CSV for team_id {team_id} in season {season}")
            return None, None, None, None, None
        if season == 'overall':
            standings_df, matches_df = self.get_pkl_standings(season=10, team_id=team_id, matches=True)
        else:
            standings_df, matches_df = self.get_pkl_standings(season, team_id=team_id, matches=True)
        standings_df = None
        matches_df = None
            return None, None, None
        # if season == 'overall':
        #     standings_df, matches_df = self.get_pkl_standings(season=10, team_id=team_id, matches=True)
        # else:
        #     standings_df, matches_df = self.get_pkl_standings(season, team_id=team_id, matches=True)
        if filtered_df2.empty:
            print(f"No data for raider skills for team_id {team_id} in season {season}")
        if filtered_df3.empty:
            print(f"No data for defender skills for team_id {team_id} in season {season}")
        # Separate the columns based on the suffixes
        rank_columns = [col for col in filtered_df.columns if col.endswith('_rank')]
        value_columns = [col for col in filtered_df.columns if col.endswith('_value')]
        per_match_columns = [col for col in filtered_df.columns if col.endswith('_per-match')]

        df_rank = filtered_df[['season', 'team_id', 'team_name'] + rank_columns]
        df_value = filtered_df[['season', 'team_id', 'team_name'] + value_columns]
        df_per_match = filtered_df[['season', 'team_id', 'team_name'] + per_match_columns]

        return df_rank, df_value, df_per_match, standings_df, matches_df
        return df_rank, df_value, df_per_match, filtered_df2, filtered_df3


def extract_number(season_string):
    match = re.search(r'\d+', season_string)
    return int(match.group()) if match else None


# Usage example
if __name__ == "__main__":
    api = KabaddiDataAPI()
    df_rank, df_value, df_per_match, df2, df3 = api.get_team_info(team_id='4',season='5')
    print(df_rank)


    # match_id = "183"
    # season = "Pro Kabaddi League Season 4, 2016"
    #
    # general_df, participants_df = api.get_match_overview(match_id, season)
    # print(general_df)
    df_rank, df_value, df_per_match, df2, df3 = api.get_team_info(team_id='4',season='7')
    print(df2)
    # x = api.get_pkl_standings(season=6, qualified=False)
    # print(x)
    # # print("-"*100)
    # # print(y)
    #
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

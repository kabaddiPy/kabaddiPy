import os
import json
from typing import List, Dict, Any, Optional, Tuple
from collections import defaultdict
from datetime import datetime
import pandas as pd
from pandas import DataFrame


class KabaddiDataAPI:
    def __init__(self, base_path: str):
        self.base_path = base_path

    def internal_match_data(self, season: str, match_id: str) -> pd.DataFrame:
        """
        Get the full data for a specific match.

        Args:
            season (str): The season year.
            match_id (str): The match ID.

        Returns:
            Dict[str, Any]: The match data as a dictionary.
        """

        file_path = os.path.join(self.base_path, "Match_Data", season, f"{match_id}.json")
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except:
            print(f"Could not load {file_path}")

    def internal_sort_pkl_match(self):
        season_match_id = api.get_matches_for_season('2019')
        print(season_match_id)
        not_pkl = []
        for j in season_match_id:
            df1, df2, df3, df4 = api.get_match_data("2019", f'{j}')
            if 'Pro Kabaddi League' not in df1['series'][0]['name']:
                print(df1['series'][0]['name'])
                not_pkl.append(f'{j}')
        # not_pkl.sort()
        print(not_pkl)

    def get_match_data(self, season: str, match_id: str) -> tuple[DataFrame, DataFrame, DataFrame, DataFrame]:
        """
        Get the full data for a specific match.

        Args:
            season (str): The season year.
            match_id (str): The match ID.

        Returns:
            Dict[str, Any]: The match data as a dictionary.
        """
        file_path = os.path.join(self.base_path, "Match_Data", season, f"{match_id}.json")
        try:
            with open(file_path, 'r') as file:
                temp = json.load(file)
            match_detail_df = pd.DataFrame([temp.get("match_detail", {})])
            teams_df = pd.DataFrame(temp.get("teams", {}).get("team", []))
            events_df = pd.DataFrame(temp.get("events", {}).get("event", []))
            zones_df = pd.DataFrame(temp.get("zones", {}).get("zone", []))

            return match_detail_df, teams_df, events_df, zones_df
        except:
            print(f"Could not load {file_path}")

    def get_match_events(self, season: str, match_id: str) -> List[Dict[str, Any]]:
        """
        Get all events for a specific match.

        Args:
            season (str): The season year.
            match_id (str): The match ID.

        Returns:
            List[Dict[str, Any]]: A list of all events in the match.
        """
        match_data = self.internal_match_data(season, match_id)
        data = match_data['events']['event']
        df = pd.DataFrame(data)  # .T transposes the DataFrame
        return df

    def get_raid_events(self, season: str, match_id: str) -> List[Dict[str, Any]]:
        """
        Get all raid events for a specific match.

        Args:
            season (str): The season year.
            match_id (str): The match ID.

        Returns:
            List[Dict[str, Any]]: A list of all raid events in the match.
        """
        events = self.get_match_events(season, match_id)
        return [event for event in events if event[event] in ['Successful Raid', 'Unsuccessful Raid', 'Empty Raid']]

    def get_player_raid_stats(self, season: str, match_id: str, raider_id: int) -> Dict[str, Any]:
        """
        Get raid statistics for a specific player in a match.

        Args:
            season (str): The season year.
            match_id (str): The match ID.
            raider_id (int): The ID of the raider.

        Returns:
            Dict[str, Any]: A dictionary containing the player's raid statistics.
        """
        raid_events = self.get_raid_events(season, match_id)
        player_raids = [event for event in raid_events if event['raider_id'] == raider_id]

        stats = {
            'total_raids': len(player_raids),
            'successful_raids': sum(1 for raid in player_raids if raid['event'] == 'Successful Raid'),
            'unsuccessful_raids': sum(1 for raid in player_raids if raid['event'] == 'Unsuccessful Raid'),
            'empty_raids': sum(1 for raid in player_raids if raid['event'] == 'Empty Raid'),
            'total_points': sum(raid['raid_points'] for raid in player_raids)
        }
        return stats

    def get_team_raid_stats(self, season: str, match_id: str, team_id: int) -> Dict[str, Any]:
        """
        Get raid statistics for a specific team in a match.

        Args:
            season (str): The season year.
            match_id (str): The match ID.
            team_id (int): The ID of the team.

        Returns:
            Dict[str, Any]: A dictionary containing the team's raid statistics.
        """
        raid_events = self.get_raid_events(season, match_id)
        team_raids = [event for event in raid_events if event['raiding_team_id'] == team_id]

        stats = {
            'total_raids': len(team_raids),
            'successful_raids': sum(1 for raid in team_raids if raid['event'] == 'Successful Raid'),
            'unsuccessful_raids': sum(1 for raid in team_raids if raid['event'] == 'Unsuccessful Raid'),
            'empty_raids': sum(1 for raid in team_raids if raid['event'] == 'Empty Raid'),
            'total_points': sum(raid['raid_points'] for raid in team_raids)
        }
        return stats

    def get_score_progression(self, season: str, match_id: str) -> List[Dict[str, Any]]:
        """
        Get the score progression throughout the match.

        Args:
            season (str): The season year.
            match_id (str): The match ID.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing the score after each event.
        """
        events = self.get_match_events(season, match_id)
        score_progression = []
        for event in events:
            score_progression.append({
                'event_no': event['event_no'],
                'clock': event['clock'],
                'score': event['score']
            })
        return score_progression

    def get_player_performance(self, season: str, match_id: str, player_id: int) -> Dict[str, Any]:
        """
        Get comprehensive performance statistics for a specific player in a match.

        Args:
            season (str): The season year.
            match_id (str): The match ID.
            player_id (int): The ID of the player.

        Returns:
            Dict[str, Any]: A dictionary containing the player's performance statistics.
        """
        events = self.get_match_events(season, match_id)
        player_events = [event for event in events if
                         event['raider_id'] == player_id or event['defender_id'] == player_id]

        performance = {
            'raid_points': sum(event['raid_points'] for event in player_events if event['raider_id'] == player_id),
            'defense_points': sum(
                event['defending_points'] for event in player_events if event['defender_id'] == player_id),
            'total_points': 0,
            'successful_raids': sum(1 for event in player_events if
                                    event['raider_id'] == player_id and event['event'] == 'Successful Raid'),
            'successful_tackles': sum(1 for event in player_events if
                                      event['defender_id'] == player_id and event['event'] == 'Successful Tackle')
        }
        performance['total_points'] = performance['raid_points'] + performance['defense_points']
        return performance

    def get_match_summary(self, season: str, match_id: str) -> Dict[str, Any]:
        """
        Get a comprehensive summary of a match including team performances and key events.

        Args:
            season (str): The season year.
            match_id (str): The match ID.

        Returns:
            Dict[str, Any]: A dictionary containing the match summary.
        """
        match_data = self.internal_match_data(season, match_id)
        if match_data is None:
            print(f"No match data for {match_id}. Check season or match id!")
            return None

        events = match_data['events']['event']

        summary = {
            'match_id': match_id,
            'season': season,
            'teams': match_data['teams'],
            'final_score': events[-1]['score'],
            'total_events': len(events),
            'team_stats': {},
            'key_events': []
        }

        for team_id in [1, 2]:  # Assuming team IDs are 1 and 2
            summary['team_stats'][team_id] = self.get_team_raid_stats(season, match_id, team_id)

        # Identify key events (e.g., Super Raids, All Outs)
        for event in events:
            if event['event'] in ['Super Raid', 'All Out']:
                summary['key_events'].append({
                    'event_no': event['event_no'],
                    'event': event['event'],
                    'clock': event['clock'],
                    'score': event['score']
                })

        return summary

    def get_available_seasons(self) -> List[str]:
        """
        Get a list of available seasons (years) in the dataset.

        Returns:
            List[str]: A list of season years.
        """
        return [folder for folder in os.listdir(os.path.join(self.base_path, "Match_Data"))
                if os.path.isdir(os.path.join(self.base_path, "Match_Data", folder))]

    def get_matches_for_season(self, season: str) -> List[str]:
        """
        Get a list of match IDs for a specific season.

        Args:
            season (str): The season year.

        Returns:
            List[str]: A list of match IDs.
        """
        season_path = os.path.join(self.base_path, "Match_Data", season)
        return [file.split('.')[0] for file in os.listdir(season_path) if file.endswith('.json')]


    def get_team_names(self, season: str, match_id: str) -> List[str]:
        """
        Get the names of the two teams playing in a specific match.

        Args:
            season (str): The season year.
            match_id (str): The match ID.

        Returns:
            List[str]: A list containing the names of the two teams.
        """
        match_data = self.internal_match_data(season, match_id)
        return [match_data['team1'], match_data['team2']]

    def get_match_result(self, season: str, match_id: str) -> Dict[str, Any]:
        """
        Get the result of a specific match.

        Args:
            season (str): The season year.
            match_id (str): The match ID.

        Returns:
            Dict[str, Any]: A dictionary containing the match result information.
        """
        match_data = self.internal_match_data(season, match_id)
        return {
            "winner": match_data['winner'],
            "score": match_data['score'],
            "margin": match_data['margin']
        }

    def get_player_stats(self, season: str, match_id: str, player_name: str) -> Optional[Dict[str, Any]]:
        """
        Get the statistics for a specific player in a match.

        Args:
            season (str): The season year.
            match_id (str): The match ID.
            player_name (str): The name of the player.

        Returns:
            Optional[Dict[str, Any]]: A dictionary containing the player's statistics, or None if not found.
        """
        match_data = self.internal_match_data(season, match_id)
        for team in ['team1_players', 'team2_players']:
            for player in match_data[team]:
                if player['name'] == player_name:
                    return player
        return None

    def get_top_raiders(self, season: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Get the top raiders for a specific season.

        Args:
            season (str): The season year.
            limit (int): The number of top raiders to return. Default is 5.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing top raiders' information.
        """
        raiders = []
        for match_id in self.get_matches_for_season(season):
            match_data = self.internal_match_data(season, match_id)
            for team in ['team1_players', 'team2_players']:
                for player in match_data[team]:
                    if player['role'] == 'raider':
                        raiders.append({
                            'name': player['name'],
                            'raid_points': player['raid_points']
                        })

        return sorted(raiders, key=lambda x: x['raid_points'], reverse=True)[:limit]

    def get_team_performance(self, season: str, team_name: str) -> Dict[str, Any]:
        """
        Get the overall performance of a team in a specific season.

        Args:
            season (str): The season year.
            team_name (str): The name of the team.

        Returns:
            Dict[str, Any]: A dictionary containing the team's performance statistics.
        """
        performance = {
            'matches_played': 0,
            'wins': 0,
            'losses': 0,
            'ties': 0,
            'total_points': 0
        }

        for match_id in self.get_matches_for_season(season):
            match_data = self.internal_match_data(season, match_id)
            if team_name in [match_data['teams']['team'][0], match_data['teams']['team'][1]]:
                performance['matches_played'] += 1
                if match_data['winner'] == team_name:
                    performance['wins'] += 1
                elif match_data['winner'] == 'Tie':
                    performance['ties'] += 1
                else:
                    performance['losses'] += 1

                team_index = '1' if match_data['team1'] == team_name else '2'
                performance['total_points'] += int(match_data['score'].split('-')[int(team_index) - 1])

        return performance


    def search_matches_by_date(self, date: datetime) -> List[Dict[str, Any]]:
        """
        Search for matches played on a specific date across all seasons.

        Args:
            date (datetime): The date to search for.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing match information.
        """
        matches = []
        for season in self.get_available_seasons():
            for match_id in self.get_matches_for_season(season):
                match_data = self.internal_match_data(season, match_id)
                print(match_data)
                match_date = datetime.strptime(match_data['match_detail']['date'], '%Y-%m-%d')
                if match_date.date() == date.date():
                    matches.append({
                        'season': season,
                        'match_id': match_id,
                        'team1': match_data['team1'],
                        'team2': match_data['team2'],
                        'winner': match_data['winner'],
                        'score': match_data['score']
                    })
        return matches

# Example usage:
api = KabaddiDataAPI(r"../1_DATA/DATA__kaggle_match")

# match_events = 
seasons = api.get_available_seasons()
print(seasons)
matches = api.get_matches_for_season("2019")
#print(matches)


# Func1
match_detail_df, teams_df, events_df , zones_df = api.get_match_data('2019','1690')
print(events_df)
# Func2
# events_df = api.get_match_events('2019', '1690')

# # Func3
# season_match_id = api.get_matches_for_season('2019')
#
# nums = []
#
# for i in season_match_id:
#     # print(i)
#     match_detail_df, teams_df, events_df , zones_df = api.get_match_data('2019',i)
#     if match_detail_df['match_number'][0] == 'Final':
#         matches_nums = match_detail_df['match_number'][0]
#     else:
#         matches_nums = match_detail_df['match_number'][0].split(" ")[1]
#         nums.append((int(matches_nums), i))
#     # print(matches_nums)
#
# nums.sort()
# print(nums)
#
# print(season_match_id)


    


# print(df1['series'])
# player_performance = api.get_player_performance('2019', '1761', 182)
# print(player_performance)
# temp = api.search_matches_by_date('2019-09-06')
# print(temp)
# score_progression = api.get_score_progression('2022', '123456')
# x= datetime(2019,5,17) # Example date: August 24, 2023
# temp = api.search_matches_by_date(x)
# print(temp)
#t = api.get_match_timeline("2019","761")
# print(api.get_team_performance("2019", "Patna Pirates"))
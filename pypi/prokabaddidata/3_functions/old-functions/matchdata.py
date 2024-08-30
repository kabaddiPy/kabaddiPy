import pandas as pd
from typing import List, Dict, Union, Optional
from datetime import datetime


class KabaddiMatchAnalyzer:
    
    def __init__(self, csv_file_path: str):
        self.df = pd.read_csv(csv_file_path)

        # Custom date parsing function
        def parse_date(date_string):
            try:
                return pd.to_datetime(date_string, format='%Y-%m-%d %H:%M%z')
            except ValueError:
                # For dates without time zone information
                try:
                    return pd.to_datetime(date_string, format='%m/%d/%Y %H:%M')
                except ValueError:
                    # If all else fails, return NaT (Not a Time)
                    return pd.NaT

        # Apply the custom date parsing function
        self.df['start_date'] = self.df['start_date'].apply(parse_date)
        self.df['end_date'] = self.df['end_date'].apply(parse_date)

    def get_match_details(self, game_id: int) -> Dict[str, Union[str, int, float]]:
        """
        Get details for a specific match.

        :param game_id: Unique game identifier
        :return: Dictionary containing match details
        """
        match_data = self.df[self.df['game_id'] == game_id]
        if match_data.empty:
            raise ValueError(f"Game ID {game_id} not found")
        return match_data.iloc[0].to_dict()

    def get_team_performance(self, team_name: str) -> Dict[str, Union[int, float]]:
        """
        Get overall performance statistics for a specific team.

        :param team_name: Name of the team
        :return: Dictionary containing team performance stats
        """
        team_matches = self.df[(self.df['team1_name'] == team_name) | (self.df['team2_name'] == team_name)]
        wins = team_matches[team_matches['winner'] == team_name].shape[0]
        total_matches = team_matches.shape[0]

        return {
            'team_name': team_name,
            'total_matches': total_matches,
            'wins': wins,
            'losses': total_matches - wins,
            'win_percentage': round((wins / total_matches) * 100, 2) if total_matches > 0 else 0
        }

    def get_top_players(self, player_type: str, n: int = 5) -> List[Dict[str, Union[str, int, float]]]:
        """
        Get top N players based on their value for a specific player type.

        :param player_type: Type of player (e.g., 'raider', 'defender')
        :param n: Number of top players to return
        :return: List of dictionaries containing player details
        """
        player_columns = [col for col in self.df.columns if col.endswith('_type')]
        player_data = []

        for col in player_columns:
            name_col = col.replace('_type', '_name')
            value_col = col.replace('_type', '_value')
            id_col = col.replace('_type', '_id')

            players = self.df[self.df[col] == player_type][[name_col, id_col, value_col]]
            players = players.groupby([name_col, id_col])[value_col].mean().reset_index()
            players.columns = ['name', 'id', 'avg_value']
            player_data.append(players)

        all_players = pd.concat(player_data).groupby(['name', 'id'])['avg_value'].mean().reset_index()
        top_players = all_players.sort_values('avg_value', ascending=False).head(n)

        return top_players.to_dict('records')

    def get_venue_statistics(self) -> List[Dict[str, Union[str, int, float]]]:
        """
        Get statistics for each venue.

        :return: List of dictionaries containing venue statistics
        """
        venue_stats = self.df.groupby('venue_name').agg({
            'game_id': 'count',
            'team1_score': 'sum',
            'team2_score': 'sum'
        }).reset_index()

        venue_stats.columns = ['venue_name', 'matches_played', 'total_points_scored']
        venue_stats['avg_points_per_match'] = round(venue_stats['total_points_scored'] / venue_stats['matches_played'],
                                                    2)

        return venue_stats.to_dict('records')

    def get_season_timeline(self, season: int) -> List[Dict[str, Union[str, datetime, int]]]:
        """
        Get a timeline of matches for a specific season.

        :param season: Season number
        :return: List of dictionaries containing match timeline details
        """
        season_matches = self.df[self.df['tour_name'].str.contains(f"Season {season}")]
        timeline = season_matches.sort_values('start_date')[
            ['game_id', 'start_date', 'team1_name', 'team2_name', 'winner']]
        return timeline.to_dict('records')

    def get_team_head_to_head(self, team1: str, team2: str) -> Dict[
        str, Union[int, float, List[Dict[str, Union[str, int]]]]]:
        """
        Get head-to-head statistics for two teams.

        :param team1: Name of the first team
        :param team2: Name of the second team
        :return: Dictionary containing head-to-head statistics
        """
        matches = self.df[((self.df['team1_name'] == team1) & (self.df['team2_name'] == team2)) |
                          ((self.df['team1_name'] == team2) & (self.df['team2_name'] == team1))]

        team1_wins = matches[matches['winner'] == team1].shape[0]
        team2_wins = matches[matches['winner'] == team2].shape[0]
        draws = matches[matches['result_code'] == 'Tied'].shape[0]

        recent_matches = matches.sort_values('start_date', ascending=False).head(5)
        recent_results = recent_matches.apply(lambda row: {
            'date': row['start_date'].strftime('%Y-%m-%d') if pd.notnull(row['start_date']) else 'Unknown',
            'winner': row['winner'],
            'score': f"{row['team1_score']}-{row['team2_score']}"
        }, axis=1).tolist()

        return {
            'total_matches': matches.shape[0],
            f'{team1}_wins': team1_wins,
            f'{team2}_wins': team2_wins,
            'draws': draws,
            'recent_matches': recent_results
        }

    def get_player_performance(self, player_name: str) -> Dict[
        str, Union[str, int, float, List[Dict[str, Union[str, int, float]]]]]:
        """
        Get performance statistics for a specific player.

        :param player_name: Name of the player
        :return: Dictionary containing player performance statistics
        """
        player_columns = [col for col in self.df.columns if col.endswith('_name')]
        player_matches = self.df[self.df[player_columns].eq(player_name).any(axis=1)]

        total_matches = player_matches.shape[0]
        player_type = player_matches[player_matches[player_columns].eq(player_name).any(axis=1)].iloc[0][
            player_columns[player_matches[player_columns].eq(player_name).any(axis=1)].str.replace('_name',
                                                                                                   '_type')].values[0]

        value_column = player_columns[player_matches[player_columns].eq(player_name).any(axis=1)].str.replace('_name',
                                                                                                              '_value')
        total_value = player_matches[value_column].sum().values[0]

        performance_by_match = player_matches.apply(lambda row: {
            'game_id': row['game_id'],
            'date': row['start_date'].strftime('%Y-%m-%d') if pd.notnull(row['start_date']) else 'Unknown',
            'value': row[value_column].values[0],
            'team': row['team1_name'] if player_name in row[
                ['team1_player1_name', 'team1_player2_name', 'team1_player3_name', 'team1_player4_name',
                 'team1_player5_name']].values else row['team2_name']
        }, axis=1).tolist()

        return {
            'player_name': player_name,
            'player_type': player_type,
            'total_matches': total_matches,
            'total_value': total_value,
            'average_value': round(total_value / total_matches, 2) if total_matches > 0 else 0,
            'performance_by_match': performance_by_match
        }

    def get_season_summary(self, season: int) -> Dict[str, Union[str, int, float, Dict[str, Union[str, int, float]]]]:
        """
        Get a summary of a specific season.

        :param season: Season number
        :return: Dictionary containing season summary statistics
        """
        season_matches = self.df[self.df['tour_name'].str.contains(f"Season {season}")]

        total_matches = season_matches.shape[0]
        total_points = season_matches['team1_score'].sum() + season_matches['team2_score'].sum()

        top_scorer = season_matches.loc[season_matches['team1_score'].idxmax()]
        top_score = max(season_matches['team1_score'].max(), season_matches['team2_score'].max())

        winners = season_matches['winner'].value_counts()
        champion = winners.index[0] if not winners.empty else "Unknown"

        return {
            'season': season,
            'total_matches': total_matches,
            'total_points': int(total_points),
            'avg_points_per_match': round(total_points / total_matches, 2) if total_matches > 0 else 0,
            'top_score': {
                'team': top_scorer['team1_name'] if top_scorer['team1_score'] == top_score else top_scorer[
                    'team2_name'],
                'score': int(top_score),
                'opponent': top_scorer['team2_name'] if top_scorer['team1_score'] == top_score else top_scorer[
                    'team1_name']
            },
            'champion': champion,
            'most_wins': int(winners.iloc[0]) if not winners.empty else 0
        }

# Usage example:
# analyzer = KabaddiMatchAnalyzer(r"..\DATA\DATA__prokabaddi_dot_com\matchesoverview\merged_match_overview.csv")
analyzer = KabaddiMatchAnalyzer(r"../1_DATA/DATA__ProKabaddi-Data/Matches-Overview/merged_match_overview.csv")





# match_details = analyzer.get_match_details(1815)  # Using game_id instead of Match_No
# print(match_details)

# team_performance = analyzer.get_team_performance('Puneri Paltan')
# print(team_performance)
#
# top_raiders = analyzer.get_top_players('raider', n=5)
# print(top_raiders)
#
# venue_stats = analyzer.get_venue_statistics()
# print(venue_stats)
#
# season_timeline = analyzer.get_season_timeline(9)
# print(season_timeline)
#
head_to_head = analyzer.get_team_head_to_head('Puneri Paltan', 'U Mumba')
print(head_to_head)
#
# player_performance = analyzer.get_player_performance('Rahul Chaudhari')
# print(player_performance)
#
# season_summary = analyzer.get_season_summary(9)
# print(season_summary)
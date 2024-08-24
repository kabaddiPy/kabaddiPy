import pandas as pd
import os
from typing import List, Dict, Union, Optional


class TeamData:
    def __init__(self, data_directory: str):
        self.data_directory = data_directory
        self.season_data = self._load_season_data()

    def _load_season_data(self) -> Dict[int, pd.DataFrame]:
        season_data = {}
        for filename in os.listdir(self.data_directory):
            if filename.startswith('json_s') and filename.endswith('_teams.csv'):
                season_number = int(filename.split('_')[1][1:])
                file_path = os.path.join(self.data_directory, filename)
                season_data[season_number] = pd.read_csv(file_path)
        return season_data

    def get_team_stats(self, team_name: str, season: Optional[int] = None) -> Dict[str, Union[str, int, float]]:
        """
        Get statistics for a specific team, optionally for a specific season.

        :param team_name: Name of the team
        :param season: Season number (optional)
        :return: Dictionary containing stats for the team
        """
        if season:
            if season not in self.season_data:
                raise ValueError(f"Data for season {season} not found")
            df = self.season_data[season]
            team_data = df[df['team_name'] == team_name]
            if team_data.empty:
                raise ValueError(f"Team {team_name} not found in season {season}")
            return team_data.iloc[0].to_dict()
        else:
            all_seasons_data = []
            for s, df in self.season_data.items():
                team_data = df[df['team_name'] == team_name]
                if not team_data.empty:
                    data = team_data.iloc[0].to_dict()
                    data['season'] = s
                    all_seasons_data.append(data)
            return all_seasons_data

    def get_top_n_teams_by_metric(self, metric: str, n: int = 5, season: Optional[int] = None) -> List[
        Dict[str, Union[str, int, float]]]:
        """
        Get top N teams based on a specific metric, optionally for a specific season.

        :param metric: Metric to sort by (e.g., 'wins', 'points', 'score_diff')
        :param n: Number of top teams to return
        :param season: Season number (optional)
        :return: List of dictionaries containing team name, metric value, and season
        """
        if season:
            if season not in self.season_data:
                raise ValueError(f"Data for season {season} not found")
            df = self.season_data[season]
            sorted_df = df.sort_values(by=metric, ascending=False).head(n)
            result = sorted_df[['team_name', metric]].to_dict('records')
            for item in result:
                item['season'] = season
            return result
        else:
            all_seasons_data = []
            for s, df in self.season_data.items():
                sorted_df = df.sort_values(by=metric, ascending=False).head(n)
                result = sorted_df[['team_name', metric]].to_dict('records')
                for item in result:
                    item['season'] = s
                all_seasons_data.extend(result)
            return sorted(all_seasons_data, key=lambda x: x[metric], reverse=True)[:n]

    # def get_team_performance_trend(self, team_name: str) -> Dict[int, str]:
    #    '''
    #    DOESN'T WORK
    #    '''
    #
    #     trends = {}
    #     # for season, df in sorted(self.season_data.items()):
    #     #     team_data = df[df['team_name'] == team_name]
    #     #     if not team_data.empty:
    #     #         current_position = team_data.iloc[0]['position']
    #     #         prev_position = team_data.iloc[0]['prev_position']
    #     #         if current_position < prev_position:
    #     #             trends[season] = 'Improving'
    #     #         elif current_position > prev_position:
    #     #             trends[season] = 'Declining'
    #     #         else:
    #     #             trends[season] = 'Stable'
    #     return trends

    def get_team_win_percentage(self, team_name: str, season: Optional[int] = None) -> Union[float, Dict[int, float]]:
        """
        Calculate the win percentage for a specific team, optionally for a specific season.

        :param team_name: Name of the team
        :param season: Season number (optional)
        :return: Win percentage as a float or dictionary of season: win percentage
        """
        if season:
            if season not in self.season_data:
                raise ValueError(f"Data for season {season} not found")
            df = self.season_data[season]
            team_data = df[df['team_name'] == team_name]
            if team_data.empty:
                raise ValueError(f"Team {team_name} not found in season {season}")
            win_percentage = (team_data.iloc[0]['wins'] / team_data.iloc[0]['played']) * 100
            return round(win_percentage, 2)
        else:
            win_percentages = {}
            for s, df in self.season_data.items():
                team_data = df[df['team_name'] == team_name]
                if not team_data.empty:
                    win_percentage = (team_data.iloc[0]['wins'] / team_data.iloc[0]['played']) * 100
                    win_percentages[s] = round(win_percentage, 2)
            return win_percentages

    def compare_team_across_seasons(self, team_name: str) -> pd.DataFrame:
        """
        Compare a team's performance across all available seasons.

        :param team_name: Name of the team
        :return: Dictionary with metrics as keys and lists of values across seasons
        """
        comparison = {
            'season': [],
            'position': [],
            'wins': [],
            'lost': [],
            'points': [],
            'score_diff': [],
            'win_percentage': []
        }

        for season, df in sorted(self.season_data.items()):
            team_data = df[df['team_name'] == team_name]
            if not team_data.empty:
                data = team_data.iloc[0]
                comparison['season'].append(season)
                for metric in comparison.keys():
                    if metric != 'season' and metric != 'win_percentage':
                        comparison[metric].append(data[metric])
                win_percentage = (data['wins'] / data['played']) * 100
                comparison['win_percentage'].append(round(win_percentage, 2))
        return pd.DataFrame.from_dict(comparison)

    def get_season_summary(self, season: int) -> Dict[str, Union[str, int, float]]:
        """ ADD MORE SUMMARY STATS
        Get a summary of a specific season.

        :param season: Season number
        :return: Dictionary containing season summary statistics
        """
        if season not in self.season_data:
            raise ValueError(f"Data for season {season} not found")

        df = self.season_data[season]
        return {
            'season': season,
            'total_matches': df['played'].sum() // 2,  # Divide by 2 to avoid double counting
            'total_league_points': df['points'].sum(),
            #'avg_points_per_match': round(df['points'].sum() / (df['played'].sum() // 2), 2),
            'highest_scoring_team': df.loc[df['points'].idxmax(), 'team_name'],
            #'best_defense_team': df.loc[df['points'].idxmin(), 'team_name'],
            'most_wins': df.loc[df['wins'].idxmax(), 'team_name'],
            'champion': df.loc[df['position'].idxmin(), 'team_name']
        }

if __name__ == "__main__":
    print("hello")
    analyzer = TeamData(r'C:\Users\KIIT\Documents\ProKabaddi_API\pypi\prokabaddidata\DATA\DATA__prokabaddi_dot_com\improved_standings\standings_csvs\teams')
    # team_stats = analyzer.get_team_stats('Jaipur Pink Panthers', season=10)
    # print(team_stats)
#
# top_teams = analyzer.get_top_n_teams_by_metric('points', n=3)
# print(top_teams)

# win_percentages = analyzer.get_team_win_percentage('Bengalur Bulls')
# print(win_percentages)

team_comparison = analyzer.compare_team_across_seasons('U Mumba')
print(team_comparison)

# most_improved = analyzer.get_most_improved_team()
# print(most_improved)

# season_summary = analyzer.get_season_summary(7)
# print(season_summary)
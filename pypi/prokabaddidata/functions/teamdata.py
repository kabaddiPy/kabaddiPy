import pandas as pd
from typing import List

class KabaddiAnalyzer:
    def __init__(self, season_csv: str):
        self.df = pd.read_csv(season_csv)

    def get_team_stats(self, team_name: str, season: int) -> pd.DataFrame:
        """Get all stats for a specific team in a given season."""
        df = self.df[(self.df['team_name'] == team_name) & (self.df['season'] == season)]
        return df.T

    def top_n_teams_by_stat(self, stat: str, season: int, n: int = 5, ascending: bool = False) -> pd.DataFrame:
        """Get top N teams by a specific stat in a given season."""
        season_data = self.df[self.df['season'] == season]
        return season_data.sort_values(f'{stat}_value', ascending=ascending)[['team_name', f'{stat}_value']].head(n)

    def compare_teams(self, team1: str, team2: str, season: int) -> pd.DataFrame:
        """Compare two teams across all stats for a given season."""
        team1_data = self.get_team_stats(team1, season)
        team2_data = self.get_team_stats(team2, season)
        return pd.concat([team1_data, team2_data], axis=1, keys=[team1, team2])

    def team_ranking(self, stat: str, season: int) -> pd.DataFrame:
        """Get team rankings for a specific stat in a given season."""
        season_data = self.df[self.df['season'] == season]
        return season_data.sort_values(f'{stat}_rank')[['team_name', f'{stat}_rank']]

    def season_summary(self, season: int) -> pd.DataFrame:
        """Get a summary of the season including top teams in various categories."""
        stats = ['team-total-points', 'team-raid-points', 'team-tackle-points', 'team-all-outs-inflicted']
        summary_dfs = []
        for stat in stats:
            top_teams = self.top_n_teams_by_stat(stat, season, n=3)
            top_teams['category'] = stat
            summary_dfs.append(top_teams)
        return pd.concat(summary_dfs, ignore_index=True)

    def team_performance_trend(self, team_name: str) -> pd.DataFrame:
        """Analyze a team's performance trend across seasons."""
        team_data = self.df[self.df['team_name'] == team_name]
        x = team_data[['season', 'team-total-points_value', 'team-raid-points_value', 'team-tackle-points_value']]
        return x.sort_values('season')

    def season_competitiveness(self, season: int) -> pd.DataFrame:
        """Measure the competitiveness of a season based on the spread of total points."""
        season_data = self.df[self.df['season'] == season]
        competitiveness = season_data['team-total-points_value'].std()
        return pd.DataFrame({'season': [season], 'competitiveness': [competitiveness]})

    def most_exciting_team(self, season: int) -> pd.DataFrame:
        """Identify the most exciting team (high scoring with high points conceded) in a given season."""
        season_data = self.df[self.df['season'] == season].copy()
        season_data['excitement_score'] = season_data['team-total-points_value'] + season_data[
            'team-total-points-conceded_value']
        return season_data.sort_values('excitement_score', ascending=False)[
            ['team_name', 'team-total-points_value', 'team-total-points-conceded_value', 'excitement_score']].head(1)

# Usage example:
analyzer = KabaddiAnalyzer(r"C:\Users\KIIT\Documents\ProKabaddi_API\pypi\prokabaddidata\DATA\DATA__prokabaddi_dot_com\teams\seasons_1_to_4_final.csv")
print(analyzer.get_team_stats('Patna Pirates', 2))
# print(analyzer.compare_teams('Bengaluru Bulls', 'Patna Pirates', 2))
print(analyzer.top_n_teams_by_stat('team-tackle-points',4))
print(analyzer.team_performance_trend("Patna Pirates"))
print(analyzer.top_n_teams_by_stat('team-tackle-points',4))
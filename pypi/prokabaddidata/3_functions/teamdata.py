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
        return x
    
    def best_raiding_team(self, season: int) -> pd.DataFrame:
        """Identify the best raiding team in a given season."""
        return self.top_n_teams_by_stat('team-raid-points', season, n=1)

    def best_defending_team(self, season: int) -> pd.DataFrame:
        """Identify the best defending team in a given season."""
        return self.top_n_teams_by_stat('team-tackle-points', season, n=1)

    def most_balanced_team(self, season: int) -> pd.DataFrame:
        """Identify the most balanced team (good in both raid and defense) in a given season."""
        season_data = self.df[self.df['season'] == season].copy()
        season_data['balance_score'] = season_data['team-raid-points_rank'] + season_data['team-tackle-points_rank']
        return season_data.sort_values('balance_score')[
            ['team_name', 'team-raid-points_rank', 'team-tackle-points_rank']].head(1)

    def team_efficiency(self, season: int) -> pd.DataFrame:
        """Calculate team efficiency (points scored vs points conceded) for a given season."""
        season_data = self.df[self.df['season'] == season].copy()
        season_data['efficiency'] = season_data['team-total-points_value'] / season_data[
            'team-total-points-conceded_value']
        return season_data[['team_name', 'efficiency']].sort_values('efficiency', ascending=False)

    def most_improved_team(self, stat: str) -> pd.DataFrame:
        """Identify the most improved team across seasons for a given stat."""
        improvements = []
        for team in self.df['team_name'].unique():
            team_data = self.df[self.df['team_name'] == team].sort_values('season')
            if len(team_data) > 1:
                improvement = team_data.iloc[-1][f'{stat}_value'] - team_data.iloc[0][f'{stat}_value']
                improvements.append({'team_name': team, 'improvement': improvement})
        return pd.DataFrame(improvements).sort_values('improvement', ascending=False).head(1)

    def season_competitiveness(self, season: int) -> pd.DataFrame:
        """Measure the competitiveness of a season based on the spread of total points."""
        season_data = self.df[self.df['season'] == season]
        competitiveness = season_data['team-total-points_value'].std()
        return pd.DataFrame({'season': [season], 'competitiveness': [competitiveness]})

    def team_consistency(self) -> pd.DataFrame:
        """Measure teams' consistency across seasons."""
        consistency = self.df.groupby('team_name')['team-total-points_value'].std().reset_index()
        consistency.columns = ['team_name', 'consistency']
        return consistency.sort_values('consistency')

    def most_exciting_team(self, season: int) -> pd.DataFrame:
        """Identify the most exciting team (high scoring with high points conceded) in a given season."""
        season_data = self.df[self.df['season'] == season].copy()
        season_data['excitement_score'] = season_data['team-total-points_value'] + season_data[
            'team-total-points-conceded_value']
        return season_data.sort_values('excitement_score', ascending=False)[
            ['team_name', 'team-total-points_value', 'team-total-points-conceded_value', 'excitement_score']].head(1)

# Usage example:
# analyzer = KabaddiAnalyzer(r"C:\Users\KIIT\Documents\ProKabaddi_API\pypi\prokabaddidata\DATA\DATA__prokabaddi_dot_com\teams\seasons_1_to_4_final.csv")
# analyzer = KabaddiAnalyzer(r"C:\Users\KIIT\Documents\ProKabaddi_API\pypi\prokabaddidata\DATA\DATA__prokabaddi_dot_com\teams\seasons_1_to_4_final.csv")

analyzer = KabaddiAnalyzer("../1_DATA/DATA__ProKabaddi-Data/teams/seasons_1_to_4_final.csv")
# analyzer = KabaddiAnalyzer("../1_DATA/DATA__ProKabaddi-Data/teams/seasons_5_plus_and_all_rounded.csv")


print(analyzer.get_team_stats('Patna Pirates', 2))
# print(analyzer.compare_teams('Bengaluru Bulls', 'Patna Pirates', 2))
print(analyzer.top_n_teams_by_stat('team-tackle-points',4))
print(analyzer.team_performance_trend("Patna Pirates"))
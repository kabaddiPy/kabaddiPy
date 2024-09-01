import json
from pathlib import Path
import pandas as pd
import sys, os

# Add the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PKL_Standings import _standings as stand


def get_team_info(team_id, season='overall'):
    file_path_5_plus = Path("../1_DATA/Team-Wise-Data/seasons_5_plus_and_all_rounded.csv")
    file_path_1_to_4 = Path("../1_DATA/Team-Wise-Data/seasons_1_to_4_final.csv")


    if season != 'overall':
        season = int(season)

    df = pd.read_csv("./PKL_AggregatedTeamStats.csv")

    df['team_id'] = pd.to_numeric(df['team_id'], errors='coerce')

    team_id = int(team_id)

    if season == 'overall':
        all_row = df[(df['team_id'] == team_id) & (df['season'] == 'all')]
        other_rows = df[(df['team_id'] == team_id) & (df['season'] != 'all')]
        filtered_df = pd.concat([all_row, other_rows]).reset_index(drop=True)
    else:
        filtered_df = df[(df['team_id'] == team_id) & (df['season'] == season)]

    if filtered_df.empty:
        print(f"No data found in CSV for team_id {team_id} in season {season}")
        return None, None, None, None
    if season == 'overall':
        standings_df, matches_df = stand.get_pkl_standings(season=10, team_id=team_id, matches=True)
    else:
        standings_df, matches_df = stand.get_pkl_standings(season, team_id, matches=True)

    # Separate the columns based on the suffixes
    rank_columns = [col for col in filtered_df.columns if col.endswith('_rank')]
    value_columns = [col for col in filtered_df.columns if col.endswith('_value')]
    per_match_columns = [col for col in filtered_df.columns if col.endswith('_per-match')]

    df_rank = filtered_df[['season', 'team_id', 'team_name'] + rank_columns]
    df_value = filtered_df[['season', 'team_id', 'team_name'] + value_columns]
    df_per_match = filtered_df[['season', 'team_id', 'team_name'] + per_match_columns]

    return df_rank, df_value, df_per_match, standings_df, matches_df


if __name__ == '__main__':
    df_rank, df_value, df_per_match, df2, df3 = get_team_info('4')
    print("Rank DataFrame:")
    print(df_rank)
    print()
    print("Value DataFrame:")
    print(df_value)
    print()
    print("Per-Match DataFrame:")
    print(df_per_match)
    print()
    print("Standings DataFrame:")
    print(df2)
    print()
    print("Matches DataFrame:")
    print(df3)

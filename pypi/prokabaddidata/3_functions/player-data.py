import pandas as pd


def get_top_ranked_players(season=10, metric='total points', top=20):
    df = pd.read_csv(r"../1_DATA/Player-Wise-Data/all_seasons_player_stats_rounded.csv")
    pd.options.mode.chained_assignment = None  # default='warn'
    season = int(season)

    metric_mapping = {
        'super tackle points': 'player-super-tackles',
        'raid points': 'player-raid-points',
        'super raids': 'player-super-raids',
        'high 5s': 'high-5s',
        'tackle points': 'player-tackle-points',
        'average tackle points': 'player-avg-tackle-points',
        'do-or-die raid points': 'player-dod-raid-points',
        'total points': 'player-total-points',
        'successful tackles': 'player-successful-tackles',
        'successful raids': 'player-successful-raids',
        'super 10s': 'super-10s'
    }

    if metric.lower() not in metric_mapping:
        raise ValueError(f"Invalid metric. Choose from: {', '.join(metric_mapping.keys())}")

    column_name = metric_mapping[metric.lower()]
    filtered_df = df[df['season'] == season].sort_values(f'{column_name}_rank')
    result_df = filtered_df[[
        'player_id',
        'season',
        'player-total-points_player_name',
        'player-total-points_team_name',
        'player-total-points_match_played',
        f'{column_name}_rank',
        f'{column_name}_value',
        f'{column_name}_points_per_match'
    ]]

    result_df.columns = ['Player ID', 'Season', 'Player Name', 'Team Name', 'Matches Played', 'Rank', metric,
                         'Points per Match']
    result_df['Player ID'] = result_df['Player ID'].astype(int)
    result_df.set_index('Rank', inplace=True)
    result_df = result_df.head(top)
    return result_df

def get_raiders_v_defenders(player_id, season):
    csv_path = r"../1_DATA/Player-Wise-Data/Raiders-v-No-Of-Defenders_CLEAN/merged_raider_v_num_defenders_FINAL.csv"
    df = pd.read_csv(csv_path, dtype={'player-id-p': int})
    if 0:
        return df
    # Query the DataFrame based on player ID and season
    result = df[(df['player-id'] == player_id)]

    # Select specific columns
    # columns_to_return = ['season', 'team_name', 'player-id', 'Raider Name', 'Number of Defenders',
    #                      'Total Raids', '% of Raids', 'Empty','Successful', 'Unsuccessful']

    return result

    # Example usage:
    # csv_path = 'path_to_your_csv_file.csv'
    # player_id = 644
    # season = 'PKL-06'
    # result = load_and_query_raider_data(csv_path, player_id, season)
    # print(result)

# Example usage:
# Assuming 'df' is your pandas DataFrame
# top_players = get_top_ranked_players(metric="do-or-die raid points")
# print(top_players)


player_id = 644
season = 'PKL-06'
result = get_raiders_v_defenders(player_id, season)
print(result)
import pandas as pd
import numpy as np

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

def get_raiders_v_defenders(player_id, season=None):
    csv_path = r"../1_DATA/Player-Wise-Data/Raiders-v-No-Of-Defenders_CLEAN/merged_raider_v_num_defenders_FINAL.csv"
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_path)

    # Filter the DataFrame for the specific player ID
    df['player-id'] = df['player-id'].astype(int)

    # Convert the passed player_id to integer as well
    player_id = int(player_id)

    # Filter the DataFrame for the specific player ID
    player_data = df[df['player-id'] == player_id]

    # Print the number of rows found
    print(f"\nRows found for player_id {player_id}: {len(player_data)}")

    # If no data found for the player ID, return None
    if player_data.empty:
        return None

    # Return the filtered DataFrame
    return player_data

    # Example usage:
    # csv_path = 'path_to_your_csv_file.csv'
    # player_id = 644
    # season = 'PKL-06'
    # result = load_and_query_raider_data(csv_path, player_id, season)
    # print(result)


def clean_player_data():
    csv_file = r"../1_DATA/Player-Wise-Data/Raiders-v-No-Of-Defenders_CLEAN/merged_raider_v_num_defenders_FINAL.csv"
    df = pd.read_csv(csv_file)
    def to_numeric_or_nan(x):
        try:
            return pd.to_numeric(x)
        except ValueError:
            return np.nan
    df['player-id'] = df['player-id'].apply(to_numeric_or_nan)
    df['player-id'] = df['player-id'].fillna(-1)
    df['player-id'] = df['player-id'].astype(int)

    return df

def get_player_details(player_id, season=10):
    df = clean_player_data()
    player_id = int(player_id)

    player_data = df[df['player-id'] == player_id]
    if player_data.empty:
        return "No player found"
    filtered_df = player_data[player_data['season'].str.extract(r'(\d+)')[0].astype(int) == season]

    if filtered_df.empty:
        return f"No data for season {season}"

    return filtered_df


import pandas as pd


def get_player_info(player_id, season=None):
    file_path = r"../1_DATA/Player-Wise-Data/all_seasons_player_stats_rounded.csv"
    df = pd.read_csv(file_path)
    print(df.info())
    def to_numeric_or_nan(x):
        try:
            return pd.to_numeric(x)
        except ValueError:
            return np.nan

    df['player_id'] = df['player_id'].apply(to_numeric_or_nan)
    df['player_id'] = df['player_id'].fillna(-1)
    df['player_id'] = df['player_id'].astype(int)

    # If season is not specified, use the latest season
    if season is None:
        season = df['season'].max()

    # Query the DataFrame
    result = df[(df['player_id'] == player_id) & (df['season'] == season)]

    return result


# Example usage:
# file_path = 'your_csv_file.csv'
# player_id = 10
# result = query_dataframe(file_path, player_id)  # Returns latest season
# result = query_dataframe(file_path, player_id, season=3)  # Returns specific season
# print(result)

if __name__ == "__main__":
# top_players = get_top_ranked_players(metric="do-or-die raid points")
# print(top_players)

# player_id = 644  # Example player ID
# player_details = get_player_details(player_id, season=6)


#     print("Player details:")
#     print(player_details)

    player_id = 10
    result = get_player_info(player_id)  # Returns latest season
    print(result)
    # top_players = get_top_ranked_players()
    # print(top_players)
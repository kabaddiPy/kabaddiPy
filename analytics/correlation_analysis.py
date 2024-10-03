import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def prepare_data(season: int) -> pd.DataFrame:
    """
    Load and merge player and match data for a given season.
    """
    # Load player stats
    player_stats = pd.read_csv('Player-Wise-Data/all_seasons_player_stats_rounded.csv')
    player_stats = player_stats[player_stats['Season'] == season]

    # Load match stats
    match_stats = pd.read_json(f'Matches-Overview/S{season}_PKL_MatchData.json')

    # Rename columns to have a common key for merging
    player_stats.rename(columns={'MatchID': 'Match_ID'}, inplace=True)
    match_stats.rename(columns={'Match_ID': 'Match_ID'}, inplace=True)  # Adjust if needed

    # Merge dataframes
    merged_data = pd.merge(player_stats, match_stats, on='Match_ID', how='inner')

    # Handle missing values
    merged_data.dropna(inplace=True)

    return merged_data


def calculate_correlations(data: pd.DataFrame, method: str = 'pearson') -> pd.DataFrame:
    """
    Calculate correlation matrix for numerical columns in the data.

    Parameters:
        data (pd.DataFrame): The preprocessed data.
        method (str): Correlation method ('pearson', 'spearman', 'kendall').

    Returns:
        pd.DataFrame: Correlation matrix.
    """
    numeric_cols = data.select_dtypes(include='number')
    corr_matrix = numeric_cols.corr(method=method)
    return corr_matrix


def visualize_correlations(corr_matrix: pd.DataFrame, title: str = "Correlation Matrix", figsize=(12, 10)) -> None:
    """
    Visualize the correlation matrix using a heatmap.

    Parameters:
        corr_matrix (pd.DataFrame): The correlation matrix to visualize.
        title (str): Title of the heatmap.
        figsize (tuple): Figure size for the plot.
    """
    plt.figure(figsize=figsize)
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title(title)
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.show()

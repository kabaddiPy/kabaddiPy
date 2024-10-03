import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def prepare_data(season: int) -> pd.DataFrame:
    """
    Load and merge player and match data for a given season.
    """
    # Load player stats
    player_stats = pd.read_csv('all_seasons_player_stats_rounded.csv')
    player_stats = player_stats[player_stats['season'] == season]

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


def explain_correlation(corr_matrix: pd.DataFrame, threshold: float = 0.7) -> None:
    """
    Explain high correlation pairs based on a threshold.

    Parameters:
        corr_matrix (pd.DataFrame): The correlation matrix.
        threshold (float): Correlation threshold to highlight strong correlations.
    """
    high_corr = (corr_matrix.abs() > threshold) & (corr_matrix != 1.0)
    strong_correlations = high_corr.stack().reset_index()
    strong_correlations = strong_correlations[strong_correlations[0]]

    print("High Correlation Pairs (absolute correlation > {:.2f}):".format(threshold))
    for index, row in strong_correlations.iterrows():
        col1, col2, _ = row
        corr_value = corr_matrix.loc[col1, col2]
        print(f"{col1} and {col2} have a correlation of {corr_value:.2f}.")
        if corr_value > 0:
            print(f"This means {col1} and {col2} tend to increase or decrease together.")
        else:
            print(f"This means when {col1} increases, {col2} tends to decrease, and vice versa.")
        print()










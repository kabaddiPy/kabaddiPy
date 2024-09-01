import pandas as pd
import os

# List of actual file paths
L = [
    './season_s-10/season10_individual_stats_df_teams/18_df_team_season10_team-all-outs-conceded.csv',
    './season_s-10/season10_individual_stats_df_teams/17_df_team_season10_team-all-outs-inflicted.csv',
    './season_s-10/season10_individual_stats_df_teams/16_df_team_season10_team-dod-raid-points.csv',
    './season_s-10/season10_individual_stats_df_teams/15_df_team_season10_team-super-tackles.csv',
    './season_s-10/season10_individual_stats_df_teams/14_df_team_season10_team-super-raid.csv',
    './season_s-10/season10_individual_stats_df_teams/13_df_team_season10_team-average-tackle-points.csv',
    './season_s-10/season10_individual_stats_df_teams/12_df_team_season10_team-tackle-points.csv',
    './season_s-10/season10_individual_stats_df_teams/11_df_team_season10_team-successful-tackles.csv',
    './season_s-10/season10_individual_stats_df_teams/10_df_team_season10_team-average-raid-points.csv',
    './season_s-10/season10_individual_stats_df_teams/9_df_team_season10_team-raid-points.csv',
    './season_s-10/season10_individual_stats_df_teams/8_df_team_season10_team-successful-raids.csv',
    './season_s-10/season10_individual_stats_df_teams/7_df_team_season10_team-avg-points-scored.csv',
    './season_s-10/season10_individual_stats_df_teams/6_df_team_season10_team-total-points-conceded.csv',
    './season_s-10/season10_individual_stats_df_teams/5_df_team_season10_team-successful-tackle-percent.csv',
    './season_s-10/season10_individual_stats_df_teams/4_df_team_season10_team-successful-tackles-per-match.csv',
    './season_s-10/season10_individual_stats_df_teams/3_df_team_season10_team-successful-raid-percent.csv',
    './season_s-10/season10_individual_stats_df_teams/2_df_team_season10_team-raid.csv',
    './season_s-10/season10_individual_stats_df_teams/1_df_team_season10_team-total-points.csv',
        # Add more paths as needed
]

def extract_suffix_from_filename(file_path):
    file_name = os.path.basename(file_path)


    suffix = file_name.split('_')[-1].replace(".csv", "").replace("team-", "")
    # print(suffix)
    return suffix


# for i in L:
#     extract_suffix_from_filename(i)



def merge_multiple_csvs(file_paths):
    merged_df = None
    
    for file_path in file_paths:
        # Extract suffix from the file name
        suffix = extract_suffix_from_filename(file_path)
        
        # Load the current CSV
        current_df = pd.read_csv(file_path)
        
        # Rename the columns using the extracted suffix
        current_df.columns = [f"{col}-{suffix}" if col != 'team_id' else 'team_id' for col in current_df.columns]
        
        # Merge with the existing dataframe
        if merged_df is None:
            merged_df = current_df
        else:
            merged_df = pd.merge(merged_df, current_df, on='team_id')
    
    return merged_df

# Perform the merge operation
merged_df_all = merge_multiple_csvs(L)

merged_df_all.to_csv('./season_s-10/merged_df_all.csv', index=False)

# Display the final merged dataframe
print(merged_df_all)

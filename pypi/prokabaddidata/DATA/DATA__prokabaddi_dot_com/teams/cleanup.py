import pandas as pd

df = pd.read_csv('all_seasons_team_stats.csv')

start_col = 'team-average-raid-points_team_name'
end_col = 'team-successful-tackles_team_name'

start_idx = df.columns.get_loc(start_col)
end_idx = df.columns.get_loc(end_col)

df['team_name'] = df.iloc[:, start_idx]

columns_to_keep = list(df.columns[:start_idx]) + ['team_name'] + list(df.columns[end_idx+1:])

df_new = df[columns_to_keep]

team_id_idx = df_new.columns.get_loc('team_id')
cols = list(df_new.columns)
cols.insert(team_id_idx + 1, cols.pop(cols.index('team_name')))
df_new = df_new[cols]

df_new.to_csv('all_seasons_team_stats_cleaned.csv', index=False)

print(df_new.head())
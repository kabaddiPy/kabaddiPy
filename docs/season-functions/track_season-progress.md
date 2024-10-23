```docs/visualization-functions/track_season_progress.md
---
layout: default
title: track_season_progress
parent: Visualization Functions
nav_order: 5
---
## `track_season_progress(season, team_id)`

Track a team's journey across the season, highlighting key wins, losses, and pivotal moments that impacted their standings.

### Parameters:
- `season` (int): The season number for which to track the team's progress.
- `team_id` (int): The ID of the team to track.

### Returns:
A dictionary containing:
- `matches_df` (DataFrame): A DataFrame with all matches played by the team.
- `standings_df` (DataFrame): A DataFrame with the standings of the team throughout the season.
- `visualizations` (list): A list of visualizations showing the team's performance trends.

### Example Usage:
```python
from kabaddiPy import PKL

import matplotlib.pyplot as plt

pkl = PKL()
team_id = 30  # Specify the team ID you want to track
progress = pkl.track_season_progress(season=9, team_id=2)

matches_df = progress['matches_df']
standings_df = progress['standings_df']
visualizations = progress['visualizations']

print("Matches played by the team:")
print(matches_df)

print("\nStandings throughout the season:")
print(standings_df)

# Display visualizations
for viz in visualizations:
    viz.show()

plt.show()
```

### Example Output:
```python
Matches played by the team:
    Season Match_ID    Match_Name League_Stage  Year  ...           team_name_1 team_id_1           team_name_2 team_id_2 Points
0        9     2892       Match 1       League  2022  ...     Dabang Delhi K.C.         2               U Mumba         5     41
10       9     2902      Match 11       League  2022  ...     Dabang Delhi K.C.         2        Gujarat Giants        31     53
14       9     2906      Match 15       League  2022  ...          U.P. Yoddhas        30     Dabang Delhi K.C.         2     44
19       9     2911      Match 20       League  2022  ...         Telugu Titans         8     Dabang Delhi K.C.         2     46
24       9     2916      Match 25       League  2022  ...     Dabang Delhi K.C.         2      Haryana Steelers        28     38
31       9     2923      Match 32       League  2022  ...         Patna Pirates         6     Dabang Delhi K.C.         2     33
40       9     2932      Match 41       League  2022  ...     Dabang Delhi K.C.         2       Bengal Warriors         4     30
44       9     2936      Match 45       League  2022  ...       Bengaluru Bulls         1     Dabang Delhi K.C.         2     43
48       9     2940      Match 49       League  2022  ...       Tamil Thalaivas        29     Dabang Delhi K.C.         2     39
51       9     2943      Match 52       League  2022  ...         Puneri Paltan         7     Dabang Delhi K.C.         2     38
56       9     2948      Match 57       League  2022  ...     Dabang Delhi K.C.         2  Jaipur Pink Panthers         3     40
66       9     2958      Match 67       League  2022  ...     Dabang Delhi K.C.         2         Telugu Titans         8     40
74       9     2966      Match 75       League  2022  ...  Jaipur Pink Panthers         3     Dabang Delhi K.C.         2     32
82       9     2974      Match 83       League  2022  ...     Dabang Delhi K.C.         2          U.P. Yoddhas        30     31
88       9     2980      Match 89       League  2022  ...     Dabang Delhi K.C.         2         Patna Pirates         6     30
89       9     2981      Match 90       League  2022  ...      Haryana Steelers        28     Dabang Delhi K.C.         2     42
97       9     2989      Match 98       League  2022  ...        Gujarat Giants        31     Dabang Delhi K.C.         2     50
104      9     2996     Match 105       League  2022  ...     Dabang Delhi K.C.         2       Bengaluru Bulls         1     49
110      9     3002     Match 111       League  2022  ...     Dabang Delhi K.C.         2       Tamil Thalaivas        29     37
114      9     3006     Match 115       League  2022  ...     Dabang Delhi K.C.         2         Puneri Paltan         7     44
121      9     3013     Match 122       League  2022  ...               U Mumba         5     Dabang Delhi K.C.         2     41
125      9     3017     Match 126       League  2022  ...       Bengal Warriors         4     Dabang Delhi K.C.         2     46
132      9     3024  Eliminator 1     Playoffs  2022  ...       Bengaluru Bulls         1     Dabang Delhi K.C.         2     24

[23 rows x 18 columns]

Standings throughout the season:
  Group  Season  Team_Id          Team_Name  League_position  Matches_played Wins Lost Tied Draws No Result League_points Score_diff  Qualified   
5  Main       9        2  Dabang Delhi K.C.                6              22   10   10    2     0         0            63         17       True 
```

### Visualizations:
The function generates the following visualizations to show performance trends:

1. **Win/Loss Trend**: A line graph showing the number of wins and losses over the season.
2. **Points Accumulation**: A line graph showing the accumulation of points over the season.
3. **League Position**: A line graph showing the team's position in the league standings over the season.

### Notes:
- This function loads the matches and standings data for the specified season and team.
- It generates visualizations to help analyze the team's performance trends throughout the season.
- If no data is available for the specified season and team, the function returns empty DataFrames and an empty list of visualizations.
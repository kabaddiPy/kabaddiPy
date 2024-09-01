
## Functions

### `get_pkl_standings(season=None, team_id=None, matches=True)`

Retrieves standings and match data for a specific season and team.

#### Parameters:
- `season` (int, optional): The season number. If not provided, defaults to 10.
- `team_id` (int, optional): The team ID to filter results. If not provided, returns data for all teams.
- `matches` (bool, optional): Whether to include match data. Defaults to False.

#### Returns:
- If `matches` is True: A tuple of two DataFrames (team_info_df, matches_df)
- If `matches` is False: A single DataFrame (team_info_df)

#### Example Usage:
```python
# Get standings for all teams in season 10 without match data
standings = get_pkl_standings()
print(standings)

    Season             Team_Name  Team_Id team_short_name League_position Matches_played Wins Lost Tied Draws No Result League_points Score_diff  Qualified
0       10         Puneri Paltan        7            Pune               1             22   17    2    3     0         0            96        253       True
1       10  Jaipur Pink Panthers        3          Jaipur               2             22   16    3    3     0         0            92        141       True
2       10     Dabang Delhi K.C.        2           Delhi               3             22   13    6    3     0         0            79         53       True
3       10        Gujarat Giants       31         Gujarat               4             22   13    9    0     0         0            70         32       True
4       10      Haryana Steelers       28         Haryana               5             22   13    8    1     0         0            70        -13       True
5       10         Patna Pirates        6           Patna               6             22   11    8    3     0         0            69         50       True
6       10       Bengal Warriorz        4          Bengal               7             22    9   11    2     0         0            55        -43      False
7       10       Bengaluru Bulls        1       Bengaluru               8             22    8   12    2     0         0            53        -67      False
8       10       Tamil Thalaivas       29      Tamil Nadu               9             22    9   13    0     0         0            51         32      False
9       10               U Mumba        5          Mumbai              10             22    6   13    3     0         0            45        -79      False
10      10            UP Yoddhas       30              UP              11             22    4   17    1     0         0            31       -116      False
11      10         Telugu Titans        8       Hyderabad              12             22    2   19    1     0         0            21       -243      False


standings, matches = get_pkl_standings(matches=True)
print(matches)
#returns a DataFrame of all the matches for the latest season

          Team_Id        date result opponent  team_score  opponent_score                    match_result
match id
3030            5  2023-12-02      W       UP          34              31            U Mumba Won by 3 Pts
3029           31  2023-12-02      W      HYD          38              32     Gujarat Giants Won by 6 Pts
3031           29  2023-12-03      W      DEL          42              31   Tamil Thalaivas Won by 11 Pts
3032           31  2023-12-03      W      BLR          34              31     Gujarat Giants Won by 3 Pts
3033            7  2023-12-04      W      JAI          37              33      Puneri Paltan Won by 4 Pts
...           ...         ...    ...      ...         ...             ...                             ...
3162           28  2024-02-26      W      GUJ          42              25  Haryana Steelers Won by 17 Pts
3161            6  2024-02-26      W      DEL          37              35      Patna Pirates Won by 2 Pts
3163            7  2024-02-28      W      PAT          37              21     Puneri Paltan Won by 16 Pts
3164           28  2024-02-28      W      JAI          31              27   Haryana Steelers Won by 4 Pts
3165            7  2024-03-01      W      HAR          28              25      Puneri Paltan Won by 3 Pts

```
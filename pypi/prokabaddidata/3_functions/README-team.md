# PKL Team Functions

This document provides an overview of the functions used to retrieve and analyze Pro Kabaddi League (PKL) standings and team information.

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

### `get_team_info(team_id, season='overall')`

Retrieves detailed information about a specific team for a given season or overall.

#### Parameters:
- `team_id` (int): The ID of the team to retrieve information for.
- `season` (str or int, optional): The season to retrieve data for. Can be 'overall' for all seasons or a specific season number. Defaults to 'overall'.

#### Returns:
A tuple of three elements:
1. DataFrame with team information from CSV
2. DataFrame with PKL standings (or None if not available)
3. DataFrame with match data (or None if not available)

#### Example Usage:
```python
['season', 'team_id', 'team_name', 'matches_played',
       'team-average-raid-points_rank', 'team-avg-points-scored_rank',
       'team-all-outs-conceded_rank', 'team-successful-tackle-percent_rank',
       'team-super-raid_rank', 'team-raid_rank',
       'team-successful-raid-percent_rank', 'team-dod-raid-points_rank',
       'team-super-tackles_rank', 'team-raid-points_rank',
       'team-successful-raids_rank', 'team-total-points-conceded_rank',
       'team-tackle-points_rank', 'team-total-points_rank',
       'team-successful-tackles-per-match_rank',
       'team-all-outs-inflicted_rank', 'team-average-tackle-points_rank',
       'team-successful-tackles_rank', 'team-average-raid-points_value',
       'team-avg-points-scored_value', 'team-all-outs-conceded_value',
       'team-successful-tackle-percent_value', 'team-super-raid_value',
       'team-raid_value', 'team-successful-raid-percent_value',
       'team-dod-raid-points_value', 'team-super-tackles_value',
       'Total touch points', 'Total bonus points', 'team-raid-points_value',
       'team-successful-raids_value', 'team-total-points-conceded_value',
       'team-tackle-points_value', 'team-total-points_value',
       'team-successful-tackles-per-match_value',
       'team-all-outs-inflicted_value', 'team-average-tackle-points_value',
       'team-successful-tackles_value', 'team-average-raid-points_per-match',
       'team-avg-points-scored_per-match', 'team-all-outs-conceded_per-match',
       'team-successful-tackle-percent_per-match', 'team-super-raid_per-match',
       'team-raid_per-match', 'team-successful-raid-percent_per-match',
       'team-dod-raid-points_per-match', 'team-super-tackles_per-match',
       'team-total-touch-points-ext_per-match',
       'team-total-bonus--points-ext_per-match', 'team-raid-points_per-match',
       'team-successful-raids_per-match',
       'team-total-points-conceded_per-match', 'team-tackle-points_per-match',
       'team-total-points_per-match',
       'team-successful-tackles-per-match_per-match',
       'team-all-outs-inflicted_per-match',
       'team-average-tackle-points_per-match',
       'team-successful-tackles_per-match']
```


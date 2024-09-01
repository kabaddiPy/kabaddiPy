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
  season  team_id        team_name  ...  team-all-outs-inflicted_per-match  team-average-tackle-points_per-match  team-successful-tackles_per-match
0    all        4  Bengal Warriors  ...                              1.169                                 0.046                              8.318
1      5        4  Bengal Warriors  ...                              1.125                                 0.335                              7.542
2      8        4  Bengal Warriors  ...                              1.227                                 0.368                              7.545
3      6        4  Bengal Warriors  ...                              1.000                                 0.378                              8.087
4      7        4  Bengal Warriors  ...                              1.708                                 0.398                              9.042
5      9        4  Bengal Warriors  ...                              1.364                                 0.442                              9.273
6     10        4  Bengal Warriors  ...                              1.409                                 0.421                              8.727

[7 rows x 62 columns]
  Group  Season        Team_Name  Team_Id team_short_name League_position Matches_played Wins Lost Tied Draws No Result League_points Score_diff  Qualified
0            10  Bengal Warriorz        4          Bengal               7             22    9   11    2     0         0            55        -43      False
         Group  Team_Id        date result opponent  team_score  opponent_score                   match_result
match id
3034                  4  2023-12-04      W      BLR          32              30   Bengal Warriorz Won by 2 Pts
3044                  4  2023-12-10      W      CHE          48              38  Bengal Warriorz Won by 10 Pts
3048                  4  2023-12-12      W      PAT          60              42  Bengal Warriorz Won by 18 Pts
3092                  4  2024-01-09      W      HYD          46              26  Bengal Warriorz Won by 20 Pts
3098                  4  2024-01-13      W       UP          42              37   Bengal Warriorz Won by 5 Pts
3101                  4  2024-01-15      W      BLR          35              29   Bengal Warriorz Won by 6 Pts
3128                  4  2024-02-02      W      DEL          45              38   Bengal Warriorz Won by 7 Pts
3142                  4  2024-02-10      W      HYD          55              35  Bengal Warriorz Won by 20 Pts
3146                  4  2024-02-12      W      MUM          46              34  Bengal Warriorz Won by 12 Pts

```


# PKL Team Functions

This document provides an overview of the functions used to retrieve and analyze Pro Kabaddi League (PKL) standings and team information.


## NEW

# PKL Team Functions

This document provides an overview of the functions used to retrieve and analyze Pro Kabaddi League (PKL) standings and team information.

### `get_team_info(team_id, season='overall')`

Retrieves detailed information about a specific team for a given season or overall.

#### Parameters:
- `team_id` (int): The ID of the team to retrieve information for.
- `season` (str or int, optional): The season to retrieve data for. Can be 'overall' for all seasons or a specific season number. Defaults to 'overall'.

#### Returns:
A tuple of five elements:
1. **Rank DataFrame**: Contains columns related to rank statistics for the team.
2. **Value DataFrame**: Contains columns related to absolute values/statistics for the team.
3. **Per-Match DataFrame**: Contains columns related to per-match statistics for the team.
4. **Standings DataFrame**: PKL standings for the specified team (or None if not available).
5. **Matches DataFrame**: Match data for the specified team (or None if not available).

#### Example Usage:
```python
df_rank, df_value, df_per_match, df_standings, df_matches = get_team_info('4')

# Displaying the Rank DataFrame
print("Rank DataFrame:")
print(df_rank)

# Displaying the Value DataFrame
print("Value DataFrame:")
print(df_value)

# Displaying the Per-Match DataFrame
print("Per-Match DataFrame:")
print(df_per_match)

# Displaying the Standings DataFrame
print("Standings DataFrame:")
print(df_standings)

# Displaying the Matches DataFrame
print("Matches DataFrame:")
print(df_matches)


### Sample Output:

**Rank DataFrame:**

```python
season  team_id        team_name  team-average-raid-points_rank  team-avg-points-scored_rank  ...  team-total-points_rank  team-successful-tackles-per-match_rank  team-all-outs-inflicted_rank  team-average-tackle-points_rank  team-successful-tackles_rank
0     all        4  Bengal Warriors                              6                           11  ...                       7                                     NaN                             7                               12                             8
1       1        4  Bengal Warriors                              5                            7  ...                       7                                     NaN                             8                                6                             6
2       2        4  Bengal Warriors                              8                            8  ...                       8                                     NaN                             6                                6                             7
3       3        4  Bengal Warriors                              6                            5  ...                       4                                     NaN                             7                                4                             4
...
```

** Value Dataframe**

```python
season  team_id        team_name  team-average-raid-points_value  team-avg-points-scored_value  ...  team-total-points_value  team-successful-tackles-per-match_value  team-all-outs-inflicted_value  team-average-tackle-points_value  team-successful-tackles_value
0     all        4  Bengal Warriors                           19.45                         32.58  ...                     6354                                      NaN                            228                              8.98                           1622
1       1        4  Bengal Warriors                           20.21                         30.71  ...                      430                                      NaN                             22                              8.71                            106
2       2        4  Bengal Warriors                           13.14                         26.21  ...                      367                                      NaN                              6                              9.79                            116
3       3        4  Bengal Warriors                           15.63                         28.75  ...                      460                                      NaN                              4                              9.38                            137
...
```

**Per-Match DataFrame**

```python
season  team_id        team_name  team-average-raid-points_per-match  ...  team-successful-tackles-per-match_per-match  team-all-outs-inflicted_per-match  team-average-tackle-points_per-match  team-successful-tackles_per-match
0     all        4  Bengal Warriors                               0.100  ...                                        0.000                              1.169                                 0.046                              8.318
1       1        4  Bengal Warriors                               1.444  ...                                        0.000                              1.571                                 0.622                              7.571
2       2        4  Bengal Warriors                               0.939  ...                                        0.000                              0.429                                 0.699                              8.286
3       3        4  Bengal Warriors                               0.977  ...                                        0.000                              0.250                                 0.586                              8.563
...
```


```python
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













## OLD (bhaskar version)


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


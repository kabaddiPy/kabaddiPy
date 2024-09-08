---
title: get_standings
parent: Overall_Functions
nav_order: 1
---

# Get PKL Standings 

Overview
{: .label .label-green }

## `get_pkl_standings(season=None, qualified=False, team_id=None)`

Retrieve the Pro Kabaddi League (PKL) standings for a specified season.
 
##### Parameters:
{: .no_toc}
{: .no_toc}
- `season` : int, optional
    The season number for which to retrieve standings. Defaults to 10 if not specified.
- `qualified` : bool, optional
    If True, returns an additional DataFrame with only qualified teams. Defaults to False.
- `team_id` : int, optional
    If specified, returns standings for only this team. Defaults to None (all teams).

##### Returns:
{: .no_toc}

A DataFrame containing standings for all teams. If qualified is True, also returns qualified team standings in a dataframe.




### Example Usage
{: .no_toc}
```python
    qualified_df, all_standings_df = pkl.get_standings(season=9, qualified=True)
    
    print("Qualified teams:")
    print(qualified_df)
    print("\nAll standings:")
    print(all_standings_df)
```


```python
Qualified teams:
  Group  Season  Team_Id             Team_Name League_position Matches_played Wins Lost Tied Draws No Result League_points Score_diff  Qualified
0  Main       9        3  Jaipur Pink Panthers               1             22   15    6    1     0         0            82        174       True
1  Main       9        7         Puneri Paltan               2             22   14    6    2     0         0            80         66       True
2  Main       9        1       Bengaluru Bulls               3             22   13    8    1     0         0            74         39       True
3  Main       9       30            UP Yoddhas               4             22   12    8    2     0         0            71         42       True
4  Main       9       29       Tamil Thalaivas               5             22   10    8    4     0         0            66          5       True
5  Main       9        2     Dabang Delhi K.C.               6             22   10   10    2     0         0            63         17       True

All standings:
   Group  Season  Team_Id             Team_Name League_position Matches_played Wins Lost Tied Draws No Result League_points Score_diff  Qualified
0   Main       9        3  Jaipur Pink Panthers               1             22   15    6    1     0         0            82        174       True
1   Main       9        7         Puneri Paltan               2             22   14    6    2     0         0            80         66       True
2   Main       9        1       Bengaluru Bulls               3             22   13    8    1     0         0            74         39       True
3   Main       9       30            UP Yoddhas               4             22   12    8    2     0         0            71         42       True
4   Main       9       29       Tamil Thalaivas               5             22   10    8    4     0         0            66          5       True
5   Main       9        2     Dabang Delhi K.C.               6             22   10   10    2     0         0            63         17       True
6   Main       9       28      Haryana Steelers               7             22   10   10    2     0         0            61         16      False
7   Main       9       31        Gujarat Giants               8             22    9   11    2     0         0            59        -16      False
8   Main       9        5               U Mumba               9             22   10   12    0     0         0            56        -28      False
9   Main       9        6         Patna Pirates              10             22    8   11    3     0         0            54        -58      False
10  Main       9        4       Bengal Warriorz              11             22    8   11    3     0         0            53        -12      False
11  Main       9        8         Telugu Titans              12             22    2   20    0     0         0            15       -245      False
```

##### Note:
{: .no_toc}

If the standings data for the specified season is empty, an empty DataFrame is returned.

---
title: Overall_Functions
layout: default
has_toc: true
has_children: true
nav_order: 2
---

### Table of contents

{: .no_toc .text-delta }

1. TOC
{:toc}


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


##### Note:
{: .no_toc}

If the standings data for the specified season is empty, an empty DataFrame is returned.


### Example Usage
{: .no_toc}
```python
    qualified_df, all_standings_df = pkl.get_standings(season=9, qualified=True)
    
    print("Qualified teams:")
    print(qualified_df)
    print("\nAll standings:")
    print(all_standings_df)
```

Output:

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


# Get PKL Matches

Overview
{: .label .label-green }

## `get_season_matches(self, season="all")`

Retrieve match data for a specific season or all seasons.

This function loads match data from JSON files and returns it as a pandas DataFrame.

##### Parameters
{: .no_toc}
- **season**: `str` or `int`, optional  
  The season number for which to retrieve match data. Use `"all"` to retrieve data for all seasons (default). If a specific season is desired, provide the season number as a string or integer.


##### Returns
{: .no_toc}
- **pandas.DataFrame**  
  A DataFrame containing match details with.
##### Notes
{: .no_toc}
  - For `"all"` seasons, it sorts the files based on the season number extracted from the filename.
  - Each row in the returned DataFrame represents a single match.


### Example Usage
{: .no_toc}
```python
    season_matches = pkl.get_season_matches(season=6)
    print(season_matches.head())

```

Output:

```python
  Season Match_ID Match_Name League_Stage  Year                                     Venue                  Match_Outcome              Start_Date                End_Date Result Winning Margin team_score_1 team_score_2        team_name_1 team_id_1       team_name_2 team_id_2
0      6      625    Match 1       League  2018  Jawaharlal Nehru Indoor Stadium, Chennai  Tamil Thalaivas Won by 16 Pts  2018-10-07T20:00+05:30  2018-10-07T20:00+05:30      W             16           42           26    Tamil Thalaivas        29     Patna Pirates         6
1      6      626    Match 2       League  2018  Jawaharlal Nehru Indoor Stadium, Chennai                                 2018-10-07T21:00+05:30  2018-10-07T21:00+05:30   Tied                          32           32      Puneri Paltan         7           U Mumba         5
2      6      627    Match 3       League  2018  Jawaharlal Nehru Indoor Stadium, Chennai    Puneri Paltan Won by 12 Pts  2018-10-08T20:00+05:30  2018-10-08T20:00+05:30      W             12           34           22      Puneri Paltan         7  Haryana Steelers        28
3      6      628    Match 4       League  2018  Jawaharlal Nehru Indoor Stadium, Chennai       U.P. Yoddha Won by 5 Pts  2018-10-08T21:00+05:30  2018-10-08T21:00+05:30      W              5           32           37    Tamil Thalaivas        29       U.P. Yoddha        30
4      6      629    Match 5       League  2018  Jawaharlal Nehru Indoor Stadium, Chennai                                 2018-10-09T20:00+05:30  2018-10-09T20:00+05:30   Tied                          32           32  Dabang Delhi K.C.         2    Gujarat Giants        31
```

---
layout: default
title: get_season_matches
parent: Season Functions
nav_order: 1
---
# Get PKL Matches

Season
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
##### Notes
{: .no_toc}
  - For `"all"` seasons, it sorts the files based on the season number extracted from the filename.
  - Each row in the returned DataFrame represents a single match.

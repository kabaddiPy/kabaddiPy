---
title: get_season_matches
parent: Overall Functions
nav_order: 2
---
## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## `get_season_matches(self, season="all")`

Retrieve match data for a specific season or all seasons.

This function loads match data from JSON files and returns it as a pandas DataFrame.

#### Parameters

- **season**: `str` or `int`, optional  
  The season number for which to retrieve match data. Use `"all"` to retrieve data for all seasons (default). If a specific season is desired, provide the season number as a string or integer.


#### Returns

- **pandas.DataFrame**  
  A DataFrame containing match details with the following columns:
  - **Season**: The season number
  - **Match_ID**: Unique identifier for the match
  - **Match_Name**: Name of the match event
  - **League_Stage**: Stage of the league (e.g., group stage, playoffs)
  - **Year**: Year of the match
  - **Venue**: Location where the match was played
  - **Match_Outcome**: Outcome of the match
  - **Start_Date**: Start date and time of the match
  - **End_Date**: End date and time of the match
  - **Result**: Result code of the match
  - **Winning Margin**: Margin of victory
  - **team_score_1**: Score of the first team
  - **team_score_2**: Score of the second team
  - **team_name_1**: Name of the first team
  - **team_id_1**: ID of the first team
  - **team_name_2**: Name of the second team
  - **team_id_2**: ID of the second team

#### Notes
  - For `"all"` seasons, it sorts the files based on the season number extracted from the filename.
  - Each row in the returned DataFrame represents a single match.


### Example Usage

```python
    import kabaddiPy

    pkl = kabaddiPy.PKL()

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
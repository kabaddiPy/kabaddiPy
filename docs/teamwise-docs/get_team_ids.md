---
layout: default
title: get_team_ids
parent: Team_Functions
nav_order: 2
---
### `get_team_ids`

Retrieve team IDs and names for a specific season.

This function returns a `DataFrame` containing team IDs and names for the given season.

#### Parameters
{: .no_toc }
- **season**: `int` or `str`  
  The season number for which to retrieve team IDs and names.
{: .no_toc }
#### Returns

- **pandas.DataFrame**  
  A `DataFrame` with columns:
  - `Team_Id`: Unique identifier for the team
  - `Team_Name`: Name of the team




### Example Usage
{: .no_toc }


```python
  team_ids = api.get_team_ids(season=5)
  print("Team-IDs")
  print(team_ids)
```



```python
Team-IDs
    Team_Id             Team_Name
0         4       Bengal Warriorz
1         6         Patna Pirates
2        30            UP Yoddhas
3         1       Bengaluru Bulls
4         8         Telugu Titans
5        29       Tamil Thalaivas
6        31        Gujarat Giants
7         7         Puneri Paltan
8        28      Haryana Steelers
9         5               U Mumba
10        3  Jaipur Pink Panthers
11        2     Dabang Delhi K.C.
```

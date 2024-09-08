---
layout: default
title: get_team_matches
parent: Team Functions
nav_order: 3
---
### `get_team_matches`

Retrieve all matches for a specific team in a given season.

This function filters the season's matches to return only those involving the specified team.

#### Parameters
{: .no_toc }
- **season**: `int` or `str`  
  The season number for which to retrieve matches.

- **team_id**: `str`  
  The unique identifier for the team.

#### Returns
{: .no_toc }
- **pandas.DataFrame**  
  A `DataFrame` containing match details for the specified team, including:
  - `Match_ID`: Unique identifier for the match
  - `Match_Name`: Name of the match event
  - `Start_Date`: Start date and time of the match
  - `Venue`: Location where the match was played
  - `team_name_1`, `team_id_1`: Name and ID of the first team
  - `team_name_2`, `team_id_2`: Name and ID of the second team
  - `team_score_1`, `team_score_2`: Scores of both teams
  - And other relevant match information


```python
  Season Match_ID Match_Name League_Stage  Year  ... team_score_2           team_name_1 team_id_1           team_name_2 team_id_2
4      10     3033    Match 5       League  2023  ...           33         Puneri Paltan         7  Jaipur Pink Panthers         3
9      10     3038   Match 10       League  2023  ...           28       Bengal Warriors         4  Jaipur Pink Panthers         3
17     10     3046   Match 18       League  2023  ...           32  Jaipur Pink Panthers         3        Gujarat Giants        31
21     10     3050   Match 22       League  2023  ...           30       Bengaluru Bulls         1  Jaipur Pink Panthers         3
26     10     3055   Match 27       League  2023  ...           29         Patna Pirates         6  Jaipur Pink Panthers         3

```
### Notes
{: .no_toc }
- The function internally calls `get_season_matches` to fetch all matches for the season.
- Matches are filtered to include only those where the specified `team_id` appears as either `team_id_1` or `team_id_2`.

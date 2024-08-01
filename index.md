---
title: Home
layout: home
---


# Prokabaddi API

## team_season_standings

Returns the latest season standings for Kabaddi teams.

### Parameters:
- `team` (str, optional): The name of a specific team to get data for. Case-insensitive.
- `rank` (int, optional): The rank (1-12) to get the team data for.

### Returns:
- If no parameters are provided: A dictionary containing data for all teams.
- If `team` is provided: A dictionary with the specified team's data.
- If `rank` is provided: A dictionary with the data of the team at the specified rank.
- If both `team` and `rank` are provided: An error message.
- If an invalid team name or rank is provided: An error message.

### Example 1: Get all team standings
```python
response = team_season_standings()




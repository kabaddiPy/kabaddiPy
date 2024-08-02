---
title: Team Functions
layout: default
has_toc: true
has_children: false
nav_order: 2
---
# Team Functions


## Table of Contents
- [Team Functions**](#Team Functions)
  - [get\_all\_team\_names](#get_all_team_names)
  - [get\_all\_team\_url](#get_all_team_url)
  - [get\_all\_player\_team\_url](#get_all_player_team_url)
  - [get\_players\_team\_info\_and\_profile\_url](#get_players_team_info_and_profile_url)
  - [get\_stats\_from\_player\_profile](#get_stats_from_player_profile)
  - [team\_season\_standings](#team_season_standings)
  - [get\_all\_season\_team\_stats](#get_all_season_team_stats)
  - [team\_line\_up](#team_line_up)
  - [team\_level\_stats](#team_level_stats)
  - [player\_performance](#player_performance)
- [Player Functions](#player_docs/index.md)


---


## get_all_team_names

Retrieves the names of all teams in the Pro Kabaddi League.

### Usage

```python
aggregator = KabaddiDataAggregator()
team_names = aggregator.get_all_team_names()
```

### Returns

- `List[str]`: A list of team names.

---

## get_all_team_url

Retrieves the URLs for all team pages on the Pro Kabaddi website.

### Usage

```python
aggregator = KabaddiDataAggregator()
team_urls = aggregator.get_all_team_url()
```

### Returns

- `List[str]`: A list of URLs for team pages.

---

## team_season_standings

Retrieves the current season standings for teams in the Pro Kabaddi League.

### Usage

```python
aggregator = KabaddiDataAggregator()
standings = aggregator.team_season_standings(team=None, rank=None)
```

### Parameters

- `team` (str, optional): The name of a specific team to get data for. Case-insensitive.
- `rank` (int, optional): The rank (1-12) to get the team data for.

### Returns

- If no parameters are provided: `List[Dict[str, Union[str, int]]]`: A list of dictionaries containing standings for all teams.
- If `team` is provided: `Dict[str, Union[str, int]]`: A dictionary containing standings for the specified team.
- If `rank` is provided: `Dict[str, Union[str, int]]`: A dictionary containing standings for the team at the specified rank.

Each dictionary contains:
- `TeamName`: Name of the team
- `play`: Number of matches played
- `won`: Number of matches won
- `lost`: Number of matches lost
- `draw`: Number of matches drawn
- `points`: Total points

---

## get_all_season_team_stats

Retrieves all season statistics for a specific team.

### Usage

```python
aggregator = KabaddiDataAggregator()
team_stats = aggregator.get_all_season_team_stats(url)
```

### Parameters

- `url` (str): The URL of the team's statistics page.

### Returns

- `Dict`: A dictionary containing various team statistics for the season. The structure depends on the data available on the page.

---

## team_line_up

Retrieves team line-up data from a Tableau dashboard.

### Usage

```python
aggregator = KabaddiDataAggregator()
line_up_data = aggregator.team_line_up()
```

### Returns

- `List`: A list containing team line-up data extracted from the Tableau dashboard. The structure depends on the data available in the dashboard.

---

## team_level_stats

Retrieves team-level statistics from a Tableau dashboard.

### Usage

```python
aggregator = KabaddiDataAggregator()
team_stats = aggregator.team_level_stats()
```

### Returns

- `List`: A list containing team-level statistics extracted from the Tableau dashboard. The structure depends on the data available in the dashboard.

---
## team_season_standings

Retrieves the current season standings for teams in the Pro Kabaddi League.

### Usage

```python
aggregator = KabaddiDataAggregator()
standings = aggregator.team_season_standings(team=None, rank=None)
```

### Parameters

- `team` (str, optional): The name of a specific team to get data for. Case-insensitive.
- `rank` (int, optional): The rank (1-12) to get the team data for.

### Returns

- If no parameters are provided: `List[Dict[str, Union[str, int]]]`: A list of dictionaries containing standings for all teams.
- If `team` is provided: `Dict[str, Union[str, int]]`: A dictionary containing standings for the specified team.
- If `rank` is provided: `Dict[str, Union[str, int]]`: A dictionary containing standings for the team at the specified rank.

Each dictionary contains:
- `TeamName`: Name of the team
- `play`: Number of matches played
- `won`: Number of matches won
- `lost`: Number of matches lost
- `draw`: Number of matches drawn
- `points`: Total points

---

## get_all_season_team_stats

Retrieves all season statistics for a specific team.

### Usage

```python
aggregator = KabaddiDataAggregator()
team_stats = aggregator.get_all_season_team_stats(url)
```

### Parameters

- `url` (str): The URL of the team's statistics page.

### Returns

- `Dict`: A dictionary containing various team statistics for the season. The structure depends on the data available on the page.

---

## team_level_stats

Retrieves statistics for all teams for a specified season or all seasons.

### Usage

```python
aggregator = KabaddiDataAggregator()
team_stats = aggregator.team_level_stats(season=4)
```
### Parameters
- `season`: The season to get details of. Defaults to all.
### Returns

- `List`: A list containing team-level statistics extracted from the Tableau dashboard. The structure depends on the data available in the dashboard.


## team_line_up

Retrieves team line-up data from a Tableau dashboard.

### Usage

```python
aggregator = KabaddiDataAggregator()
line_up_data = aggregator.team_line_up()
```

### Returns

- `List`: A list containing team line-up data extracted from the Tableau dashboard. The structure depends on the data available in the dashboard.

---
**Note**: The functions that interact with constantly updating dashboards (`team_line_up` and `team_level_stats`) may return complex data structures. The exact format of the returned data depends on the structure and content  at the time of extraction.

---
title: ProKabaddi API Docs
layout: default
has_toc=false
---


# Prokabaddi API

This documentation covers the main functions of the `KabaddiDataAggregator` class that return useful data for Kabaddi statistics and information.

This is an update.

## Table of Contents

- [Prokabaddi API](#prokabaddi-api)
  - [Table of Contents](#table-of-contents)
  - [get\_all\_team\_names](#get_all_team_names)
    - [Usage](#usage)
    - [Returns](#returns)
  - [get\_all\_team\_url](#get_all_team_url)
    - [Usage](#usage-1)
    - [Returns](#returns-1)
  - [get\_all\_player\_team\_url](#get_all_player_team_url)
    - [Usage](#usage-2)
    - [Returns](#returns-2)
  - [get\_players\_team\_info\_and\_profile\_url](#get_players_team_info_and_profile_url)
    - [Usage](#usage-3)
    - [Returns](#returns-3)
  - [get\_stats\_from\_player\_profile](#get_stats_from_player_profile)
    - [Usage](#usage-4)
    - [Parameters](#parameters)
    - [Returns](#returns-4)
  - [team\_season\_standings](#team_season_standings)
    - [Usage](#usage-5)
    - [Parameters](#parameters-1)
    - [Returns](#returns-5)
  - [get\_all\_season\_team\_stats](#get_all_season_team_stats)
    - [Usage](#usage-6)
    - [Parameters](#parameters-2)
    - [Returns](#returns-6)
  - [team\_line\_up](#team_line_up)
    - [Usage](#usage-7)
    - [Returns](#returns-7)
  - [team\_level\_stats](#team_level_stats)
    - [Usage](#usage-8)
    - [Returns](#returns-8)
  - [player\_performance](#player_performance)
    - [Usage](#usage-9)
    - [Returns](#returns-9)

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

## get_all_player_team_url

Retrieves the URLs for all player team pages on the Pro Kabaddi website.

### Usage

```python
aggregator = KabaddiDataAggregator()
player_team_urls = aggregator.get_all_player_team_url()
```

### Returns

- `List[str]`: A list of URLs for player team pages.

---

## get_players_team_info_and_profile_url

Retrieves information about players, including their names, profile URLs, and team URLs.

### Usage

```python
aggregator = KabaddiDataAggregator()
players_info = aggregator.get_players_team_info_and_profile_url()
```

### Returns

- `List[Dict[str, str]]`: A list of dictionaries, each containing:
  - `name`: Player's name
  - `profileURL`: URL of the player's profile page
  - `teamURL`: URL of the player's team page

---

## get_stats_from_player_profile

Retrieves statistics from a player's profile page.

### Usage

```python
aggregator = KabaddiDataAggregator()
player_stats = aggregator.get_stats_from_player_profile(profile_url)
```

### Parameters

- `profile_url` (str): The URL of the player's profile page.

### Returns

- `Dict[str, str]`: A dictionary containing:
  - Two key-value pairs for player statistics (keys and values depend on the available data)
  - `teamName`: The name of the player's team

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

## player_performance

Retrieves player performance data from a Tableau dashboard.

### Usage

```python
aggregator = KabaddiDataAggregator()
player_performance_data = aggregator.player_performance()
```

### Returns

- `List`: A list containing player performance data extracted from the Tableau dashboard. The structure depends on the data available in the dashboard.

---

**Note**: The functions that interact with Tableau dashboards (`team_line_up`, `team_level_stats`, and `player_performance`) may return complex data structures. The exact format of the returned data depends on the structure and content of the Tableau dashboards at the time of extraction.



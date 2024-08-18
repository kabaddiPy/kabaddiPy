---
title: Player Functions
layout: default
has_toc: true
has_children: false
nav_order: 3
---
# Player Functions


## Table of Contents
- [Player Functions](#player-functions)
  - [Table of Contents](#table-of-contents)
  - [get\_stats\_from\_player\_profile](#get_stats_from_player_profile)
    - [Usage](#usage)
    - [Parameters](#parameters)
    - [Returns](#returns)
  - [player\_performance](#player_performance)
    - [Usage](#usage-1)
    - [Returns](#returns-1)
  - [get\_all\_player\_team\_url](#get_all_player_team_url)
    - [Usage](#usage-2)
    - [Returns](#returns-2)
  - [get\_players\_team\_info\_and\_profile\_url](#get_players_team_info_and_profile_url)
    - [Usage](#usage-3)
    - [Returns](#returns-3)
  - [player\_performance](#player_performance-1)
    - [Usage](#usage-4)
    - [Returns](#returns-4)


### Usage

```python
aggregator = KabaddiDataAggregator()
player_stats = aggregator.get_stats_from_player_profile(profile_name)
```

### Parameters

- `profile_name` (str): The player's name.

### Returns

- `Dict[str, str]`: A dictionary containing:
  - Two key-value pairs for player statistics (keys and values depend on the available data)
  - `teamName`: The name of the player's team

---

## get_player_details



## player_performance

Retrieves player performance data from all seasons or particular seasons.

### Usage

```python
aggregator = KabaddiDataAggregator()
player_performance_data = aggregator.player_performance()
```
### Returns

- `List`: A list containing player performance data extracted from the Tableau dashboard. The structure depends on the data available in the dashboard.

---






## player_performance

Retrieves player performance data.

### Usage

```python
aggregator = KabaddiDataAggregator()
player_performance_data = aggregator.player_performance()
```

### Returns

- `List`: A list containing player performance data extracted from the Tableau dashboard. The structure depends on the data available in the dashboard.
  
---

**Note**: The functions that interact with constantly updating dashboards (`team_line_up`, `team_level_stats`, and `player_performance`) may return complex data structures. The exact format of the returned data depends on the structure and content of the Tableau dashboards at the time of extraction.

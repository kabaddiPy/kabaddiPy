---
layout: default
title: get_player_info
parent: Player Functions
nav_order: 2
---
## `get_player_info(player_id, season=None)`

Retrieve comprehensive player information for a specific season.

### Parameters:
{: .no_toc }

- `player_id` (int): The unique identifier for the player.
- `season` (int, optional): The season number for which to retrieve data. If not specified, the latest season available will be used.

### Returns:
{: .no_toc }

A tuple containing three DataFrames, each transposed for easier reading: `player_stats_df_rank`, `player_stats_df_value` and `player_stats_df_per_match`,

### Usage
{: .no_toc}

```python
stats_rank, stats_value, stats_per_match = pkl.get_player_info(player_id=142,season=9)
print(stats_rank)

season	                        9
player_id	                142
player_name	                Sandeep Narwal
player_matches_played	        7
player_position_id	        0
player_position_name	        All Rounder
team_id	                        30
team_full_name	                U.P. Yoddhas
player-super-tackles_rank	76.0
player-raid-points_rank	        70.0
player-super-raids_rank	        NaN
player-high-5s_rank	        33.0
player-tackle-points_rank	69.0
#
#...with 5 more rows for 'player-avg-tackle-points_rank	','player-dod-raid-points_rank',
#   'player-total-points_rank','player-successful-tackles_rank','player-successful-raids_rank' 
#   and 'super-10s_rank'

print(stats_value)
season	                    9
player_id	            142
player_name	            Sandeep Narwal
player_matches_played	    7
player_position_id	    0
player_position_name	    All Rounder
team_id	                    30
team_full_name	            U.P. Yoddhas
player-super-tackles_value  1.0
player-raid-points_value    10.0
player-super-raids_value    NaN
player-high-5s_value        1.0
#
#...with 15 more rows for player-tackle-points_value,'player-avg-tackle-points_value'
#   'player-dod-raid-points_value', 'player-total-points_value','player-successful-tackles_value'
#   'player-successful-raids_value', 'super-10s_value','Total Tackles','Successful Tackles'
#   'Defender Success Rate','Total Raids','Successful Raids', 'Raider Success Rate', 'Total Played'
#    and 'Total Starts'

print(stats_per_match)

season                                9
player_id                             142
player_name                           Sandeep Narwal
player_matches_played                 7
player_position_id                    0
player_position_name                  All Rounder
team_id                               30
team_full_name                        U.P. Yoddhas
player-super-tackles_points_per_match  0.14
player-raid-points_points_per_match    1.43
player-super-raids_points_per_match    NaN
high-5s_points_per_match               0.14
player-tackle-points_points_per_match  1.71
#
#...with 5 more rows 'player-dod-raid-points_points_per_match', 'player-total-points_points_per_match'  
#   'player-successful-tackles_points_per_match','player-successful-raids_points_per_match'  
#   and 'super-10s_points_per_match'


```

### Notes:
{: .no_toc }
- The function aggregates data from various sources including CSV files on player statistics, raider vs. defender data, defender success rates, raider success rates, and lineup information.
- If data is unavailable for the specified player or season, appropriate warning messages are printed.
- Handles data type conversions and missing value imputations for consistency.

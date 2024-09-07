---
title: Player Functions
layout: default
has_toc: true
has_children: false
nav_order: 4
---

# Player Functions

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


---

## `get_matchwise_player_info(player_id, season)`

Extract detailed player statistics from all matches in a given season.

### Parameters:
{: .no_toc }
- `player_id` (int): The ID of the player.
- `season` (int): The season number.

### Returns:
{: .no_toc }
A DataFrame containing detailed player statistics for each match for the specified player.
  
### Usage
{: .no_toc }

```python
player_stats = pkl.get_matchwise_player_info(142,9)

print(player_stats)

match_id	date	team_name	team_score	opponent_name	opponent_score	played
0	3020	12/9/2022	U.P. Yoddhas	45	Puneri Paltan	41	        True
1	3003	12/2/2022	U.P. Yoddhas	38	U Mumba	        28	        True
2	3025	12/13/2022	U.P. Yoddhas	36	Tamil Thalaivas	36	        True
3	2997	11/28/2022	U.P. Yoddhas	33	Bengal Warriors	32	        True
4	2994	11/26/2022	U.P. Yoddhas	35	Patna Pirates	33	        True
5	3016	12/7/2022	U.P. Yoddhas	28	Tamil Thalaivas	43	        True
6	3010	12/4/2022	U.P. Yoddhas	35	Bengaluru Bulls	38	        True
#
#...with 26 more columns ['starter', 'on_court', 'captain', 'total_points', 'raid_points',
#   'tackle_points', 'raids_total', 'raids_successful', 'raids_unsuccessful', 'raids_empty',
#   'super_raids', 'tackles_total', 'tackles_successful', 'tackles_unsuccessful', 'super_tackles',
#   'green_card_count', 'yellow_card_count', 'red_card_count', 'top_raider', 'top_defender',
#   'substitutions', 'first_substitution_time',  'matches_played', 'matches_started',  
#   'average_points_full_season' and   'total_substitutions_full_season'    
```
### Notes:
{: .no_toc }
- The function processes all JSON match files for the specified season and extracts detailed player statistics.
- If no data is found for the specified player or season, an empty DataFrame is returned.
- Includes additional calculated statistics such as the number of matches played, matches started, average points for the season, and total substitutions.


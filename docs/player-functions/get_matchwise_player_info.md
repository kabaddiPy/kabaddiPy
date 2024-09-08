---
layout: default
title: get_matchwise_player_info
parent: Player Functions
nav_order: 1
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

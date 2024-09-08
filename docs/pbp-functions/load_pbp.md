---
layout: default
title: load_pbp
parent: Match Functions
nav_order: 1
---

## `load_pbp(season, match_id)`

Load the play-by-play (PBP) data for a specific match in a given season.

### Parameters:
{: .no_toc }

- `season` (int): The season number.
- `match_id` (str): The unique identifier for the match.

### Returns:
{: .no_toc }

- `DataFrame`: A DataFrame containing the play-by-play events of the match. Returns `None` if the match was not found for a season.

### Usage
{: .no_toc }

```python
event_no event_half	 event	event_id	event_text	            raider_id	raiding_team_id
1	    1	Successful Raid	    1	Arjun Deshwal raids successfully    2024.0	3.0
2	    1	Unsuccessful Raid   2	Surender Gill unsuccessful raid	    3241.0	30.0
3	    1	Unsuccessful Raid   2	Arjun Deshwal unsuccessful raid	    2024.0	3.0
4	    1	Successful Raid	    1	Pardeep Narwal raids successfully   197.0	30.0
5	    1	Empty Raid	    3	V Ajith Kumar empty raid	    3053.0	3.0
6	    1	Empty Raid	    3	Pardeep Narwal empty raid	    197.0	30.0
7	    1	Unsuccessful Raid   2	V Ajith Kumar unsuccessful raid	    3053.0	3.0
8	    1	Empty Raid	    3	Surender Gill empty raid	    3241.0	30.0
9	    1	Empty Raid	    3  	Sunil Kumar empty raid	            368.0	3.0
10	    1	Unsuccessful Raid   2	Pardeep Narwal unsuccessful raid    197.0	30.0
#
#...with 95 more rows and 28 more columns: ['defender_id', 'defending_team_id', 'raid_points', 
#   'raid_touch_points','raid_bonus_points', 'raid_technical_points', 'raid_all_out_points',
#   'defending_capture_points', 'defending_bonus_points','defending_technical_points',
#   'defending_all_out_points', 'super_raid','super_tackle', 'do_or_die', 'super_ten',
#   'high_five', 'review','defending_points', 'clock', 'status_id','score', 'seq_no',
#   'defenders', 'created_date', 'player_id', 'substituted_by', 'team_id' and 'substitute_time'
```
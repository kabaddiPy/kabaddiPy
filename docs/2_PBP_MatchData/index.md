---
title: Play-by-Play Data
layout: default
has_toc: true
has_children: false
nav_order: 5
---

#### Table of contents

{: .no_toc .text-delta }

1. TOC
{:toc}


## `load_match_details(season, match_id)`

Load and process match details for a specific season and match ID.

##### Parameters:
{: .no_toc }

- `season` (int): The season number.
- `match_id` (str): The unique identifier for the match.

##### Returns:
{: .no_toc }

A tuple containing six DataFrames: `match_detail_df`, `events_df`, `zones_df`, `team1_df`, `team2_df` and `breakdown_df`

##### Examples
{: .no_toc }

```python
match_detail_df,events_df,zones_df,team1_df,team2_df,breakdown_df = pkl.load_match_details(season=9,
                                                                                      match_id='2895')
print(match_detail_df)
 match_id match_number  clock_minutes  clock_seconds       date  start_time         matchtime_iso
0      2895      Match 4             39             57  10/8/2022      19:30  2022-10-08T14:00:00Z
#
#...with 16 more columns: 'gmtoffset', 'result_value', 'result_winning_method', 'result_winning_team',
#   'result_winning_team_id', 'player_of_the_match', 'series_id', 'series_parent_series_name', 'status', 
#   'toss_winner', 'toss_selection', 'win_by_coin_toss_winner', 'venue_id', 'venue_name', 'stage',
#   and 'group'. 

print(events_df)
event_no event_half	event	     event_id	event_text	                   raider_id	raiding_team_id
1	    1	    Successful Raid	    1	Aslam Inamdar raids successfully	4960.0	7.0
2	    1	    Empty Raid	            3	Sachin empty raid	                757.0	6.0
3	    1	    Successful Raid	    1	Mohit Goyat raids successfully	        4022.0	7.0
4	    1	    Successful Raid	    1	Vishwas S raids successfully	        4757.0	6.0
5	    1	    Successful Raid	    1	Akash Shinde raids successfully	        4959.0	7.0
6	    1	    Empty Raid	            3	Sachin empty raid	                757.0	6.0
7	    1	    Empty Raid	            3	Mohit Goyat empty raid	                4022.0	7.0
8	    1	    Unsuccessful Raid	    2	Vishwas S unsuccessful raid	        4757.0	6.0
9	    1	    Unsuccessful Raid	    2	Aslam Inamdar unsuccessful raid	        4960.0	7.0
10	    1	    Successful Raid	    1	Sachin raids successfully	         757.0	6.0
#
#...with 87 more rows and 28 more columns: ['defender_id', 'defending_team_id', 'raid_points', 
#   'raid_touch_points','raid_bonus_points', 'raid_technical_points', 'raid_all_out_points',
#   'defending_capture_points', 'defending_bonus_points','defending_technical_points',
#   'defending_all_out_points', 'super_raid','super_tackle', 'do_or_die', 'super_ten',
#   'high_five', 'review','defending_points', 'clock', 'status_id','score', 'seq_no',
#   'defenders', 'created_date', 'player_id', 'substituted_by', 'team_id' and 'substitute_time'

print(team1_df)
team_id	team_name	  team_score	id	name	      jersey	played	captain	on_court starter
6	    Patna Pirates	34.0	757	Sachin	        99	True	False	True	  True
NaN	    NaN	                NaN	3107	Neeraj Kumar    5	True	True	True   	  True
NaN	    NaN	                NaN	3343	Sajin C	        11	True	False	True	  True
NaN	    NaN	                NaN	3023	Rohit Gulia	7	True	False	True	  True
NaN	    NaN	                NaN	4757	Vishwas S	22	True	False	True	  True
#
#...with 10 more rows and 37 columns: ['red_card', 'yellow_card', 'green_card', 'red_card_count',
#       'yellow_card_count', 'green_card_count', 'top_raider', 'top_defender',
#       'total_points', 'raid_points', 'tackle_points', 'raids_total',
#       'raids_successful', 'tackles_total', 'tackles_successful',
#       'strong_zones_zone_1', 'strong_zones_zone_2', 'strong_zones_zone_3',
#       'strong_zones_zone_4', 'strong_zones_zone_5', 'strong_zones_zone_6',
#       'strong_zones_zone_7', 'strong_zones_zone_8', 'strong_zones_zone_9',
#       'strong_zones_zone_10', 'strong_zones_zone_11', 'weak_zones_zone_1',
#       'weak_zones_zone_2', 'weak_zones_zone_3', 'weak_zones_zone_4',
#       'weak_zones_zone_5', 'weak_zones_zone_6', 'weak_zones_zone_7',
#       'weak_zones_zone_8', 'weak_zones_zone_9', 'weak_zones_zone_10',
#       'weak_zones_zone_11'

print(breakdown_df)
    team_id	team_name	raids_total	raids_successful	raids_unsuccessful	
0	6	Patna Pirates	42	        13	                8	
1	7	Puneri Paltan	43	        18	                11	
#
#...with 13 more columns ['raids_empty', 'tackles_total', 'tackles_successful',
#       'tackles_unsuccessful', 'points_total', 'points_raid', 'points_tackle',
#       'points_all_out', 'points_extras', 'raid_success_rate',
#       'tackle_success_rate', 'longest_streak' and 'streak_percent'

print(zones_df)
        id	name
0	1	Left Lobby
1	2	Right Lobby
2	3	Midline Left
3	4	Midline Centre
4	5	Midline Right
5	6	Baulk Left
6	7	Baulk Centre
7	8	Baulk Right
8	9	Bonus Left
9	10	Bonus Centre
10	11	Bonus Right
```



### Notes:
{: .no_toc }

- If an error occurs during data loading or processing, the function will print an error message and return `None` for all DataFrames.
- The function retrieves the match data from a JSON file and processes it to extract relevant match information.
- In season 4 or if breakdown data is unavailable, an empty `breakdown_df` will be returned.

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
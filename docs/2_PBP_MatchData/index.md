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
- `season` (int): The season number.
- `match_id` (str): The unique identifier for the match.

##### Returns:
A tuple containing six DataFrames: `match_detail_df`, `events_df`, `zones_df`, `team1_df`, `team2_df` and `breakdown_df`

##### Examples
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
```



### Notes:
- If an error occurs during data loading or processing, the function will print an error message and return `None` for all DataFrames.
- The function retrieves the match data from a JSON file and processes it to extract relevant match information.
- In season 4 or if breakdown data is unavailable, an empty `breakdown_df` will be returned.

---

## `load_pbp(season, match_id)`

Load the play-by-play (PBP) data for a specific match in a given season.

### Parameters:
- `season` (int): The season number.
- `match_id` (str): The unique identifier for the match.

### Returns:
- `DataFrame`: A DataFrame containing the play-by-play events of the match. Returns `None` if there was an error loading the match details.

### Notes:
- This function calls `load_match_details` to retrieve the full match data and extracts only the `events_df` (play-by-play data).
- Other match-related information (e.g., team details, zones) is discarded.

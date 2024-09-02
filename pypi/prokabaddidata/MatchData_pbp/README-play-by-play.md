# Methods

### get_match_data(season: str, match_id: str)

Get the full data for a specific match.

**Parameters:**
- `season (str)`: The season name.
- `match_id (str)`: The match ID.

**Returns:**
- `Tuple[DataFrame, DataFrame, DataFrame, DataFrame, DataFrame, DataFrame]`: A tuple containing match detail, teams, events, zones, team1, and team2 DataFrames.

### get_match_events(season: str, match_id: str)

Get all events for a specific match.

**Parameters:**
- `season (str)`: The season name.
- `match_id (str)`: The match ID.

**Returns:**
- `DataFrame`: A DataFrame containing all events in the match.


## Helper functions
### get_available_seasons()

Get a list of available seasons in the dataset.

**Returns:**
- `List[str]`: A list of season names.

### get_matches_for_season(season: str)

Get a list of match IDs for a specific season.

**Parameters:**
- `season (str)`: The season name.

**Returns:**
- `List[str]`: A list of match IDs.


## Example Usage

```python
# Initialize the class
api = KabaddiDataAPI(r"..\1_DATA\MatchWise-Data\Organised_MatchData_pbp")

match_detail_df, teams_df, events_df, zones_df, team1_df, team2_df = api.get_match_data('Season_Pro Kabaddi League Season 7, 2019', '1690')
print(match_detail_df)
```
Output:
```python
print(match_detail_df)
#printing the match details dataframe
   match_id match_number  clock_minutes  clock_seconds       date  ...   stage toss_winner          toss_selection venue_id                            venue_name
0      1690      Match 6             11             52  7/22/2019  ...  League           7  Choice of court :Right        9  Gachibowli Indoor Stadium, Hyderabad

[1 rows x 27 columns]
27 columns include ['match_id', 'match_number', 'clock_minutes', 'clock_seconds', 'date', 'start_time', 'matchtime_iso', 'gmtoffset', 'result_outcome',
'result_value', 'result_winning_method', 'result_winning_team', 'result_winning_team_id', 'player_of_the_match_id','player_of_the_match_value', 'series_id',
'series_name', 'series_short_name', 'series_parent_series_id', 'series_parent_series_name', 'status_id', 'status', 'stage','toss_winner', 'toss_selection',
'venue_id', 'venue_name'],


print(teams_df)
#returns comparison of two teams in the match
   id              name  ...                                              stats                                      state_of_play
0   7     Puneri Paltan  ...  {'points': {'total': 24, 'all_out': 0, 'extras...  {'is_raiding_now': False, 'players_on_court': ...
1  28  Haryana Steelers  ...  {'points': {'total': 34, 'all_out': 4, 'extras...  {'is_raiding_now': True, 'players_on_court': 4...

[2 rows x 7 columns]
Index(['id', 'name', 'score', 'short_name', 'squad', 'stats', 'state_of_play'],

print(events_df)
#returns the play-py-play events of the match
    event_no              event  event_id                      event_text  raider_id  ...     score  defenders  team_id  player_id  substituted_by
0          1         Empty Raid         3               Naveen Empty Raid     2357.0  ...    [0, 0]         []      NaN        NaN             NaN
1          2         Empty Raid         3              Manjeet Empty Raid      763.0  ...    [0, 0]         []      NaN        NaN             NaN
2          3  Unsuccessful Raid         2         Vinay Unsuccessful Raid     2488.0  ...    [1, 0]     [2291]      NaN        NaN             NaN
3          4  Unsuccessful Raid         2   Pawan Kumar Unsuccessful Raid      156.0  ...    [1, 1]     [2463]      NaN        NaN             NaN
4          5         Empty Raid         3               Naveen Empty Raid     2357.0  ...    [1, 1]         []      NaN        NaN             NaN
..       ...                ...       ...                             ...        ...  ...       ...        ...      ...        ...             ...
87        88       Substitution         5  Ravi Kumar comes in for Naveen        NaN  ...       NaN        NaN     28.0     2357.0           240.0
88        89  Unsuccessful Raid         2       Manjeet Unsuccessful Raid      763.0  ...  [24, 33]     [2463]      NaN        NaN             NaN
89        90       Substitution         5  Naveen comes in for Ravi Kumar        NaN  ...       NaN        NaN     28.0      240.0          2357.0
90        91    Successful Raid         1       Naveen raids successfully     2357.0  ...  [24, 34]      [322]      NaN        NaN             NaN
91        92         Empty Raid         3          Pawan Kumar Empty Raid      156.0  ...  [24, 34]         []      NaN        NaN             NaN

[92 rows x 29 columns]
29 columns include: ['event_no', 'event', 'event_id', 'event_text', 'raider_id', 'raiding_team_id', 'defender_id', 'defending_team_id', 'raid_points',
'raid_touch_points','raid_bonus_points', 'raid_technical_points', 'raid_all_out_points', 'defending_capture_points','defending_bonus_points',
'defending_technical_points','defending_all_out_points', 'defending_points', 'super_raid','super_tackle', 'clock', 'status_id', 'do_or_die', 'review',
'score','defenders','team_id', 'player_id', 'substituted_by']


print(zones_df)
#all the zones in the match
    id            name
0    1      Left Lobby
1    2     Right Lobby
2    3    Midline Left
3    4  Midline Centre
4    5   Midline Right
5    6      Baulk Left
6    7    Baulk Centre
7    8     Baulk Right
8    9      Bonus Left
9   10    Bonus Centre
10  11     Bonus Right

[11 rows x 2 columns]

print(team1_df)
#the team info for the first team

      id                      name  jersey  played  captain  on_court  ...  weak_zones_zone_10  weak_zones_zone_11  team_id      team_name  team_score  team_short_name
0    763                   Manjeet       3    True    False     False  ...                   0                   2        7  Puneri Paltan          24              PUN       
1    322             Surjeet Singh       6    True     True     False  ...                   0                   0        7  Puneri Paltan          24              PUN       
2    161       Girish Maruti Ernak       8    True    False      True  ...                   0                   0        7  Puneri Paltan          24              PUN       
3   2479            Shubham Shinde       9    True    False      True  ...                   0                   0        7  Puneri Paltan          24              PUN       
4    156               Pawan Kumar      12    True    False      True  ...                   0                   0        7  Puneri Paltan          24              PUN       
5    694              Deepak Yadav      33    True    False     False  ...                   0                   0        7  Puneri Paltan          24              PUN       
6   2291                Amit Kumar      77    True    False     False  ...                   0                   0        7  Puneri Paltan          24              PUN       
7    347             Sagar Krishna       1   False    False     False  ...                   0                   0        7  Puneri Paltan          24              PUN       
8    301                Hadi Tajik       4   False    False     False  ...                   0                   0        7  Puneri Paltan          24              PUN       
9   2492  Jadhav Balasaheb Shahaji       5    True    False      True  ...                   0                   0        7  Puneri Paltan          24              PUN       
10   718                 R. Sriram      18   False    False     False  ...                   0                   0        7  Puneri Paltan          24              PUN       
11   324            Darshan Kadian      88    True    False      True  ...                   0                   0        7  Puneri Paltan          24              PUN       

[12 rows x 48 columns]
48 columns are: (['id', 'name', 'jersey', 'played', 'captain', 'on_court', 'starter', 'red_card', 'yellow_card', 'green_card', 'red_card_count',
       'yellow_card_count', 'green_card_count', 'top_raider', 'top_defender','total_points', 'raid_points', 'tackle_points', 'raids_total',
       'raids_successful', 'tackles_total', 'tackles_successful','strong_zones_zone_1', 'strong_zones_zone_2', 'strong_zones_zone_3',
       'strong_zones_zone_4', 'strong_zones_zone_5', 'strong_zones_zone_6','strong_zones_zone_7', 'strong_zones_zone_8', 'strong_zones_zone_9',
       'strong_zones_zone_10', 'strong_zones_zone_11', 'weak_zones_zone_1','weak_zones_zone_2', 'weak_zones_zone_3', 'weak_zones_zone_4',
       'weak_zones_zone_5', 'weak_zones_zone_6', 'weak_zones_zone_7','weak_zones_zone_8', 'weak_zones_zone_9', 'weak_zones_zone_10',
       'weak_zones_zone_11', 'team_id', 'team_name', 'team_score','team_short_name']

print(team2_df)
#similar structure of output as above
```


## Get match events for a specific match
```python
match_id = '60'
season = '1'
match_events = api.get_match_events(season, match_id)
print(f"Events in match {match_id}:")
print(match_events)
```
Output : 
```python
    event_no              event  event_id                        event_text  raider_id  raiding_team_id  ...     score  defenders  reason  player_id  team_id  substituted_by
0          1         Empty Raid         3            Rohit Kumar Empty Raid      326.0              1.0  ...    [0, 0]         []     NaN        NaN      NaN             NaN 
1          2    Successful Raid         1  Sachin Tanwar raids successfully      757.0             31.0  ...    [0, 1]      [318]     NaN        NaN      NaN             NaN 
2          3         Empty Raid         3            Rohit Kumar Empty Raid      326.0              1.0  ...    [0, 1]         []     NaN        NaN      NaN             NaN 
3          4         Empty Raid         3            Rohit Gulia Empty Raid      686.0             31.0  ...    [0, 1]         []     NaN        NaN      NaN             NaN 
4          5  Unsuccessful Raid         2     Sumit Singh Unsuccessful Raid      363.0              1.0  ...    [0, 2]      [772]     NaN        NaN      NaN             NaN 
..       ...                ...       ...                               ...        ...              ...  ...       ...        ...     ...        ...      ...             ... 
85        86  Unsuccessful Raid         2     Vinod Kumar Unsuccessful Raid      764.0             31.0  ...  [23, 42]         []     NaN        NaN      NaN             NaN 
86        87    Successful Raid         1    Rohit Kumar raids successfully      326.0              1.0  ...  [24, 42]      [357]     NaN        NaN      NaN             NaN 
87        88         Empty Raid         3                More GB Empty Raid      772.0             31.0  ...  [24, 42]         []     NaN        NaN      NaN             NaN 
88        89         Empty Raid         3         Mahender Singh Empty Raid      769.0              1.0  ...  [24, 42]         []     NaN        NaN      NaN             NaN 
89        90         Empty Raid         3                More GB Empty Raid      772.0             31.0  ...  [24, 42]         []     NaN        NaN      NaN             NaN 

[90 rows x 30 columns]
30 columns include: ['event_no', 'event', 'event_id', 'event_text', 'raider_id', 'raiding_team_id', 'defender_id', 'defending_team_id', 'raid_points','raid_touch_points',
                     'raid_bonus_points', 'raid_technical_points','raid_all_out_points', 'defending_capture_points','defending_bonus_points', 'defending_technical_points',
                     'defending_all_out_points', 'defending_points', 'super_raid', 'super_tackle', 'clock', 'status_id', 'do_or_die', 'review', 'score','defenders',
                     'reason', 'player_id', 'team_id', 'substituted_by']

```




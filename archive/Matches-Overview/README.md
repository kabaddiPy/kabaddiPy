## Matches Overview

This folder contains the code and data for fetching and processing match data from Pro Kabaddi League.

### Files

1. `_match-data.py`
   - This file contains the code to fetch match data for a given match ID and season.


### Example Usage

```python
from _match-data import get_match_overview

match_id = "183"
season = "Pro Kabaddi League Season 4, 2016"

match_overview = get_match_overview(match_id, season)
print(match_overview)
```

This will fetch the match data for the given match ID and season and print it.

Output:
```
General Details:
  match_id event_name                          tour_name result_code season_id  ... venue_id event_status                           event_sub_status winning_margin event_stage
0      183    Match 2  Pro Kabaddi League Season 4, 2016           W         4  ...        5    Completed  U Mumba beat Jaipur Pink Panthers (36-34)              2      League

[1 rows x 13 columns]



Participants:
               team_name team_id       player_name player_id player_points player_type
0                U Mumba       5      Rakesh Kumar        88            12      Raider
1                U Mumba       5  Rishank Devadiga        94             5            
2                U Mumba       5             Sunil       207             2            
3                U Mumba       5     Surjeet Singh       322             2            
4                U Mumba       5        Anup Kumar        29             2            
5                U Mumba       5   Gurvinder Singh        46             1            
6                U Mumba       5       Jeeva Kumar        54             1            
7                U Mumba       5       Manoj Dhull       233             0            
8                U Mumba       5    Surender Singh       234             0            
9   Jaipur Pink Panthers       3     Shabeer Bappu       105             9            
10  Jaipur Pink Panthers       3         Ran Singh       160             4            
11  Jaipur Pink Panthers       3        Ajay Kumar       389             3            
12  Jaipur Pink Panthers       3        Amit Hooda       212             3            
13  Jaipur Pink Panthers       3      Tushar Patil       242             2            
14  Jaipur Pink Panthers       3     Rajesh Narwal        86             2            
15  Jaipur Pink Panthers       3      Jasvir Singh        52             2            
16  Jaipur Pink Panthers       3     Jawahar Dagar       390             1            

```



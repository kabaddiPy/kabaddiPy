# Functions



## Match Data Functions

This file contains functions for loading and querying Pro Kabaddi League match data.

### Functions

1. `get_match_overview(folder_path, match_id, season)`:
2. 
   - Retrieves detailed information about a specific match.
   - Parameters:
     - `folder_path`: Path to the directory containing match data JSON files.
     - `match_id`: Unique identifier for the match.
     - `season`: Season name of the Pro Kabaddi League.
   - Returns two pandas DataFrames:
     - `general_df`: Contains general match details (tour name, series ID, dates, venue, status, winning margin).
     - `participants_df`: Contains information about participating teams and players.

### Example Usage

The file demonstrates how to use the `get_match_overview` function:

```python
general_df, participants_df = get_match_overview("../1_DATA/MatchWise-Data/ Matches-Overview", 
                                                "60", 
"Pro Kabaddi League Season 1, 2014")

print("General Details:")
print(general_df)

print("\n\nParticipants:")
print(participants_df)
```

Output:

```
General Details:
                           tour_name series_id             start_date               end_date                    venue_name event_status winning_margin
0  Pro Kabaddi League Season 1, 2014         1  08/31/2014T5:30:00TAM  08/31/2014T5:30:00TAM  DOME,NSCI,SVP STADIUM,MUMBAI    Completed             11

Participants:
               team_name team_id         player_name player_id player_value  player_type
0   Jaipur Pink Panthers       3      Maninder Singh       143            8             
1   Jaipur Pink Panthers       3       Rajesh Narwal        86            7             
2   Jaipur Pink Panthers       3     Prashant Chavan       147            6  All Rounder
3   Jaipur Pink Panthers       3        Jasvir Singh        52            4             
4   Jaipur Pink Panthers       3           Ran Singh       160            3             
5   Jaipur Pink Panthers       3      Navneet Gautam        72            2     Defender
6   Jaipur Pink Panthers       3        Balbir Singh        32            0  All Rounder
7   Jaipur Pink Panthers       3          Rohit Rana        96            0             
8   Jaipur Pink Panthers       3     Samarjeet Singh       159            0     Defender
9                U Mumba       5          Anup Kumar        29           10             
10               U Mumba       5    Rishank Devadiga        94            3             
11               U Mumba       5  Pawan Kumar Kadian       156            3             
12               U Mumba       5       Shabeer Bappu       105            2             
13               U Mumba       5         Jeeva Kumar        54            2             
14               U Mumba       5      Mohit Chhillar        71            1             
15               U Mumba       5         Jeeva Gopal        53            0     Defender
16               U Mumba       5         Vishal Mane       123            0             
17               U Mumba       5       Surender Nada       146            0     Defender




```
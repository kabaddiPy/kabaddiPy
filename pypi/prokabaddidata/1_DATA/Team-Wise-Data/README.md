

This contains **Team-Wise** data


i.e. data that has been collected on a team-wise basis at a Macro Level.


```
Defender_Skills_TeamWise
Raider-Skills_TeamWise
seasons_1_to_4_final.csv
seasons_5_plus_and_all_rounded.csv
standings_json
z_archive
```


### Defender_Skills_TeamWise

Contains a file `ALL_Defensive_Skills_Merged.csv` which has the following data:

For all seasons post season 5:

Each team (mostly) have the following:

- Type 1

  1. A count of the skills used to carry out `successful tackles`.

- Type(2) If a tackle was unsuccesful i.e. the raider managed to escape to the other side:

  2. A count of the skill employed by the raider on the defenders that led to an unsuccesful tackle by the defenders. (termed `raider-skill`)
  
  3. A count of the "`counter-action-skill`" i.e. the tactic employed by the raider to escape the tackle attempt by the defending team.




List of Unique Defender_Skills (that led to successful tackles):

```
Ankle
Other
Push
Thigh
self out
Knee Hold
Follow
Ankle Hold
Block
Thigh Hold
Dive
Chain
Hand Touch
Struggle
Running Hand Touch
Toe Touch
Body Hold
Self-out
Release
Out Turn
Jump
Dubki
In Turn
Create Gap
Defender self out
Leg Thrust
Reverse Kick
Side Kick
Running Kick
Chain_def
Defender selfout(lobby shirt pull)
Raider self out(lobby tim..)
```

List of Unique Counter-Skills (that led to unsuccesful tackles):

```
Release
Struggle
Out Turn
Jump
Dubki
In Turn
Create Gap
Chain
Running Hand Touch
Hand Touch
Defender self out
Leg Thrust
Reverse Kick
Toe Touch
Side Kick
Running Kick
Thigh Hold
Block
Dive
Ankle Hold
Push
Body Hold
Self-out
Chain_def
Follow
Defender selfout(lobby shirt pull)
Raider self out(lobby tim..)
```


List of Unique Attacking-Skills (that led to unsuccesful tackles):

```
Hand Touch
Struggle
Running Hand Touch
Toe Touch
Block
Dive
Thigh Hold
Ankle Hold
Body Hold
Push
Follow
Self-out
Release
Out Turn
Jump
Dubki
In Turn
Create Gap
Chain
Defender self out
Leg Thrust
Reverse Kick
Side Kick
Running Kick
Chain_def
Defender selfout(lobby shirt pull)
Raider self out(lobby tim..)
```


### Raider-Skills_TeamWise






### seasons_1_to_4_final.csv

Contains team performance data for the first four seasons of Pro Kabaddi League. 

Each row represents a team's performance in a specific season.



```
season, team_id, team_name, matches_played, 

1  team-average-raid-points_{rank, value, per-match}, 
2  team-avg-points-scored_{rank, value, per-match},, 
3  team-all-outs-conceded_{rank, value, per-match},, 
4  team-super-raid_{rank, value, per-match},, 
5  team-dod-raid-points_{rank, value, per-match},, 
6  team-super-tackles_{rank, value, per-match},, 
7  team-raid-points_{rank, value, per-match},, 
8  team-successful-raids_{rank, value, per-match},, 
9  team-total-points-conceded_{rank, value, per-match},, 
10  team-tackle-points_{rank, value, per-match},, 
11  team-total-points_{rank, value, per-match},, 
12  team-all-outs-inflicted_{rank, value, per-match},, 
13  team-average-tackle-points_{rank, value, per-match},, 
14  team-successful-tackles_{rank, value, per-match},, 
```




### seasons_5_plus_and_all_rounded.csv

Contains similar data for seasons 5 onwards, including an "all" category for cumulative stats. It includes two additional columns: "Total touch points" and "Total bonus points".

Column names for seasons_5_plus_and_all_rounded.csv:

```
season, team_id, team_name, matches_played, 

1  team-average-raid-points_{rank, value, per-match}
2  team-avg-points-scored_{rank, value, per-match}
3  team-all-outs-conceded_{rank, value, per-match}
4  team-successful-tackle-percent_{rank, value, per-match}
5  team-super-raid_{rank, value, per-match}
6  team-raid_{rank, value, per-match}
7  team-successful-raid-percent_{rank, value, per-match}
8  team-dod-raid-points_{rank, value, per-match}
9  team-super-tackles_{rank, value, per-match}

10  Total touch points_{value, per-match}, 
11  Total bonus points_{value, per-match}, 

12  team-raid-points_{rank, value, per-match}
13  team-successful-raids_{rank, value, per-match}
14  team-total-points-conceded_{rank, value, per-match}
15  team-tackle-points_{rank, value, per-match}
16  team-total-points_{rank, value, per-match}
17  team-successful-tackles-per-match_{rank, value, per-match}
18  team-all-outs-inflicted_{rank, value, per-match}
19  team-average-tackle-points_{rank, value, per-match}
20  team-successful-tackles_{rank, value, per-match}
```



### standings_json

This contains standings data for all seasons (Season-01 to Season-10) in JSON format.

It has a file for each season. 

The data is in the format of a dictionary with a single key "standings" which is a dictionary itself with keys such as `series_id`, `series_name`, `parent_series_id`, `champion_id`, `parent_series_global_id`, `last_updated`, `groups`.

The "groups" key contains a list with a single dictionary representing the group. This group dictionary has the following structure:

- "id": Group ID
- "name": Group name (e.g., "A")
- "teams": A dictionary containing a "team" key, which is a list of dictionaries, each representing a team

Each team dictionary in the "team" list contains detailed information about the team's performance:

- "`team_id`": Unique identifier for the team (e.g., 1, 2, 3, etc.)
- "`team_global_id`": Global identifier for the team (Always 0. Not useful.) [❌]
- "`team_name`": Full name of the team
- "`team_short_name`": Abbreviated name of the team
- "`position`": Current position in the standings
- "`prev_position`": Previous position in the standings (Always null. Not useful.) [❌]
- "`position_status`": Status of the team's position (Always null. Not useful.) [❌]
- "`played`": Number of matches played
- "`wins`": Number of matches won
- "`lost`": Number of matches lost
- "`tied`": Number of matches tied
- "`draws`": Number of matches drawn
- "`noresult`": Number of matches with no result
- "`score_diff`": Score difference 
- "`points_conceded`": Points conceded by the team (Always empty string. Not useful.) [❌]
- "`points_scored`": Points scored by the team (Always empty string. Not useful.) [❌]
- "`points`": Total points in the standings
- "`away_wins`": Number of away wins (Always empty string. Not useful.) [❌]
- "`away_points_conceded`": Points conceded in away matches (Always empty string. Not useful.) [❌]
- "`away_points_scored`": Points scored in away matches (Always empty string. Not useful.) [❌]
- "`home_wins`": Number of home wins (Always empty string. Not useful.) [❌]
- "`is_qualified`": Boolean indicating if the team has qualified
- "`trump_matches_won`": Number of trump matches won (Always empty string. Not useful.) [❌]
- "`ga`": Goals against (Always empty string. Not applicable for kabaddi. Not useful.) [❌]
- "`gf`": Goals for (Always empty string. Not applicable for kabaddi. Not useful.) [❌]
- "`match_result`": A dictionary containing a "match" key, which is a list of dictionaries representing individual match results

Each match result dictionary contains:

- "id": Match ID
- "result": Result of the match for the current team (e.g., "W" for win, "L" for loss, "T" for tie)
- "prev_position": Previous position before this match (Not useful.) [❌]
- "date": Date of the match
- "teama_id": ID of team A
- "teama_short_name": Short name of team A
- "teama_score": Score of team A
- "teamb_id": ID of team B
- "teamb_short_name": Short name of team B
- "teamb_score": Score of team B
- "post_match_position": Position after this match (Not useful.) [❌]
- "match_result": Description of the match result (e.g., "U Mumba Won by 7 Pts")


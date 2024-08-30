
# Player-Wise Data

List of files:

```
AllSeasons_AllTeams_DefenderSuccessRate.xlsx
AllSeasons_AllTeams_RaiderSuccessRate.xlsx
Raiders-v-No-Of-Defenders_CLEAN -> `merged_raider_v_num_defenders_FINAL.csv`
Team_Lineup_CLEAN -> `Player_Team_Lineup_merged.csv`
all_seasons_player_stats_rounded.csv
```


## AllSeasons_AllTeams_DefenderSuccessRate.xlsx

Contains defender performance data across all seasons and teams. Includes:
- Unique player identifiers
- Season and team information
- Defender names
- Total and **successful tackles**
- Defender success rate (percentage)



## AllSeasons_AllTeams_RaiderSuccessRate.xlsx

Contains raider performance data across all seasons and teams. Includes:
- Unique player identifiers
- Season and team information
- Raider names
- Total and **successful raids**
- Raider success rate (percentage)


## Raiders-v-No-Of-Defenders_CLEAN

This CSV file contains detailed performance data for players in the Pro Kabaddi League (PKL) Season 5 to 9. It includes:

- Player information: name, ID, and team
- Match statistics: number of raids against different numbers of defenders
- Performance metrics: success rates for empty, successful, and unsuccessful raids
- (**Data is broken down by the number of defenders faced (1-7)**)

The dataset provides a comprehensive view of each player's raiding performance across various defensive scenarios, allowing for in-depth analysis of player strategies and effectiveness in different game situations.


## Team_Lineup_CLEAN -> `Player_Team_Lineup_merged.csv`

This CSV file contains detailed player lineup information for the Pro Kabaddi League (PKL) across multiple seasons. Key features include:

- Player details: Name, ID, position
- Team information: Name, ID
- Season data
- Performance metrics: Games played, **games started**
- Unique player-team-season identifiers

The dataset covers multiple PKL seasons and provides a comprehensive view of player participation and team composition over time.


## all_seasons_player_stats_rounded.csv


This CSV file contains comprehensive player statistics for seasons 1 to 10 of Pro Kabaddi League. Key features include:

## Player Statistics CSV Columns

Unique_ID, season, player_id, player-total-points_player_name, player-total-points_match_played, player-total-points_position_id, player-total-points_position_name, player-total-points_team_name, team_id, player-total-points_team_full_name


1. player-super-tackles_{`rank`, value, `points_per_match`},
2. player-raid-points_{`rank`, value, `points_per_match`},
3. player-super-raids_{`rank`, value, `points_per_match`},
4. high-5s_{`rank`, value, `points_per_match`},
5. player-tackle-points_{`rank`, value, `points_per_match`},
6. player-avg-tackle-points_{`rank`, value, `points_per_match`},
7. player-dod-raid-points_{`rank`, value, `points_per_match`},
8. player-total-points_{`rank`, value, `points_per_match`},
9. player-successful-tackles_{`rank`, value, `points_per_match`},
10. player-successful-raids_{`rank`, value, `points_per_match`},
11. super-10s_{`rank`, value, `points_per_match`},









TODOs here


- [ x ] Do player-ids for RaiderSuccessRate
- [ x ] Do S7 last team DefenderSuccessRate
- [ x ] Add player-id to `all_seasons_player_stats_rounded`
- [ ] Second pass for Raiders v Num of Defenders
- [ x ] Add player-id to `team-lineup-merged`

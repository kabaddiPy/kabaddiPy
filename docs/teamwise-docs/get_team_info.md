---
layout: default
title: get_team_info
parent: Team Functions
nav_order: 1
---
### `get_team_info`

Retrieve team information for a specific team and season.

This function fetches aggregated statistics, raider skills, and defender skills for a given team in a specified season or across all seasons.

#### Parameters
{: .no_toc }
- **team_id**: `int`  
  The unique identifier for the team.

- **season**: `str` or `int`, optional  
  The season for which to retrieve data. Can be:
  - `'overall'` (default): Retrieves data across all seasons.
  - `int`: A specific season number.

#### Returns
{: .no_toc }
- **tuple**  
  A tuple containing five elements:
  1. `df_rank` (`DataFrame`): Team rankings in various categories.
  2. `df_value` (`DataFrame`): Raw statistic values for the team.
  3. `df_per_match` (`DataFrame`): Per-match statistics for the team.
  4. `filtered_team_raider_skills` (`DataFrame` or `None`): Raider skills data for the team.
  5. `filtered_team_defender_skills` (`DataFrame` or `None`): Defender skills data for the team.

#### Notes
{: .no_toc }
- If `season` is `'overall'`, raider and defender skills data are not returned (set to `None`).
- For a specific season, all `DataFrames` are transposed for easier reading.
- If no data is found for the specified team and season, all return values will be `None`.

### Example Usage
{: .no_toc }
```python
    df_rank, df_value, df_per_match, filtered_team_raider_skills, filtered_team_defender_skills = api.get_team_info(season=6, team_id=29)
    print("Team Rank:")
    print(df_rank)
    print("\nTeam Value:")
    print(df_value)
    print("\nTeam Per Match:")
    print(df_per_match)
    print("\nTeam Raider Skills:")
    print(filtered_team_raider_skills)
    print("\nTeam Defender Skills:")
    print(filtered_team_defender_skills)
```

Output:

```python
    
Team Rank:
                                                     53
season                                              6.0
team_id                                              29
team_name                               Tamil Thalaivas
matches_played                                       22
team-average-raid-points_rank                         7
team-avg-points-scored_rank                          10
team-all-outs-conceded_rank                           7
team-successful-tackle-percent_rank                 NaN
team-super-raid_rank                                 11
team-raid_rank                                      NaN
team-successful-raid-percent_rank                   NaN
team-dod-raid-points_rank                            10
team-super-tackles_rank                               7
team-raid-points_rank                                 9
team-successful-raids_rank                            8
team-total-points-conceded_rank                       8
team-tackle-points_rank                              12
team-total-points_rank                               10
team-successful-tackles-per-match_rank              NaN
team-all-outs-inflicted_rank                          9
team-average-tackle-points_rank                      12
team-successful-tackles_rank                         12

---

Team Value:
                                                      53
season                                               6.0
team_id                                               29
team_name                                Tamil Thalaivas
matches_played                                        22
team-all-outs-conceded_value                          27
team-successful-tackle-percent_value                 NaN
team-super-raid_value                                  7
team-raid_value                                      NaN
team-successful-raid-percent_value                   NaN
team-dod-raid-points_value                            67
team-super-tackles_value                              15
Total_touch_points_value                           315.0
Total_bonus_points_value                           105.0
team-raid-points_value                               419
team-successful-raids_value                          345
team-total-points-conceded_value                     741
team-tackle-points_value                             189
team-total-points_value                              671
team-successful-tackles_value                        173
team-successful-tackles-per-match_value              NaN
team-all-outs-inflicted_value                         20
team-average-raid-points_value                     19.05
team-avg-points-scored_value                        30.5
team-average-tackle-points_value                    8.59

---

Team Per Match:
                                                     53
season                                              6.0
team_id                                              29
team_name                               Tamil Thalaivas
matches_played                                       22
team-all-outs-conceded_per-match                  1.227
team-super-raid_per-match                         0.318
team-raid_per-match                                 0.0
team-dod-raid-points_per-match                    3.045
team-super-tackles_per-match                      0.682
team-total-touch-points-ext_per-match            14.318
team-total-bonus--points-ext_per-match            4.773
team-raid-points_per-match                       19.045
team-successful-raids_per-match                  15.682
team-total-points-conceded_per-match             33.682
team-tackle-points_per-match                      8.591
team-total-points_per-match                        30.5
team-all-outs-inflicted_per-match                 0.909
team-successful-tackles_per-match                 7.864

---

Team Raider Skills:
    Season            Skill Type          Skill Name  Tamil Thalaivas (29)
0        6  Counter Action Skill             Release                  49.0
1        6  Counter Action Skill            Struggle                  17.0
2        6  Counter Action Skill            Out Turn                  19.0
3        6  Counter Action Skill                Jump                  17.0
4        6  Counter Action Skill             In Turn                   9.0
5        6  Counter Action Skill          Create Gap                   9.0
6        6  Counter Action Skill               Dubki                   3.0
7        6       Attacking Skill  Running Hand Touch                  91.0
8        6       Attacking Skill          Hand Touch                  56.0
9        6       Attacking Skill          Leg Thrust                  14.0
10       6       Attacking Skill           Toe Touch                  10.0
11       6       Attacking Skill   Defender self out                   6.0
12       6       Attacking Skill        Reverse Kick                   7.0
13       6       Attacking Skill           Side Kick                   3.0
14       6       Attacking Skill        Running Kick                   NaN
15       6       Defensive Skill                Dive                  28.0
16       6       Defensive Skill               Block                  41.0
17       6       Defensive Skill          Ankle Hold                  37.0
18       6       Defensive Skill          Thigh Hold                  24.0
19       6       Defensive Skill                Push                  28.0
20       6       Defensive Skill           Body Hold                  24.0
21       6       Defensive Skill            Self-out                  16.0
22       6       Defensive Skill              Follow                   2.0
23       6       Defensive Skill           Chain_def                   1.0

---

Team Defender Skills:
    Season            Skill Type          Skill Name  Tamil Thalaivas (29)
0        6       Defensive Skill               Block                  47.0
1        6       Defensive Skill                Dive                  30.0
2        6       Defensive Skill          Thigh Hold                  24.0
3        6       Defensive Skill          Ankle Hold                  16.0
4        6       Defensive Skill           Body Hold                  22.0
5        6       Defensive Skill                Push                  27.0
6        6       Defensive Skill              Follow                   NaN
7        6       Defensive Skill            Self-out                   3.0
8        6  Counter Action Skill             Release                  81.0
9        6  Counter Action Skill            Struggle                  13.0
10       6  Counter Action Skill            Out Turn                  20.0
11       6  Counter Action Skill                Jump                  16.0
12       6  Counter Action Skill               Dubki                   5.0
13       6  Counter Action Skill             In Turn                   8.0
14       6  Counter Action Skill          Create Gap                   5.0
15       6  Counter Action Skill               Chain                   NaN
16       6       Attacking Skill  Running Hand Touch                  74.0
17       6       Attacking Skill          Hand Touch                  44.0
18       6       Attacking Skill   Defender self out                   6.0
19       6       Attacking Skill          Leg Thrust                  17.0
20       6       Attacking Skill        Reverse Kick                   6.0
21       6       Attacking Skill           Toe Touch                  20.0
22       6       Attacking Skill           Side Kick                   3.0
23       6       Attacking Skill        Running Kick                   3.0
```


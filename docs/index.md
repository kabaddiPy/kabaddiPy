---
title: Home
layout: default
has_toc: true
nav_order: 1
has_children: false
---


# Prokabaddi API

This documentation covers the main functions of the `KabaddiDataAPI` class that return useful data for Kabaddi statistics and information.

{: .note }
> This documentation is actively being developed alongwith the API.



---

## Installation 
Use the following command to install.

```shell
pip install kabaddiPy
```

---

We have split our functions into 3 categories:

## Overall Functions
  ### 1. `get_pkl_standings`(season=None, qualified=False, team_id=None)
  
  ### 2. `get_season_matches`(season="all")

## Team-Wise Functions
  
  ### 3. `get_team_info`(team_id, season='overall')

  ### 4. `get_team_matches`(season, team_id)

  ### 5. `build_team_roster`(team_id, season)

## Player-Information
  
  ### 6. `get_player_info`(player_id, season=None)


## Detailed Granular Match-Details (Play-by-Play)
  
  ### 7. `load_match_details`(season, match_id)

  ### 8. `load_pbp_data`(season, match_id)


## Visualisation Functions
  
  ### 9. `plot_point_progression`(file_path)

  ### 10. `plot_team_zones`(directory_path, team_id, zone_type='strong')

  ### 11. `plot_player_zones`(directory_path, player_id, zone_type='strong')

  ### 12. `plot_player_zones_grid`(x,y,z)



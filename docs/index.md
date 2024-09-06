---
title: Home
layout: default
has_toc: true
nav_order: 1
has_children: false
---


# Prokabaddi API

This documentation covers the main functions of the `KabaddiDataAPI` class that return useful data for Kabaddi statistics and information.


[`kabaddiPy`](https://github.com/kabaddiPy/kabaddiPy) is a python
Package that is designed to pull play-by-play data from
the newest version of the [ProKabaddi League](https://www.prokabaddi.com/). 
In the past, there have been a next to no scrapers for the Kabaddi.

With the first season of the league kicking off on January 1st, and
games being broadcast on ESPN+, this package was created to allow access
to play-by-play data to continue pushing women’s hockey analytics
forward.

The lack of data and poor access to data have been the
biggest barrier to entry in kabaddi analytics, a barrier that
this package intends to alleviate.

<center>

<img src='https://github-production-user-asset-6210df.s3.amazonaws.com/85307430/354763168-e074c4c2-18b3-4580-a9dd-1aa40f9495b0.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAVCODYLSA53PQK4ZA%2F20240906%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240906T000835Z&X-Amz-Expires=300&X-Amz-Signature=b0107ce954e05cb6ec04bc6871afc2ae30260290f7fb99599baa22ef1e881936&X-Amz-SignedHeaders=host&actor_id=85307430&key_id=0&repo_id=836594456' width="70%" />

</center>



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



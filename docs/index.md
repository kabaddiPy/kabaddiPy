---
title: Home
layout: default
has_toc: true
nav_order: 1
has_children: false
---

# `kabaddiPy`


This documentation covers the main functions of the `KabaddiDataAPI` class that return useful data for Kabaddi statistics and information.

[`kabaddiPy`](https://github.com/kabaddiPy/kabaddiPy) is a python package that is designed to pull **play-by-play**, **team**, **player** and **standings** data from the newest version of the [ProKabaddi League](https://www.prokabaddi.com/) website. In the past, there have been next to no scrapers for the sport.

<div style="float: right; margin-left: 15px;">
    <img src='https://github.com/user-attachments/assets/e074c4c2-18b3-4580-a9dd-1aa40f9495b0' width="300px" />
</div>

With Season 11 of the Pro Kabaddi League set to begin on October 18, and the 2025 Kabaddi World Cup on the horizon, this package was developed to provide access to detailed play-by-play data, aiming to energize & catalyze the Kabaddi analytics community.

The lack of data and poor access to data have been the biggest barriers to entry in Kabaddi analytics, a barrier that this package intends to alleviate.



This documentation covers the main functions of the `KabaddiDataAPI` class that return useful data for Kabaddi statistics and information. [`kabaddiPy`](https://github.com/kabaddiPy/kabaddiPy) is a python Package that is designed to pull play-by-play data from the newest version of the [ProKabaddi League](https://www.prokabaddi.com/).




{: .note }
> This documentation is actively being developed alongwith the API.



---

## Installation 
Use the following command to install.

```shell
pip install kabaddiPy
```

---

## Documentation

You can find the documentation for [`kabaddiPy`](https://github.com/kabaddiPy/kabaddiPy) on [GitHub pages](https://kabaddipy.github.io/kabaddiPy/).

You can view CSVs of historical play-by-play on the [`kabaddiPy`](https://github.com/kabaddiPy/kabaddiPy) [data repo](https://github.com/kabaddiPy/kabaddi-data), as well as the process for scraping that historical data.


---


We have split our functions into 3 categories:

#### Overall Functions
  
  1. `get_pkl_standings(season=None, qualified=False, team_id=None)`
  
  2. `get_season_matches(season="all")`

#### Team-Wise Functions
  
  3. `get_team_info(team_id, season='overall')`

  4. `get_team_matches(season, team_id)`

  5. `build_team_roster(team_id, season)`

#### Player-Information
  
  6. `get_player_info(player_id, season=None)`
   
  7. `get_matchwise_player_info(self, player_id, season)`
   
  8. `get_player_rvd(self, player_id, season=None)`


#### Detailed Granular Match-Details (Play-by-Play)
  
  8. `load_match_details(season, match_id)`

  9. `load_pbp_data(season, match_id)`


#### Visualisation Functions
  
  10. `plot_point_progression(season, match_id)`

  11. `plot_team_zones(team_id, season, zone_type='strong')`

  12. `plot_player_zones_improved(player_id, season, zone_type='strong')`

  13. `plot_player_zones_grid(player_ids, season, zone_type='strong', max_cols=4)`


#### Utility Function

  14.  `get_team_ids(season)`



### Citation

To cite the [`kabaddiPy`](https://github.com/kabaddiPy/kabaddiPy) package in publications, use:


**BibTex Citation**

```
@misc{kabaddiPy_2024,
  author = {kabaddiPy},
  title = {kabaddiPy: A Python Package for Kabaddi Analytics},
  url = {https://kabaddipy.github.io/kabaddiPy/},
  year = {2024}
}
```

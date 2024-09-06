---
title: Player Functions
layout: default
has_toc: true
has_children: false
nav_order: 4
---

# Player Functions

## `get_player_info(player_id, season=None)`

Retrieve comprehensive player information for a specific season.

### Parameters:
- `player_id` (int): The unique identifier for the player.
- `season` (int, optional): The season number for which to retrieve data. If not specified, the latest season available will be used.

### Returns:
A tuple containing four pandas DataFrames, each transposed for easier reading:
1. `player_stats_df_rank` (DataFrame): Player's ranking statistics.
2. `player_stats_df_value` (DataFrame): Player's value statistics.
3. `player_stats_df_per_match` (DataFrame): Player's per-match statistics.
4. `rvd_extracted_df` (DataFrame): Raider vs. Defender statistics.

### Notes:
- The function aggregates data from various sources including CSV files on player statistics, raider vs. defender data, defender success rates, raider success rates, and lineup information.
- If data is unavailable for the specified player or season, appropriate warning messages are printed.
- Handles data type conversions and missing value imputations for consistency.


---

## `get_detailed_player_info(player_id, season)`

Extract detailed player statistics from all matches in a given season.

### Parameters:
- `player_id` (int): The ID of the player.
- `season` (int): The season number.

### Returns:
- `pandas.DataFrame`: A DataFrame containing detailed player statistics for each match, including:
  - `match_id`, `date`, `team_name`, `team_score`, `opponent_name`, `opponent_score`
  - `played`, `starter`, `on_court`, `captain`, `total_points`, `raid_points`, `tackle_points`
  - `raids_total`, `raids_successful`, `raids_unsuccessful`, `raids_empty`, `super_raids`
  - `tackles_total`, `tackles_successful`, `tackles_unsuccessful`, `super_tackles`
  - `green_card_count`, `yellow_card_count`, `red_card_count`
  - `top_raider`, `top_defender`
  - `substitutions` and `first_substitution_time` (if any)

### Notes:
- The function processes all JSON match files for the specified season and extracts detailed player statistics.
- If no data is found for the specified player or season, an empty DataFrame is returned.
- Includes additional calculated statistics such as the number of matches played, matches started, average points for the season, and total substitutions.


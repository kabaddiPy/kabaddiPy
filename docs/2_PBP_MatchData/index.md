---
title: Play-by-Play Data
layout: default
has_toc: true
has_children: false
nav_order: 5
---

#### Table of contents

{: .no_toc .text-delta }

1. TOC
{:toc}


## `load_match_details(season, match_id)`

Load and process match details for a specific season and match ID.

### Parameters:
- `season` (int): The season number.
- `match_id` (str): The unique identifier for the match.

### Returns:
A tuple containing six pandas DataFrames:
1. `match_detail_df`: DataFrame with overall match details.
2. `events_df`: DataFrame with all events that occurred during the match.
3. `zones_df`: DataFrame with information about different zones on the court.
4. `team1_df`: DataFrame with detailed information about the first team.
5. `team2_df`: DataFrame with detailed information about the second team.
6. `breakdown_df`: DataFrame with breakdown data of the game.


### Notes:
- If an error occurs during data loading or processing, the function will print an error message and return `None` for all DataFrames.
- The function retrieves the match data from a JSON file and processes it to extract relevant match information.
- In season 4 or if breakdown data is unavailable, an empty `breakdown_df` will be returned.

---

## `load_pbp(season, match_id)`

Load the play-by-play (PBP) data for a specific match in a given season.

### Parameters:
- `season` (int): The season number.
- `match_id` (str): The unique identifier for the match.

### Returns:
- `DataFrame`: A DataFrame containing the play-by-play events of the match. Returns `None` if there was an error loading the match details.

### Notes:
- This function calls `load_match_details` to retrieve the full match data and extracts only the `events_df` (play-by-play data).
- Other match-related information (e.g., team details, zones) is discarded.

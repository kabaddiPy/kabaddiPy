# KabaddiDataAPI

The `KabaddiDataAPI` class provides a set of methods to access and analyze data from Pro Kabaddi League (PKL) matches and seasons.

## Main Functions

### 1. `get_pkl_standings(season=None, qualified=False, team_id=None`)

Retrieves the standings for a specific PKL season.

- **Inputs:**
  - `season`: int (default: None, uses the latest season)
  - `qualified`: bool (default: False)
  - `team_id`: int (default: None)
- **Output:** pandas DataFrame containing team standings

### 2. `get_season_matches(season="all")`

Retrieves match data for a specific season or all seasons.

- **Input:** `season`: str or int (default: "all")
- **Output:** pandas DataFrame containing match details

### 3. `get_team_info(team_id, season='overall')`

Retrieves comprehensive information for a specific team in a given season or overall.

- **Inputs:**
  - `team_id`: int
  - `season`: str or int (default: 'overall')
- **Output:** Tuple of pandas DataFrames (rank, value, per_match, raider_skills, defender_skills)

### 4. `get_team_matches(season, team_id)`

Retrieves all matches for a specific team in a given season.

- **Inputs:**
  - `season`: int
  - `team_id`: str
- **Output:** pandas DataFrame containing match details

### 5. `build_team_roster(team_id, season)`

Builds a roster for a specific team in a given season.

- **Inputs:**
  - `team_id`: int
  - `season`: int
- **Output:** pandas DataFrame containing player roster information

### 6. `get_player_info(player_id, season=None)`

Retrieves comprehensive information for a specific player in a given season.

- **Inputs:**
  - `player_id`: int
  - `season`: int (default: None, uses the latest season)
- **Output:** Tuple of pandas DataFrames (rank, value, per_match, raiders_vs_defenders)

### 7. `load_match_details(season, match_id)`

Retrieves full data for a specific match.

- **Inputs:**
  - `season`: str
  - `match_id`: str
- **Output:** Tuple of pandas DataFrames (match_detail, teams, events, zones, team1, team2)

### 8. `load_pbp_data(season, match_id)`

Retrieves all events (play-by-play data) for a specific match.

- **Inputs:**
  - `season`: str
  - `match_id`: str
- **Output:** pandas DataFrame containing all events in the match


## Usage

```python
api = KabaddiDataAPI()

# Example: Get standings for season 10
standings = api.get_pkl_standings(season=10)

# Example: Get match data for season 6
matches = api.get_season_matches(season=6)

# Example: Get team info for team_id 29 in season 6
team_info = api.get_team_info(season=6, team_id=29)

# Example: Get player info for player_id 660 in season 9
player_info = api.get_player_info(player_id=660, season=9)

# Example: Load match details for match_id 2895 in season 9
match_details = api.load_match_details(season='9', match_id='2895')
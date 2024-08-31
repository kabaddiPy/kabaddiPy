# Match_Dat

## Match Data pbp

The match data is structured into several main sections:

#### 1. match_detail
- **Basic Info**: `match_id`, `match_number`, `clock` (minutes, seconds), `date`, `start_time`, `matchtime_iso`, `gmtoffset`
- **Result**: 
  - `outcome`, `value`, `winning_method`, `winning_team`, `winning_team_id`
- **Player of the Match**: `id`, `value`
- **Series Info**: 
  - `id`, `name`, `short_name`, `parent_series_id`, `parent_series_name`
- **Status**: `status_id`, `status`, `stage`
- **Toss**: `winner`, `selection`
- **Venue**: `id`, `name`

#### 2. teams
- `home_team_id`, `home_team_name`
- **Team Array**:
  - `id`, `name`, `score`, `short_name`
  - **Squad** (array of players):
    - Basic: `id`, `name`, `short_name`, `skill`, `role`
    - Cards: `red_card`, `yellow_card`, `green_card`, `*_card_count`
    - Status: `jersey`, `played`, `captain`, `on_court`, `starter`, `top_raider`
    - Points: `total`, `raid_points`, `tackle_points`
    - Performance: `raids`, `tackles`, `strong_zones`, `weak_zones`

#### 3. stats (for each team)
- **Points**: `total`, `all_out`, `extras`, `declare`, `raid_points`, `tackle_points`
- **Raids**: `total`, `super_raids`, `successful`, `unsuccessful`, `Empty`
- **Tackles**: `total`, `super_tackles`, `successful`, `unsuccessful`
- `all_outs`, `declare`

#### 4. state_of_play (for each team)
- `is_raiding_now`, `players_on_court`
- **Players Array**: `id`, `is_raiding_now`, `on_court`

#### 5. events (array of match events)
- Event Info: `event_no`, `event`, `event_id`, `event_text`
- Player Info: `raider_id`, `raiding_team_id`, `defender_id`, `defending_team_id`
- Points: `raid_points`, `raid_touch_points`, `raid_bonus_points`, `raid_technical_points`, `raid_all_out_points`, `defending_capture_points`, `defending_bonus_points`, `defending_technical_points`, `defending_all_out_points`, `defending_points`
- Special: `super_raid`, `super_tackle`, `clock`, `status_id`, `do_or_die`
- Review: `review_taken`, `team_id`, `outcome`, `reason`
- `score`, `defenders` (array)

#### 6. zones
- **Zone Array**: `id`, `name`




## Matches Overview Data

This directory contains JSON files with overview information about Pro Kabaddi League matches.

#### File Description

- `json_s5.json`: Contains match data for Pro Kabaddi League Season 5

#### Data Structure

Each JSON file contains an array of match objects under the "matches" key. Each match object includes the following information:

- `tour_name`: Name of the tournament (e.g. `Pro Kabaddi League Season 3, 2016`)
- `result_code`: Result code of the match (e.g. `W` for win, `L` for loss)
- `series_id`: ID of the series 
- `end_date`: End date and time of the match
- `event_group`: Group of the event (if applicable)
- `event_sub_status`: Brief description of the match result (e.g. `U Mumba beat Telugu Titans (27-25)`)
- `start_date`: Start date and time of the match
- `event_islinkable`: Indicates if the event is linkable
- `event_status`: Status of the event (e.g., "Completed")
- `event_duration_left`: Remaining duration of the event (not useful (❌))
- `result_sub_code`: Sub-code of the result (not useful (❌))
- `event_is_daynight`: Indicates if it's a day/night event (not useful (❌))
- `winning_margin`: Margin of victory (e.g. `2` for a 2-point victory)
- `event_status_id`: ID of the event status (not useful (❌))
- `venue_id`: ID of the venue
- `sport`: Sport name (always "kabaddi" in this case)
- `venue_name`: Name of the venue (e.g. `Rajiv Gandhi Indoor Stadium`)
- `game_id`: ID of the game 
- `event_stage`: Stage of the event (e.g., "League")
- `event_name`: Name of the event (e.g., "Match 1")
- `league_code`: Code of the league (e.g., "pkl" for Pro Kabaddi League)
- `event_state`: State of the event 
- `series_name`: Name of the series (e.g. `Pro Kabaddi League Season 3, 2016`)
- `tour_id`: ID of the tour
- `event_livecoverage`: Information about live coverage (if applicable)

### Participants

Each match object also includes a `participants` array with details about the teams and players involved:

- `name`: Full name of the team
- `short_name`: Short name or abbreviation of the team
- `id`: Team ID
- `value`: Score of the team
- `players_involved`: Array of player objects, each containing:
  - `name`: Name of the player
  - `id`: Player ID
  - `value`: Points scored by the player
  - `type`: Player's role (if specified)


## Usage

This data can be used for various analyses, including:

- Match results and statistics
- Player performance tracking
- Team performance analysis
- Venue statistics
- Season-wide trends and patterns

Researchers and analysts can use this data to gain insights into the Pro Kabaddi League matches, team strategies, and player performances.

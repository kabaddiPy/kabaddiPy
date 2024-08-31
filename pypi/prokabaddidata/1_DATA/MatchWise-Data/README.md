
# Matches Data


## Match_Data_pbp


# Match Data Structure

## 1. match_detail
   - match_id
   - match_number
   - clock (minutes, seconds)
   - date
   - start_time
   - matchtime_iso
   - gmtoffset
   - result
     - outcome
     - value
     - winning_method
     - winning_team
     - winning_team_id
   - player_of_the_match (id, value)
   - series
     - id
     - name
     - short_name
     - parent_series_id
     - parent_series_name
   - status_id
   - status
   - stage
   - toss (winner, selection)
   - venue (id, name)

## 2. teams
   - home_team_id
   - home_team_name
   - team (array)
     - id
     - name
     - score
     - short_name
     - squad (array of players)
       - id
       - name
       - short_name
       - skill
       - role
       - red_card
       - yellow_card
       - green_card
       - red_card_count
       - yellow_card_count
       - green_card_count
       - jersey
       - played
       - captain
       - on_court
       - starter
       - top_raider
       - points
         - total
         - raid_points (total, touch, raid_bonus)
         - tackle_points (total, capture, capture_bonus)
       - raids
         - total
         - super_raids
         - successful
         - unsuccessful
         - Empty
       - tackles
         - total
         - super_tackles
         - successful
         - unsuccessful
       - strong_zones
         - strong_zone (array of zone_id and points)
       - weak_zones
         - weak_zone (array of zone_id and points)
       - top_defender

## 3. stats (for each team)
   - points
     - total
     - all_out
     - extras
     - declare
     - raid_points (total, touch, raid_bonus)
     - tackle_points (total, capture, capture_bonus)
   - raids
     - total
     - super_raids
     - successful
     - unsuccessful
     - Empty
   - tackles
     - total
     - super_tackles
     - successful
     - unsuccessful
   - all_outs
   - declare

## 4. state_of_play (for each team)
   - is_raiding_now
   - players_on_court
   - players (array)
     - id
     - is_raiding_now
     - on_court

## 5. events (array of match events)
   - event_no
   - event
   - event_id
   - event_text
   - raider_id (if applicable)
   - raiding_team_id (if applicable)
   - defender_id (if applicable)
   - defending_team_id (if applicable)
   - raid_points
   - raid_touch_points
   - raid_bonus_points
   - raid_technical_points
   - raid_all_out_points
   - defending_capture_points
   - defending_bonus_points
   - defending_technical_points
   - defending_all_out_points
   - defending_points
   - super_raid
   - super_tackle
   - clock
   - status_id
   - do_or_die
   - review
     - review_taken
     - team_id
     - outcome (id, outcome_value)
     - reason (id, reason_value)
   - score
   - defenders (array)

## 6. zones
   - zone (array)
     - id
     - name





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

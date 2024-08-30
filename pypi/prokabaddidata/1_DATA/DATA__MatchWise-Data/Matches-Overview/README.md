# Matches Overview Data

This directory contains JSON files with detailed information about Pro Kabaddi League matches.

## File Description

- `json_s5.json`: Contains match data for Pro Kabaddi League Season 5

## Data Structure

Each JSON file contains an array of match objects under the "matches" key. Each match object includes the following information:

- `tour_name`: Name of the tournament
- `result_code`: Result code of the match
- `series_id`: ID of the series
- `end_date`: End date and time of the match
- `event_group`: Group of the event (if applicable)
- `event_sub_status`: Brief description of the match result
- `start_date`: Start date and time of the match
- `event_islinkable`: Indicates if the event is linkable
- `event_status`: Status of the event (e.g., "Completed")
- `event_duration_left`: Remaining duration of the event (if applicable)
- `result_sub_code`: Sub-code of the result
- `event_is_daynight`: Indicates if it's a day/night event
- `winning_margin`: Margin of victory
- `event_status_id`: ID of the event status
- `venue_id`: ID of the venue
- `sport`: Sport name (always "kabaddi" in this case)
- `venue_name`: Name of the venue
- `game_id`: ID of the game
- `event_stage`: Stage of the event (e.g., "League")
- `event_name`: Name of the event (e.g., "Match 1")
- `league_code`: Code of the league (e.g., "pkl" for Pro Kabaddi League)
- `event_state`: State of the event
- `series_name`: Name of the series
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

Researchers and analysts can use this data to gain insights into the Pro Kabaddi League Season 5 matches, team strategies, and player performances.

from prokabaddidata.prokabaddidata import KabaddiDataAggregator

aggregator = KabaddiDataAggregator()

# Get all team names
team_names = aggregator.get_all_team_names()
print("Team Names:", team_names)

# Get season standings
standings = aggregator.team_season_standings()
print("Season Standings:", standings)

# Get player information
players_info = aggregator.get_players_team_info_and_profile_url()
print("Players Info:", players_info[:5])  # Print first 5 players

# Get team line-up data
line_up_data = aggregator.team_line_up()
print("Team Line-up Data:", line_up_data)

# Add more function calls as needed

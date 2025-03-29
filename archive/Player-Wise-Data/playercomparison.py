import kabaddiPy
pkl = kabaddiPy.PKL()
# List of player IDs to compare
player_ids = [143, 12, 211, 160]  # Example player IDs

# Compare the player zones in a grid, specifying the season and zone type
pkl.plot_player_zones_grid(player_ids, season=5, zone_type='strong', max_cols=2)


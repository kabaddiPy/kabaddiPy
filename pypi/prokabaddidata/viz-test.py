import os
import json
import matplotlib.pyplot as plt
import numpy as np


def get_player_points_in_zones(player_id, directory):
    # Define the zones based on your description
    zones = {
        1: "Left Lobby", 2: "Right Lobby", 3: "Midline Left",
        4: "Midline Centre", 5: "Midline Right", 6: "Baulk Left",
        7: "Baulk Centre", 8: "Baulk Right", 9: "Bonus Left",
        10: "Bonus Centre", 11: "Bonus Right"
    }

    # Initialize dictionary to track points in each zone
    points_by_zone = {zone_id: 0 for zone_id in zones.keys()}

    # Process each file in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                data = json.load(file)

                # Iterate through the teams and players
                for team in data['gameData']['teams']['team']:
                    for player in team['squad']:
                        if player['id'] == player_id:
                            # Sum points in strong zones
                            for strong_zone in player['strong_zones']['strong_zone']:
                                zone_id = strong_zone['zone_id']
                                points_by_zone[zone_id] += strong_zone['points']

    return points_by_zone


import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle

def plot_half_kabaddi_court(points_by_zone):
    fig, ax = plt.subplots(figsize=(15, 12))

    # Court dimensions for half the court
    court_width, court_length = 13, 10

    # Colors
    court_color = '#4169E1'  # Royal Blue
    lobby_color = '#B22222'  # Firebrick Red

    # Draw half court (main play area)
    ax.add_patch(Rectangle((1, 0), (court_width - 2) / 2, court_length, fill=True, color=court_color))

    # Draw left lobby only (half court)
    ax.add_patch(Rectangle((0, 0), 1, court_length, fill=True, color=lobby_color))

    # Draw lines on half court
    line_color = 'white'
    ax.axhline(y=court_length / 2, color=line_color, linewidth=2)
    ax.axhline(y=3.75, color=line_color, linewidth=2)
    ax.axhline(y=court_length - 3.75, color=line_color, linewidth=2)
    ax.axhline(y=1, color=line_color, linewidth=2)
    ax.axhline(y=court_length - 1, color=line_color, linewidth=2)

    # Add labels for half court
    ax.text((court_width - 2) / 4 + 1, court_length / 2, 'Mid Line', ha='center', va='center', color='white')
    ax.text((court_width - 2) / 4 + 1, 3.75, 'Baulk Line', ha='center', va='bottom', color='white')
    ax.text((court_width - 2) / 4 + 1, court_length - 3.75, 'Baulk Line', ha='center', va='top', color='white')
    ax.text((court_width - 2) / 4 + 1, 1, 'Bonus Line', ha='center', va='bottom', color='white')
    ax.text((court_width - 2) / 4 + 1, court_length - 1, 'Bonus Line', ha='center', va='top', color='white')
    ax.text(0.5, court_length / 2, 'Left Lobby', ha='center', va='center', rotation=90, color='white')

    # Plot heat map of points scored in each zone
    max_points = max(points_by_zone.values()) if points_by_zone else 1

    zone_positions = {
        1: (1, 1),  # Left Lobby
        3: (1, 5),  # Midline Left
        6: (1, 8),  # Baulk Left
        9: (1, 10),  # Bonus Left
        4: ((court_width - 2) / 4 + 1, 1),  # Midline Centre
        7: ((court_width - 2) / 4 + 1, 5),  # Baulk Centre
        10: ((court_width - 2) / 4 + 1, 8),  # Bonus Centre
    }

    for zone_id, (x, y) in zone_positions.items():
        points = points_by_zone.get(zone_id, 0)
        intensity = points / max_points
        ax.add_patch(Rectangle((x - 0.5, y - 0.5), 2, 2, fill=True, alpha=intensity, color='green'))
        ax.text(x, y, str(points), ha='center', va='center', color='white', fontsize=14, fontweight='bold')

    # Customize the plot
    ax.set_xlim(0, court_width / 2)
    ax.set_ylim(0, court_length)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title('Points Scored by Player in Half-Court Zones', fontsize=16)

    plt.show()

# Example points by zone data (replace with actual data)



def load_json_data(file_path):
    with open(file_path, 'r') as file:
        return json.loads(file.read())
def aggregate_player_data(directory_path, player_id):
    player_data = None
    strong_zones = {i: 0 for i in range(1, 12)}
    weak_zones = {i: 0 for i in range(1, 12)}

    for filename in os.listdir(directory_path):
        if filename.endswith('.json'):
            file_path = os.path.join(directory_path, filename)
            data = load_json_data(file_path)

            teams = data['gameData']['teams']['team']
            for team in teams:
                for player in team['squad']:
                    if player['id'] == player_id:
                        print(player['id'])
                        if not player_data:
                            player_data = player

                        for zone in player['strong_zones']['strong_zone']:
                            strong_zones[zone['zone_id']] += zone['points']

                        for zone in player['weak_zones']['weak_zone']:
                            weak_zones[zone['zone_id']] += zone['points']

    return player_data, strong_zones, weak_zones


# Example usage
# directory = r"C:\Users\KIIT\Documents\ProKabaddi_API\pypi\prokabaddidata\MatchData_pbp\Season_PKL_Season_9_2022"
directory = r"C:\Users\KIIT\Documents\ProKabaddi_API\pypi\prokabaddidata\MatchData_pbp\Season_PKL_Season_5_2017"
player_id = 46 # Replace with the player's ID
points_by_zone = get_player_points_in_zones(player_id, directory)
player_data, strong_zones, weak_zones = aggregate_player_data(directory, player_id)
print(points_by_zone)
print(strong_zones)
plot_half_kabaddi_court(points_by_zone)
#plot_points_on_kabaddi_mat(points_by_zone)

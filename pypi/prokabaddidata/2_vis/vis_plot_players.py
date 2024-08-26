import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, Circle
import json

def load_json_data(file_path):
    with open(file_path, 'r') as file:
        return json.loads(file.read())

def get_zone_coordinates(zone_id, court_width, court_length):
    zones = {
        1: (0.5, court_length/2),  # Left Lobby
        2: (court_width-0.5, court_length/2),  # Right Lobby
        3: (court_width/4, court_length-0.5),  # Midline Left
        4: (court_width/2, court_length-0.5),  # Midline Centre
        5: (3*court_width/4, court_length-0.5),  # Midline Right
        6: (court_width/4, 3*court_length/4),  # Baulk Left
        7: (court_width/2, 3*court_length/4),  # Baulk Centre
        8: (3*court_width/4, 3*court_length/4),  # Baulk Right
        9: (court_width/4, 0.5),  # Bonus Left
        10: (court_width/2, 0.5),  # Bonus Centre
        11: (3*court_width/4, 0.5),  # Bonus Right
    }
    return zones.get(zone_id, (court_width/2, court_length/2))

def plot_kabaddi_court_with_player_data(data, player_id, zone_type='strong'):
    fig, ax = plt.subplots(figsize=(15, 12))
    
    # Court dimensions
    court_width, court_length = 13, 10
    
    # Colors
    court_color = '#4169E1'  # Royal Blue
    lobby_color = '#B22222'  # Firebrick Red
    
    # Draw court (main play area)
    ax.add_patch(Rectangle((1, 0), court_width-2, court_length, fill=True, color=court_color))
    
    # Draw lobbies
    ax.add_patch(Rectangle((0, 0), 1, court_length, fill=True, color=lobby_color))
    ax.add_patch(Rectangle((court_width-1, 0), 1, court_length, fill=True, color=lobby_color))
    
    # Draw lines
    line_color = 'white'
    ax.axhline(y=court_length/2, color=line_color, linewidth=2)
    ax.axhline(y=3.75, color=line_color, linewidth=2)
    ax.axhline(y=court_length-3.75, color=line_color, linewidth=2)
    ax.axhline(y=1, color=line_color, linewidth=2)
    ax.axhline(y=court_length-1, color=line_color, linewidth=2)
    
    # Add labels
    ax.text(court_width/2, court_length/2, 'Mid Line', ha='center', va='center', color='white')
    ax.text(court_width/2, 3.75, 'Baulk Line', ha='center', va='bottom', color='white')
    ax.text(court_width/2, court_length-3.75, 'Baulk Line', ha='center', va='top', color='white')
    ax.text(court_width/2, 1, 'Bonus Line', ha='center', va='bottom', color='white')
    ax.text(court_width/2, court_length-1, 'Bonus Line', ha='center', va='top', color='white')
    ax.text(0.5, court_length/2, 'Left Lobby', ha='center', va='center', rotation=90, color='white')
    ax.text(court_width-0.5, court_length/2, 'Right Lobby', ha='center', va='center', rotation=90, color='white')
    
    # Find the selected player
    teams = data['teams']['team']
    player = None
    for team in teams:
        for p in team['squad']:
            if p['id'] == player_id:
                player = p
                break
        if player:
            break
    
    if player:
        # Plot player position (center of the court for simplicity)
        player_x, player_y = court_width/2, court_length/2
        ax.add_patch(Circle((player_x, player_y), 0.3, fill=True, color='yellow'))
        ax.text(player_x, player_y, str(player['jersey']), ha='center', va='center', color='black')
        
        # Plot heat map of selected zone type
        zones = player[f'{zone_type}_zones'][f'{zone_type}_zone']
        for zone in zones:
            if zone['points'] > 0:
                zone_x, zone_y = get_zone_coordinates(zone['zone_id'], court_width, court_length)
                color = 'green' if zone_type == 'strong' else 'red'
                ax.add_patch(Rectangle((zone_x-0.5, zone_y-0.5), 1, 1, fill=True, alpha=0.3, color=color))
                ax.text(zone_x, zone_y, str(zone['points']), ha='center', va='center', color='white')
        
        # Set title
        plt.title(f"{player['name']} - {zone_type.capitalize()} Zones", fontsize=16, pad=20)
    else:
        plt.title(f"Player with ID {player_id} not found", fontsize=16, pad=20)
    
    # Set axis limits and remove ticks
    ax.set_xlim(0, court_width)
    ax.set_ylim(0, court_length)
    ax.set_xticks([])
    ax.set_yticks([])
    
    plt.tight_layout()
    plt.show()

# Usage
file_path = '../1_DATA/DATA__kaggle_match/Match_Data/2017/410.json'  # Make sure this file is in the same directory as your script
data = load_json_data(file_path)

# Example usage: Plot strong zones for player with ID 41 (Deepak Hooda)
plot_kabaddi_court_with_player_data(data, player_id=106, zone_type='strong')

# To plot weak zones for the same player, you would use:
# plot_kabaddi_court_with_player_data(data, player_id=41, zone_type='weak')
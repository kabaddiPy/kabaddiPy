import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, Circle
import json
import os


def load_json_data(file_path):
    with open(file_path, 'r') as file:
        return json.loads(file.read())


def get_zone_coordinates(zone_id, court_width, court_length):
    zones = {
        1: (0.5, court_length / 2),  # Left Lobby
        2: (court_width - 0.5, court_length / 2),  # Right Lobby
        3: (court_width / 4, court_length - 0.5),  # Midline Left
        4: (court_width / 2, court_length - 0.5),  # Midline Centre
        5: (3 * court_width / 4, court_length - 0.5),  # Midline Right
        6: (court_width / 4, (3 * court_length / 4) - 0.5),  # Baulk Left
        7: (court_width / 2, (3 * court_length / 4) - 0.5),  # Baulk Centre
        8: (3 * court_width / 4, (3 * court_length / 4) - 0.5),  # Baulk Right
        9: (court_width / 4, 0.5),  # Bonus Left
        10: (court_width / 2, 0.5),  # Bonus Centre
        11: (3 * court_width / 4, 0.5),  # Bonus Right
    }
    return zones.get(zone_id, (court_width / 2, court_length / 2))


def aggregate_player_data(directory_path, player_id):
    player_data = None
    strong_zones = {i: 0 for i in range(1, 12)}
    weak_zones = {i: 0 for i in range(1, 12)}

    for filename in os.listdir(directory_path):
        if filename.endswith('.json'):
            file_path = os.path.join(directory_path, filename)
            data = load_json_data(file_path)
            data = data['gameData']
            teams = data['teams']['team']
            for team in teams:
                for player in team['squad']:
                    if player['id'] == player_id:
                        if not player_data:
                            player_data = player

                        for zone in player['strong_zones']['strong_zone']:
                            strong_zones[zone['zone_id']] += zone['points']
                            # print(strong_zones)

                        for zone in player['weak_zones']['weak_zone']:
                            weak_zones[zone['zone_id']] += zone['points']


    return player_data, strong_zones, weak_zones


def plot_player_zones(directory_path, player_id, zone_type='strong'):
    player_data, strong_zones, weak_zones = aggregate_player_data(directory_path, player_id)

    if not player_data:
        print(f"Player with ID {player_id} not found in any match data.")
        return

    fig, ax = plt.subplots(figsize=(15, 12))
    court_width, court_length = 13, 10

    court_color = '#4169E1'  # Royal Blue
    lobby_color = '#B22222'  # Firebrick Red

    # Draw court (main play area)
    ax.add_patch(Rectangle((1, 0), court_width - 2, court_length / 2, fill=True, color=court_color))

    # Draw lobbies
    ax.add_patch(Rectangle((0, 0), 1, court_length / 2, fill=True, color=lobby_color))
    ax.add_patch(Rectangle((court_width - 1, 0), 1, court_length / 2, fill=True, color=lobby_color))

    # Draw lines
    line_color = 'white'
    ax.axhline(y=court_length / 2, color=line_color, linewidth=2)
    ax.axhline(y=3.75, color=line_color, linewidth=2)
    ax.axhline(y=1, color=line_color, linewidth=2)

    ax.text(court_width / 2, court_length / 2, 'Mid Line', ha='center', va='center', color='black', fontsize=14)
    ax.text(court_width / 2, 3.75, 'Baulk Line', ha='center', va='bottom', color='black', fontsize=14)
    ax.text(court_width / 2, 1, 'Bonus Line', ha='center', va='bottom', color='black', fontsize=14)
    ax.text(0.5, (court_length / 4) - 0.2, 'Left Lobby', ha='center', va='center', color='black', fontsize=14)
    ax.text(court_width - 0.5, (court_length / 4) - 0.2, 'Right Lobby', ha='center', va='center', color='black',
            fontsize=14)

    # Plot player position (center of the court for simplicity)
    player_x, player_y = court_width / 2, (court_length / 2) - 2.5
    ax.add_patch(Circle((player_x, player_y), 0.25, fill=True, color='yellow'))
    ax.text(player_x, player_y + 0.1, str(player_data['jersey']), ha='center', va='center', color='black', fontsize=14)
    ax.text(player_x + 0.01, player_y - 0.1, 'Jersey', ha='center', va='center', color='black', fontsize=12)

    # Plot heat map of selected zone type
    zones = strong_zones if zone_type == 'strong' else weak_zones
    max_points = max(zones.values())
    non_zero_values = filter(lambda x: x > 0, zones.values())
    min_points = min(non_zero_values, default=1)

    for zone_id, points in zones.items():
        if points > 0:
            zone_x, zone_y = get_zone_coordinates(zone_id, court_width, court_length / 2)
            color = 'green' if zone_type == 'strong' else 'red'
            intensity = points / max_points
            if zone_type == 'weak':
                intensity = min_points / points

            ax.add_patch(Rectangle((zone_x - 0.5, zone_y), 1, 0.5, fill=True, alpha=intensity, color=color))
            ax.text(zone_x, zone_y + 0.2, str(points), ha='center', va='center', color='white', fontsize=14)

    # Set title
    plt.title(f"{player_data['name']} - Season {zone_type.capitalize()} Zones", fontsize=16, pad=20)

    # Set axis limits and remove ticks
    ax.set_xlim(0, court_width)
    ax.set_ylim(0, court_length / 2)
    ax.set_xticks([])
    ax.set_yticks([])

    plt.tight_layout()
    plt.show()


def aggregate_team_data(directory_path, team_id):
    team_data = None
    team_id = str(team_id)
    strong_zones = {i: 0 for i in range(1, 12)}
    weak_zones = {i: 0 for i in range(1, 12)}

    for filename in os.listdir(directory_path):
        if filename.endswith('.json'):
            file_path = os.path.join(directory_path, filename)
            data = load_json_data(file_path)
            data = data['gameData']
            teams = data['teams']['team']
            for team in teams:
                if team['id'] == team_id:
                    if not team_data:
                        team_data = team

                    for player in team['squad']:
                        for zone in player['strong_zones']['strong_zone']:
                            strong_zones[zone['zone_id']] += zone['points']

                        for zone in player['weak_zones']['weak_zone']:
                            weak_zones[zone['zone_id']] += zone['points']

    return team_data, strong_zones, weak_zones


def plot_team_zones(directory_path, team_id, zone_type='strong'):
    team_data, strong_zones, weak_zones = aggregate_team_data(directory_path, team_id)
    team_id = str(team_id)
    if not team_data:
        print(f"Team with ID {team_id} not found in any match data.")
        return

    fig, ax = plt.subplots(figsize=(15, 12))
    court_width, court_length = 13, 10

    court_color = '#4169E1'  # Royal Blue
    lobby_color = '#B22222'  # Firebrick Red

    # Draw court (main play area)
    ax.add_patch(Rectangle((1, 0), court_width - 2, court_length / 2, fill=True, color=court_color))

    # Draw lobbies
    ax.add_patch(Rectangle((0, 0), 1, court_length / 2, fill=True, color=lobby_color))
    ax.add_patch(Rectangle((court_width - 1, 0), 1, court_length / 2, fill=True, color=lobby_color))

    # Draw lines
    line_color = 'white'
    ax.axhline(y=court_length / 2, color=line_color, linewidth=2)
    ax.axhline(y=3.75, color=line_color, linewidth=2)
    ax.axhline(y=1, color=line_color, linewidth=2)

    ax.text(court_width / 2, court_length / 2, 'Mid Line', ha='center', va='center', color='black', fontsize=14)
    ax.text(court_width / 2, 3.75, 'Baulk Line', ha='center', va='bottom', color='black', fontsize=14)
    ax.text(court_width / 2, 1, 'Bonus Line', ha='center', va='bottom', color='black', fontsize=14)
    ax.text(0.5, (court_length / 4) - 0.2, 'Left Lobby', ha='center', va='center', color='black', fontsize=14)
    ax.text(court_width - 0.5, (court_length / 4) - 0.2, 'Right Lobby', ha='center', va='center', color='black',
            fontsize=14)

    # Plot player position (center of the court for simplicity)
    player_x, player_y = court_width / 2, (court_length / 2) - 2.5
    ax.add_patch(Circle((player_x, player_y), 0.25, fill=True, color='yellow'))
    # ax.text(player_x, player_y + 0.1, str(player_data['jersey']), ha='center', va='center', color='black', fontsize=14)
    ax.text(player_x + 0.01, player_y - 0.1, 'Jersey', ha='center', va='center', color='black', fontsize=12)

    # Plot heat map of selected zone type
    zones = strong_zones if zone_type == 'strong' else weak_zones
    max_points = max(zones.values())
    non_zero_values = filter(lambda x: x > 0, zones.values())
    min_points = min(non_zero_values, default=1)

    for zone_id, points in zones.items():
        if points > 0:
            zone_x, zone_y = get_zone_coordinates(zone_id, court_width, court_length / 2)
            color = 'green' if zone_type == 'strong' else 'red'
            intensity = points / max_points
            if zone_type == 'weak':
                intensity = min_points / points

            ax.add_patch(Rectangle((zone_x - 0.5, zone_y), 1, 0.5, fill=True, alpha=intensity, color=color))
            ax.text(zone_x, zone_y + 0.2, str(points), ha='center', va='center', color='white', fontsize=14)

    # Set title
    # plt.title(f"{player_data['name']} - Season {zone_type.capitalize()} Zones", fontsize=16, pad=20)

    # Set axis limits and remove ticks
    ax.set_xlim(0, court_width)
    ax.set_ylim(0, court_length / 2)
    ax.set_xticks([])
    ax.set_yticks([])

    plt.tight_layout()
    plt.show()

def load_json_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def plot_point_progression(file_path):
    # Load the JSON data
    data = load_json_data(file_path)
    teams = data['gameData']['teams']

    # team1_id = 31
    # team2_id = 2
    events = data['gameData']['events']['event']

    team1_id = None
    team2_id = None
    team1_total_points = [0]
    team2_total_points = [0]

    for event in events:
        if team1_id is None:
            team1_id = event['raiding_team_id']
        if team2_id is None:
            team2_id = event['defending_team_id']
        if 'raid_points' in event:
            if event['raid_points'] > 0:
                if event['raiding_team_id'] == team1_id:
                    team1_total_points.append(team1_total_points[-1] + event['raid_points'])
                    team2_total_points.append(team2_total_points[-1] + event['defending_points'])
                else:
                    team1_total_points.append(team1_total_points[-1] + event['defending_points'])
                    team2_total_points.append(team2_total_points[-1] + event['raid_points'])
            elif event['defending_points'] > 0:
                if event['defending_team_id'] == team1_id:
                    team1_total_points.append(team1_total_points[-1] + event['defending_points'])
                    team2_total_points.append(team2_total_points[-1] + event['raid_points'])
                else:
                    team1_total_points.append(team1_total_points[-1] + event['raid_points'])
                    team2_total_points.append(team2_total_points[-1] + event['defending_points'])
            else:
                team1_total_points.append(team1_total_points[-1])
                team2_total_points.append(team2_total_points[-1])
        else:
            team1_total_points.append(team1_total_points[-1])
            team2_total_points.append(team2_total_points[-1])

    x = range(len(team1_total_points))
    plt.figure(figsize=(12, 6))
    plt.plot(x, team1_total_points, label=f'Team {team1_id}')
    plt.plot(x, team2_total_points, label=f'Team {team2_id}')
    plt.xlabel('Event')
    plt.ylabel('Total Points')
    plt.title('Team Point Progression')
    plt.legend()
    plt.show()
# Usage
if __name__=="__main__":

    #directory_path = r"C:\Users\KIIT\Documents\ProKabaddi_API\pypi\prokabaddidata\MatchData_pbp\other-data\old_data\Season_PKL_Season_5_2017"
    directory_path = r"C:\Users\KIIT\Documents\ProKabaddi_API\pypi\prokabaddidata\MatchData_pbp\Season_PKL_Season_5_2017"
    player_id = 143  # Example: Deepak Hooda

    plot_player_zones(directory_path,player_id,zone_type='strong')
    plot_player_zones(directory_path,player_id,zone_type='weak')
    # player_data, strong_zones, weak_zones = aggregate_player_data(directory_path, player_id)
    # print(strong_zones)
    plot_team_zones(directory_path, 4, zone_type='strong')
    plot_team_zones(directory_path, 4, zone_type='weak')

    plot_point_progression(r"C:\Users\KIIT\Documents\ProKabaddi_API\pypi\prokabaddidata\MatchData_pbp\Season_PKL_Season_5_2017\32_Match_32_ID_317.json")
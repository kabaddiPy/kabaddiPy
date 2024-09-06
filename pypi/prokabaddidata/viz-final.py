import math
from math import ceil

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, Circle
import json
import os
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib import cm
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, Circle, Wedge
from matplotlib.colors import LinearSegmentedColormap
from matplotlib import cm


def load_json_data(file_path):
    with open(file_path, 'r') as file:
        return json.loads(file.read())


# def get_zone_coordinates(zone_id, court_width, court_length):
#     zones = {
#         1: (0.5, court_length / 2),  # Left Lobby
#         2: (court_width - 0.5, court_length / 2),  # Right Lobby
#         3: (court_width / 4, court_length - 0.5),  # Midline Left
#         4: (court_width / 2, court_length - 0.5),  # Midline Centre
#         5: (3 * court_width / 4, court_length - 0.5),  # Midline Right
#         6: (court_width / 4, (3 * court_length / 4) - 0.5),  # Baulk Left
#         7: (court_width / 2, (3 * court_length / 4) - 0.5),  # Baulk Centre
#         8: (3 * court_width / 4, (3 * court_length / 4) - 0.5),  # Baulk Right
#         9: (court_width / 4, 0.5),  # Bonus Left
#         10: (court_width / 2, 0.5),  # Bonus Centre
#         11: (3 * court_width / 4, 0.5),  # Bonus Right
#     }
#     return zones.get(zone_id, (court_width / 2, court_length / 2))

def internal_plot_player_zones_improved(player_id, season, zone_type='strong', fig=None, ax=None):
    season_directories = {
        1: "Season_PKL_Season_1_2014", 2: "Season_PKL_Season_2_2015", 3: "Season_PKL_Season_3_2016",
        4: "Season_PKL_Season_4_2016",
        5: "Season_PKL_Season_5_2017", 6: "Season_PKL_Season_6_2018", 7: "Season_PKL_Season_7_2019",
    }
    if season not in season_directories:
        raise ValueError(f"Invalid season number. Available seasons are: {list(season_directories.keys())}")

    directory_path = f"./MatchData_pbp/{season_directories[season]}"

    player_data, strong_zones, weak_zones = aggregate_player_data(directory_path, player_id)

    if not player_data:
        print(f"Player with ID {player_id} not recorded for any match data.")
        return

    # fig, ax = plt.subplots(figsize=(12, 8))
    if ax is None:
        fig, ax = plt.subplots(figsize=(6, 4))
    court_width, court_length = 13, 10

    # Custom color schemes
    court_color = '#E6F3FF'  # Light blue for court
    lobby_color = '#FFE6E6'  # Light red for lobby
    line_color = '#333333'  # Dark gray for lines

    # Draw court (main play area)
    ax.add_patch(Rectangle((1, 0), court_width - 2, court_length, fill=True, color=court_color, ec=line_color, lw=2))

    # Draw lobbies
    ax.add_patch(Rectangle((0, 0), 1, court_length, fill=True, color=lobby_color, ec=line_color, lw=2))
    ax.add_patch(Rectangle((court_width - 1, 0), 1, court_length, fill=True, color=lobby_color, ec=line_color, lw=2))

    # Draw lines
    ax.axhline(y=court_length, color=line_color, linewidth=2)
    ax.axhline(y=3 * court_length / 4, color=line_color, linewidth=2)
    ax.axhline(y=1, color=line_color, linewidth=2)

    # Line Labels
    label_style = {'ha': 'center', 'va': 'center', 'color': line_color, 'fontsize': 10, 'fontweight': 'bold'}
    ax.text(court_width / 2, court_length + 0.2, 'Mid Line', **label_style)
    ax.text(court_width / 2, 3 * court_length / 4 + 0.2, 'Baulk Line', **label_style)
    ax.text(court_width / 2, 0.8, 'Bonus Line', **label_style)
    ax.text(0.5, court_length / 2, 'Left\nLobby', **label_style)
    ax.text(court_width - 0.5, court_length / 2, 'Right\nLobby', **label_style)

    # Plot player position
    player_x, player_y = court_width / 2, court_length / 2
    jersey_circle = Circle((player_x, player_y), 0.5, fill=True, facecolor='#FFD700', edgecolor=line_color, linewidth=2,
                           zorder=10)
    ax.add_patch(jersey_circle)
    ax.text(player_x, player_y, str(player_data['jersey']), ha='center', va='center', color=line_color, fontsize=14,
            fontweight='bold', zorder=11)

    # Plot heat map of selected zone type
    zones = strong_zones if zone_type == 'strong' else weak_zones
    max_points = max(zones.values())
    non_zero_values = [v for v in zones.values() if v > 0]
    min_points = min(non_zero_values) if non_zero_values else 1

    # Custom color maps with increased contrast
    if zone_type == 'strong':
        colors = ['#E6FFE6', '#66FF66', '#00CC00', '#006400']
    else:
        colors = ['#FFE6E6', '#FF9999', '#FF3333', '#8B0000']
    n_bins = 100
    cmap = LinearSegmentedColormap.from_list('custom', colors, N=n_bins)

    # Plot zones
    for zone_id, points in zones.items():
        if points > 0:
            zone_x, zone_y = get_zone_coordinates(zone_id, court_width, court_length)
            intensity = (points - min_points) / (max_points - min_points)
            color = cmap(intensity)

            if zone_id in [1, 2]:  # Lobby zones
                if zone_id == 1:  # Left lobby
                    wedge = Wedge((1, court_length / 2), 0.9, 90, 270, color=color, alpha=0.7, ec=line_color, lw=1,
                                  zorder=5)
                else:  # Right lobby
                    wedge = Wedge((court_width - 1, court_length / 2), 0.9, 270, 90, color=color, alpha=0.7,
                                  ec=line_color, lw=1, zorder=5)
                ax.add_patch(wedge)
            else:  # Inner court zones
                circle = Circle((zone_x, zone_y), 0.9, fill=True, color=color, alpha=0.7, ec=line_color, lw=1, zorder=5)
                ax.add_patch(circle)

            ax.text(zone_x, zone_y, str(points), ha='center', va='center', color='white', fontsize=10,
                    fontweight='bold', zorder=6)

    # Set axis limits and remove ticks
    ax.set_xlim(0, court_width)
    ax.set_ylim(0, court_length)
    ax.set_xticks([])
    ax.set_yticks([])

    # plt.tight_layout()
    # plt.show()
    return fig, ax


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


def plot_player_zones_improved(player_id, season, zone_type='strong'):
    season_directories = {
        1: "Season_PKL_Season_1_2014", 2: "Season_PKL_Season_2_2015", 3: "Season_PKL_Season_3_2016",
        4: "Season_PKL_Season_4_2016",
        5: "Season_PKL_Season_5_2017", 6: "Season_PKL_Season_6_2018", 7: "Season_PKL_Season_7_2019",
    }
    if season not in season_directories:
        raise ValueError(f"Invalid season number. Available seasons are: {list(season_directories.keys())}")

    directory_path = f"./MatchData_pbp/{season_directories[season]}"

    player_data, strong_zones, weak_zones = aggregate_player_data(directory_path, player_id)

    if not player_data:
        print(f"Player with ID {player_id} not found in any match data.")
        return

    fig, ax = plt.subplots(figsize=(12, 8))
    court_width, court_length = 13, 10

    # Custom color schemes
    court_color = '#E6F3FF'  # Light blue for court
    lobby_color = '#FFE6E6'  # Light red for lobby
    line_color = '#333333'  # Dark gray for lines

    # Draw court (main play area)
    ax.add_patch(Rectangle((1, 0), court_width - 2, court_length, fill=True, color=court_color, ec=line_color, lw=2))

    # Draw lobbies
    ax.add_patch(Rectangle((0, 0), 1, court_length, fill=True, color=lobby_color, ec=line_color, lw=2))
    ax.add_patch(Rectangle((court_width - 1, 0), 1, court_length, fill=True, color=lobby_color, ec=line_color, lw=2))

    # Draw lines
    ax.axhline(y=court_length, color=line_color, linewidth=2)
    ax.axhline(y=3 * court_length / 4, color=line_color, linewidth=2)
    ax.axhline(y=1, color=line_color, linewidth=2)

    # Line Labels
    label_style = {'ha': 'center', 'va': 'center', 'color': line_color, 'fontsize': 10, 'fontweight': 'bold'}
    ax.text(court_width / 2, court_length + 0.2, 'Mid Line', **label_style)
    ax.text(court_width / 2, 3 * court_length / 4 + 0.2, 'Baulk Line', **label_style)
    ax.text(court_width / 2, 0.8, 'Bonus Line', **label_style)
    ax.text(0.5, court_length / 2, 'Left\nLobby', **label_style)
    ax.text(court_width - 0.5, court_length / 2, 'Right\nLobby', **label_style)

    # Plot player position
    player_x, player_y = court_width / 2, court_length / 2
    jersey_circle = Circle((player_x, player_y), 0.5, fill=True, facecolor='#FFD700', edgecolor=line_color, linewidth=2,
                           zorder=10)
    ax.add_patch(jersey_circle)
    ax.text(player_x, player_y, str(player_data['jersey']), ha='center', va='center', color=line_color, fontsize=14,
            fontweight='bold', zorder=11)

    # Plot heat map of selected zone type
    zones = strong_zones if zone_type == 'strong' else weak_zones
    max_points = max(zones.values())
    non_zero_values = [v for v in zones.values() if v > 0]
    min_points = min(non_zero_values) if non_zero_values else 1

    # Custom color maps with increased contrast
    if zone_type == 'strong':
        colors = ['#E6FFE6', '#66FF66', '#00CC00', '#006400']
    else:
        colors = ['#FFE6E6', '#FF9999', '#FF3333', '#8B0000']
    n_bins = 100
    cmap = LinearSegmentedColormap.from_list('custom', colors, N=n_bins)

    # Plot zones
    for zone_id, points in zones.items():
        if points > 0:
            zone_x, zone_y = get_zone_coordinates(zone_id, court_width, court_length)
            intensity = (points - min_points) / (max_points - min_points)
            color = cmap(intensity)

            if zone_id in [1, 2]:  # Lobby zones
                if zone_id == 1:  # Left lobby
                    wedge = Wedge((1, court_length / 2), 0.9, 90, 270, color=color, alpha=0.7, ec=line_color, lw=1,
                                  zorder=5)
                else:  # Right lobby
                    wedge = Wedge((court_width - 1, court_length / 2), 0.9, 270, 90, color=color, alpha=0.7,
                                  ec=line_color, lw=1, zorder=5)
                ax.add_patch(wedge)
            else:  # Inner court zones
                circle = Circle((zone_x, zone_y), 0.9, fill=True, color=color, alpha=0.7, ec=line_color, lw=1, zorder=5)
                ax.add_patch(circle)

            ax.text(zone_x, zone_y, str(points), ha='center', va='center', color='white', fontsize=10,
                    fontweight='bold', zorder=6)

    # Set title
    plt.title(f"{player_data['name']} - Season {zone_type.capitalize()} Zones", fontsize=16, fontweight='bold', pad=20)

    # Set axis limits and remove ticks
    ax.set_xlim(0, court_width)
    ax.set_ylim(0, court_length)
    ax.set_xticks([])
    ax.set_yticks([])

    plt.tight_layout()
    plt.show()


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


def plot_team_zones(team_id, season, zone_type='strong'):
    season_directories = {
        1: "Season_PKL_Season_1_2014", 2: "Season_PKL_Season_2_2015", 3: "Season_PKL_Season_3_2016",
        4: "Season_PKL_Season_4_2016",
        5: "Season_PKL_Season_5_2017", 6: "Season_PKL_Season_6_2018", 7: "Season_PKL_Season_7_2019",
    }
    if season not in season_directories:
        raise ValueError(f"Invalid season number. Available seasons are: {list(season_directories.keys())}")

    directory_path = f"./MatchData_pbp/{season_directories[season]}"

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


# def load_json_data(file_path):
#     with open(file_path, 'r') as file:
#         return json.load(file)

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


def plot_player_zones_grid(player_ids, season, zone_type='strong', max_cols=4):
    n_plots = len(player_ids)

    valid_plots = []
    for player_id in player_ids:
        try:
            # Create a temporary figure that won't be displayed
            temp_fig, temp_ax = plt.subplots()
            result = internal_plot_player_zones_improved(player_id, season, zone_type, fig=temp_fig, ax=temp_ax)
            if result is not None:
                valid_plots.append(player_id)
            else:
                print(f"Skipping player {player_id}: Function returned None")
            # Close the temporary figure to prevent it from being displayed
            plt.close(temp_fig)
        except Exception as e:
            print(f"Error plotting player {player_id}: {str(e)}")

    n_valid = len(valid_plots)

    if n_valid == 0:
        print("No valid plots to display.")
        return

    # Calculate optimal grid size
    cols = min(max_cols, n_valid)
    rows = math.ceil(n_valid / cols)

    fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 4 * rows))
    fig.suptitle(f"Player Zone Plots - Season {season}", fontsize=16)

    axes = axes.flatten() if isinstance(axes, np.ndarray) else [axes]

    for i, (ax, player_id) in enumerate(zip(axes, valid_plots)):
        result = internal_plot_player_zones_improved(player_id, season, zone_type, fig=fig, ax=ax)
        if result is not None:
            ax.set_title(f"Player ID: {player_id}", fontsize=10)

    # Remove any unused subplots
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # directory_path = r"C:\Users\KIIT\Documents\ProKabaddi_API\pypi\prokabaddidata\MatchData_pbp\other-data\old_data\Season_PKL_Season_5_2017"
    directory_path = r"./MatchData_pbp/Season_PKL_Season_5_2017"
    player_id = 143  # Example: Deepak Hooda

    # plot_player_zones_improved(player_id,season=5,zone_type='strong')
    # # plot_player_zones_improved(directory_path,player_id,zone_type='weak')
    # # player_data, strong_zones, weak_zones = aggregate_player_data(directory_path, player_id)
    # # print(strong_zones)
    # plot_team_zones(5,season=5, zone_type='strong')
    # plot_team_zones(5,season=5, zone_type='weak')
    #plot_point_progression(r"C:\Users\KIIT\Documents\kabaddiPy\pypi\prokabaddidata\MatchData_pbp\Season_PKL_Season_10_2023 __ MATCH 1 MISSING\12_Match_12_ID_3040.json")
    column_list = [143, 3176, 219, 621, 3084, 111]
    plot_player_zones_grid(column_list, season=5, zone_type='strong', max_cols=2)


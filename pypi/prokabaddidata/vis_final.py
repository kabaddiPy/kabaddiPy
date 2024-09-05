import math
import json
from matplotlib.patches import Rectangle, Circle, Wedge
from matplotlib.colors import LinearSegmentedColormap
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.patches import Patch
from setuptools.command.rotate import rotate


def load_json_data(file_path):
    with open(file_path, 'r') as file:
        return json.loads(file.read())

def internal_plot_player_grid(player_id, season, zone_type='strong', fig=None, ax=None):
    season_directories = {
        1: "Season_PKL_Season_1_2014", 2: "Season_PKL_Season_2_2015", 3: "Season_PKL_Season_3_2016",
        4: "Season_PKL_Season_4_2016",
        5: "Season_PKL_Season_5_2017", 6: "Season_PKL_Season_6_2018", 7: "Season_PKL_Season_7_2019",
    }
    if season not in season_directories:
        raise ValueError(f"Invalid season number. Available seasons are: {list(season_directories.keys())}")

    directory_path = f"./MatchData_pbp/{season_directories[season]}"

    player_data, strong_zones, weak_zones = internal_aggregate_player_data(directory_path, player_id)

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
    ax.text(0.5, court_length / 2, 'Left Lobby', **label_style)
    ax.text(court_width - 0.5, court_length / 2, 'Right Lobby', **label_style)

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


def internal_aggregate_player_data(directory_path, player_id):
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


def plot_player_zones_improved(player_id, season, zone_type='strong'):
    season_directories = {
        1: "Season_PKL_Season_1_2014", 2: "Season_PKL_Season_2_2015", 3: "Season_PKL_Season_3_2016",
        4: "Season_PKL_Season_4_2016",
        5: "Season_PKL_Season_5_2017", 6: "Season_PKL_Season_6_2018", 7: "Season_PKL_Season_7_2019",
    }
    if season not in season_directories:
        raise ValueError(f"Invalid season number. Available seasons are: {list(season_directories.keys())}")

    directory_path = f"./MatchData_pbp/{season_directories[season]}"

    player_data, strong_zones, weak_zones = internal_aggregate_player_data(directory_path, player_id)

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


def plot_point_progression(season, match_id):
    file_path= "./MatchData_pbp/"

    for dir in os.listdir(file_path):
        if f"Season_{season}" in dir:
            file_path = file_path + dir + "/"
            break

    for match in os.listdir(file_path):
        if f"ID_{match_id}" in match:
            file_path = file_path + match

    print(file_path)

    data = load_json_data(file_path)
    teams = data['gameData'].get('teams', [])
    events = data['gameData']['events']['event']

    team1_id = None
    team2_id = None
    team1_total_points = [0]  # Starting from 0 for Team 1
    team2_total_points = [0]  # Starting from 0 for Team 2
    raid_events = []

    for i, event in enumerate(events):
        if team1_id is None:
            team1_id = event['raiding_team_id']
        if team2_id is None:
            team2_id = event['defending_team_id']

        if 'raid_points' in event:
            if event['raid_points'] > 0 or event['defending_points'] > 0:
                raid_events.append(i)

            if event['raiding_team_id'] == team1_id:
                team1_total_points.append(team1_total_points[-1] + event['raid_points'])
                team2_total_points.append(team2_total_points[-1] + event['defending_points'])
            else:
                team1_total_points.append(team1_total_points[-1] + event['defending_points'])
                team2_total_points.append(team2_total_points[-1] + event['raid_points'])
        else:
            team1_total_points.append(team1_total_points[-1])
            team2_total_points.append(team2_total_points[-1])

    # Create the plot
    fig, ax = plt.subplots(figsize=(15, 8))
    x = range(len(team1_total_points))

    # Plot the lines with gradients
    team1_color = '#FF9999'
    team2_color = '#66B2FF'

    team_id_map = {
        4: 'Bengal Warriors',
        1: 'Bengaluru Bulls',
        2: 'Dabang Delhi',
        31: 'Gujarat Giants',
        28: 'Haryana Steelers',
        6: 'Patna Pirates',
        7: 'Puneri Paltan',
        29: 'Tamil Thalaivas',
        5: 'U Mumba',
        30: 'U.P. Yoddha',
        3: "Jaipur Pink Panthers"
    }

    ax.plot(x, team1_total_points, label=f'Team {team_id_map[int(team1_id)]}', color=team1_color, linewidth=2.5)
    ax.plot(x, team2_total_points, label=f'Team {team_id_map[int(team2_id)]}', color=team2_color, linewidth=2.5)

    # Fill the area under the curves
    ax.fill_between(x, team1_total_points, alpha=0.3, color=team1_color)
    ax.fill_between(x, team2_total_points, alpha=0.3, color=team2_color)

    # Highlight raid events
    for raid in raid_events:
        ax.axvline(x=raid, color='gray', alpha=0.3, linestyle='--')

    # Customize the plot
    ax.set_xlabel('Events', fontsize=12, fontweight='bold')
    ax.set_ylabel('Total Points', fontsize=12, fontweight='bold')
    ax.set_title(f'Point Progression for Match {match_id}', fontsize=16, fontweight='bold')

    # Add a grid
    ax.grid(False, linestyle='--', alpha=0.7)

    # Set axis limits to start at (0, 0)
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)

    # Customize tick labels
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    # Add team names to the legend
    team1_name = get_team_name(teams, team1_id)
    team2_name = get_team_name(teams, team2_id)
    legend_elements = [
        Patch(facecolor=team1_color, edgecolor=team1_color, label=f'{team_id_map[team1_id]} (Team {team1_id})'),
        Patch(facecolor=team2_color, edgecolor=team2_color, label=f'{team_id_map[team2_id]} (Team {team2_id})'),
        

    ]
    ax.legend(handles=legend_elements, loc='upper left', fontsize=10)

    # Add final scores
    final_score_text = f"Final Score: {team_id_map[team1_id]} {team1_total_points[-1]} - {team2_total_points[-1]} {team_id_map[team2_id]}"
    ax.text(0.5, -0.1, final_score_text, ha='center', va='center', transform=ax.transAxes, fontsize=12,
            fontweight='bold')

    # Threshold part to highlight significant score differences
    max_diff = max(abs(np.array(team1_total_points) - np.array(team2_total_points)))
    threshold = max_diff * 0.95  # Highlight differences that are 95% of the maximum difference

    for i in range(1, len(team1_total_points)):
        diff = team1_total_points[i] - team2_total_points[i]
        if abs(diff) >= threshold:
            ax.annotate(f"Δ{abs(diff)}", (i, max(team1_total_points[i], team2_total_points[i])),
                        xytext=(0, 10), textcoords='offset points', ha='center', va='bottom',
                        bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
                        arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

    plt.tight_layout()
    plt.show()

def get_team_name(teams, team_id):
    """Helper function to get team name safely."""
    for team in teams:
        if isinstance(team, dict) and team.get('id') == team_id:
            return team.get('name', f'Team {team_id}')
    return f'Team {team_id}'

def plot_player_zones_grid(player_ids, season, zone_type='strong', max_cols=4):

    n_plots = len(player_ids)

    valid_plots = []
    for player_id in player_ids:
        try:
            # Create a temporary figure that won't be displayed
            temp_fig, temp_ax = plt.subplots()
            result = internal_plot_player_grid(player_id, season, zone_type, fig=temp_fig, ax=temp_ax)
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
        result = internal_plot_player_grid(player_id, season, zone_type, fig=fig, ax=ax)
        if result is not None:
            ax.set_title(f"Player ID: {player_id}", fontsize=10)

    # Remove any unused subplots
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # directory_path = r"C:\Users\KIIT\Documents\ProKabaddi_API\pypi\prokabaddidata\MatchData_pbp\other-data\old_data\Season_PKL_Season_5_2017"
    # directory_path = r"./MatchData_pbp/Season_PKL_Season_5_2017"
    player_id = 143  # Example: Deepak Hooda

    # plot_player_zones_improved(player_id,season=5,zone_type='strong')
    # # plot_player_zones_improved(directory_path,player_id,zone_type='weak')
    # # player_data, strong_zones, weak_zones = internal_aggregate_player_data(directory_path, player_id)
    # # print(strong_zones)
    # plot_team_zones(5,season=5, zone_type='strong')
    # plot_team_zones(5,season=5, zone_type='weak')

    plot_player_zones_improved(player_id, season=5, zone_type='strong')
    plot_player_zones_improved(player_id, season=5, zone_type='weak')
    # player_data, strong_zones, weak_zones = internal_aggregate_player_data(directory_path, player_id)
    # print(strong_zones)
    plot_team_zones(5, season=5, zone_type='strong')
    plot_team_zones(5, season=5, zone_type='weak')

    # plot_point_progression(r"./MatchData_pbp/Season_PKL_Season_5_2017/32_Match_32_ID_317.json", season=5, match_id=317)
    plot_point_progression(season=10, match_id=3164)

    column_list = [143, 3176, 219, 621, 3084, 111]
    plot_player_zones_grid(column_list, season=5, zone_type='strong', max_cols=2)

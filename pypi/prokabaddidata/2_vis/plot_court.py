import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def plot_kabaddi_court():
    fig, ax = plt.subplots(figsize=(10, 12))
    
    # Court dimensions
    court_width = 13
    court_length = 10
    
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
    # Mid line
    ax.axhline(y=court_length/2, color=line_color, linewidth=2)
    # Baulk lines
    ax.axhline(y=3.75, color=line_color, linewidth=2)
    ax.axhline(y=court_length-3.75, color=line_color, linewidth=2)
    # Bonus lines
    ax.axhline(y=1, color=line_color, linewidth=2)
    ax.axhline(y=court_length-1, color=line_color, linewidth=2)
    
    # Add labels
    ax.text(court_width/2, court_length/2, 'Mid Line 6.5m from\nEnd Line', ha='center', va='center', color='white')
    ax.text(court_width/2, 3.75, 'Baulk Line', ha='center', va='bottom', color='white')
    ax.text(court_width/2, court_length-3.75, 'Baulk Line', ha='center', va='top', color='white')
    ax.text(court_width/2, 1, 'Bonus Line', ha='center', va='bottom', color='white')
    ax.text(court_width/2, court_length-1, 'Bonus Line', ha='center', va='top', color='white')
    ax.text(0.5, court_length/2, 'Lobby', ha='center', va='center', rotation=90, color='white')
    ax.text(court_width-0.5, court_length/2, 'Lobby', ha='center', va='center', rotation=90, color='white')
    
    # Add measurements
    ax.text(court_width-1.2, 3.75/2, '<3.75m>', ha='right', va='center', color='white', rotation=90)
    ax.text(court_width-1.2, (court_length-3.75/2), '<3.75m>', ha='right', va='center', color='white', rotation=90)
    ax.text(court_width-1.2, 0.5, '<1m>', ha='right', va='center', color='white', rotation=90)
    ax.text(court_width-1.2, court_length-0.5, '<1m>', ha='right', va='center', color='white', rotation=90)
    
    # Set title and subtitle
    plt.title('13m x 10m Kabaddi Court', fontsize=16, pad=20)
    plt.text(court_width/2, -0.5, 'Based on IKF Rules', ha='center', fontsize=12)
    
    # Set axis limits and remove ticks
    ax.set_xlim(0, court_width)
    ax.set_ylim(-1, court_length+1)
    ax.set_xticks([])
    ax.set_yticks([])
    
    plt.tight_layout()
    plt.show()

plot_kabaddi_court()
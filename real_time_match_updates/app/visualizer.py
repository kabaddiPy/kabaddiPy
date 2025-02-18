import matplotlib.pyplot as plt
import os

def plot_team_performance():
    # Sample team performance data
    team_a_performance = [10, 20, 30, 40, 50]
    team_b_performance = [15, 25, 35, 45, 55]
    rounds = [1, 2, 3, 4, 5]
    
    plt.figure()
    plt.plot(rounds, team_a_performance, label="Team A", color='blue', marker='o')
    plt.plot(rounds, team_b_performance, label="Team B", color='red', marker='o')
    plt.xlabel('Rounds')
    plt.ylabel('Performance')
    plt.title('Team Performance Over Time')
    plt.legend()

    chart_path = os.path.join('static', 'team_performance_chart.png')
    plt.savefig(chart_path)
    plt.close()

    return chart_path

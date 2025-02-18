# Assuming you have the necessary libraries installed
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import networkx as nx

# Read the CSV file
data = pd.read_csv('Pypi/kabaddiPy/more visvalisation/csv/combined_data.csv')

# Radar Plot Example
def radar_plot(data):
    categories = list(data.columns[6:9])  # Adjusted to use relevant columns for radar plot
    values = data.loc[0, categories].values.flatten().tolist()
    values += values[:1]  # Repeat the first value to close the circle
    angles = [n / float(len(categories)) * 2 * 3.14159 for n in range(len(categories))]
    angles += angles[:1]

    plt.figure(figsize=(6, 6))
    ax = plt.subplot(111, polar=True)
    ax.fill(angles, values, color='blue', alpha=0.25)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    plt.title('Radar Plot')
    plt.savefig('radar_plot.jpeg', format='jpeg')  # Save as JPEG
    plt.close()  # Close the plot

# Heatmap Example
def heatmap(data):
    # Select only numeric columns for correlation
    numeric_data = data.select_dtypes(include=['number'])
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(numeric_data.corr(), annot=True, cmap='coolwarm')
    plt.title('Heatmap of Correlations')
    plt.savefig('heatmap.jpeg', format='jpeg')  # Save as JPEG
    plt.close()  # Close the plot

# Stacked Bar Chart Example
def stacked_bar_chart(data):
    data.set_index('Team').plot(kind='bar', stacked=True, figsize=(10, 6))  # Assuming 'Team' is a column
    plt.title('Stacked Bar Chart')
    plt.savefig('stacked_bar_chart.jpeg', format='jpeg')  # Save as JPEG
    plt.close()  # Close the plot

# Network Graph Example
def network_graph(data):
    G = nx.Graph()
    for index, row in data.iterrows():
        if pd.notna(row['Defender Name']) and pd.notna(row['Raider Name']):
            G.add_edge(row['Defender Name'], row['Raider Name'])  # Assuming these are the relevant columns
    plt.figure(figsize=(10, 8))
    nx.draw(G, with_labels=True)
    plt.title('Network Graph of Player Cooperation')
    plt.savefig('network_graph.jpeg', format='jpeg')  # Save as JPEG
    plt.close()  # Close the plot

# Match Timeline Visualization Example
def match_timeline(data):
    plt.figure(figsize=(10, 6))
    plt.plot(data['season'], data['Total Tackles'])  # Assuming 'season' and 'Total Tackles' are columns
    plt.title('Match Timeline Visualization')
    plt.xlabel('Season')
    plt.ylabel('Total Tackles')
    plt.savefig('match_timeline.jpeg', format='jpeg')  # Save as JPEG
    plt.close()  # Close the plot

# Interactive Visualization Example
def interactive_visualization(data):
    fig = px.scatter(data, x='Total Tackles', y='Successful Tackles', color='Team')  # Adjust as needed
    fig.write_image('interactive_visualization.jpeg')  # Save as JPEG

# Call the visualization functions
radar_plot(data)
heatmap(data)
stacked_bar_chart(data)
network_graph(data)
match_timeline(data)
interactive_visualization(data)

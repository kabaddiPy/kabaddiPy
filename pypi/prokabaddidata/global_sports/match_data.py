import re
import pandas as pd

# Load the HTML content from the file
file_path = './file.html'
with open(file_path, 'r') as file:
    html_content = file.read()

# Step 1: Extract Dates
dates = re.findall(r'\d{4}-\d{2}-\d{2}', html_content)

# Step 2: Extract Team Names
teams = re.findall(r'team_full">([^<]+)</span>', html_content)

# Step 3: Extract Scores
scores = re.findall(r'match_score"\s*style=".*?">\s*(\d+\s*:\s*\d+)\s*</span>', html_content)

# Step 4: Extract Outcome (W, L, D)
outcomes = re.findall(r'team_form_abbrv" style="background-color:#\w+;">([WLD])</div>', html_content)

# Organize the extracted data
data = []
for i in range(len(teams) // 2):
    match = {
        "Date": dates[i],
        "Team A": teams[i*2],
        "Team B": teams[i*2 + 1],
        "Score": scores[i],
        "Outcome": outcomes[i]
    }
    data.append(match)

# Create the DataFrame
df = pd.DataFrame(data)

print(df)

# # Show the first few rows of the dataframe
# df.head()

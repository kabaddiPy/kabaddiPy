import json
import pandas as pd
import os


def process_json_file(file_path, output_dir):
    with open(file_path, "r") as file:
        data = json.load(file)

    standings_data = data["standings"]
    standings_df = pd.DataFrame([standings_data])

    teams_data = standings_data["groups"][0]["teams"]["team"]
    teams_df = pd.DataFrame(teams_data)

    matches_data = []
    for team in teams_data:
        for match in team["match_result"]["match"]:
            match["team_id"] = team["team_id"]
            matches_data.append(match)
    matches_df = pd.DataFrame(matches_data)

    # Create base filename from the input JSON filename
    base_filename = os.path.splitext(os.path.basename(file_path))[0]


    

    # # Save each dataframe as a CSV
    # standings_df.to_csv(
    #     os.path.join(output_dir, f"{base_filename}_standings.csv"), index=False
    # )
    teams_df.to_csv(os.path.join(output_dir, f"{base_filename}_teams.csv"), index=False)
    matches_df.to_csv(
        os.path.join(output_dir, f"{base_filename}_matches.csv"), index=False
    )

    print(f"CSVs created for {base_filename}")


# Directory containing JSON files
json_dir = "./standings"

# Directory to save CSV files
output_dir = "./standings_csvs"

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Process each JSON file in the directory
for filename in os.listdir(json_dir):
    if filename.endswith(".json"):
        file_path = os.path.join(json_dir, filename)
        process_json_file(file_path, output_dir)

print("All JSON files processed and CSVs created.")

    import os
import json
import pandas as pd





if __name__ == "__main__":
    match_id = "183"
    season = "Pro Kabaddi League Season 4, 2016"

    general_df, participants_df = get_match_overview(match_id, season)

    print("General Details:")
    print(general_df)

    print("\nParticipants:")
    print(participants_df)






# Match data anni

# import json
# import pandas as pd


# # Function to load JSON files from a directory
# # # Function to load JSON files from a directory
# # def load_json_files():
# #     folder_path = "../1_DATA/MatchWise-Data/Matches-Overview"
# #     json_files = []
# #     for file_name in os.listdir(folder_path):
# #         print(os.listdir(folder_path))
        
# #         if file_name.endswith('.json'):
# #             with open(os.path.join(folder_path, file_name)) as f:
# #                 json_files.append(json.load(f))

# #     return json_files


# import os
# import json
# import re

# def load_json_files():
#     folder_path = "../1_DATA/MatchWise-Data/Matches-Overview"
#     json_files = []
#     for file_name in os.listdir(folder_path):
#         if file_name.endswith('.json'):
#             with open(os.path.join(folder_path, file_name)) as f:
#                 json_files.append(json.load(f))
    
#     # Get all JSON files in the directory
#     file_names = [f for f in os.listdir(folder_path) if f.endswith('.json')]
    
#     # Sort the file names by season number
#     sorted_file_names = sorted(file_names, key=lambda x: int(re.search(r's(\d+)', x).group(1)))
    
#     # Load JSON files in the sorted order
#     for file_name in sorted_file_names:
#         with open(os.path.join(folder_path, file_name)) as f:
#             # print(f"Appending {file_name} to the list now.")
#             json_files.append((re.search(r's(\d+)', file_name).group(1) , json.load(f)))

    
#     for j in json_files:
#         print(j[0])

#     return json_files


# @ -20,9 +50,15 @@ def get_match_overview(match_id, season):

#     # Filtering based on season and match_id
#     match_details = None

#     for data in json_files:
#         if data['matches'][0]['tour_name'] == season:

#         data = data[1]
        
#         if f"Season {season}" in data['matches'][0]['tour_name']:
            
#             for match in data['matches']:
                
#                 if match['game_id'] == match_id:
#                     match_details = match
#                     break
# @ -70,9 +106,25 @@ def get_match_overview(match_id, season):
#         return None, None


# def get_all_match_ids():
#     json_files = load_json_files()


    
#     for j in json_files:
#         print(f"Season {j}")
        
        



# if __name__ == "__main__":

#     #TODO: write a function that enables the user to see all the match-ids per season


#     match_id = "60"
#     season = "Pro Kabaddi League Season 1, 2014"
#     season = "1"

#     general_df, participants_df = get_match_overview(match_id, season)

# @ -81,3 +133,10 @@ if __name__ == "__main__":

#     print("\nParticipants:")
#     print(participants_df)


#     print("\n----------\n")




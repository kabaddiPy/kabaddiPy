# kabaddi_data.py
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup
from time import sleep
import json
import pandas as pd
import glob
import re
import os
import numpy as np



WEBSITE_URL_1_PREFIX = "https://www.prokabaddi.com"


class KabaddiDataAggregator:
    def __init__(self, headless=True):
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        self.driver = webdriver.Firefox(options=options)
        self.player_details_df = None
        self.team_details_df = None
        self.team_members_df = None

    def __del__(self):
        self.driver.quit()

    def get_all_team_names(self):
        self.driver.get(f"{WEBSITE_URL_1_PREFIX}/teams")
        elements = self.driver.find_elements(By.CLASS_NAME, "card-text")
        return [element.text.replace("\n", " ") for element in elements]

    def get_all_team_url(self):
        self.driver.get(f"{WEBSITE_URL_1_PREFIX}/stats")
        return [
            i.replace("/players", "")
            for i in [
                i.get_attribute("href")
                for i in self.driver.find_elements(By.TAG_NAME, "a")
                if i is not None
            ]
            if i is not None and "players" in i
        ]
    def get_auction_data(self):
        self.driver.get("file:///C:/Users/KIIT/Documents/cmu-api-test/hello-kabaddi-adda-stats.html")
        players = self.driver.find_elements(By.CLASS_NAME, "players-list-player")
        print("start")
        player_data = []
        for player in players:
            try:
                link_element = player.find_element(By.TAG_NAME, "a")
                link = link_element.get_attribute("href")
                name = link_element.text

                category_div = player.find_element(By.CLASS_NAME, "players-list-category")
                category = category_div.text

                short_stats_divs = player.find_elements(By.CLASS_NAME, "short-stats-div")
                price = ""
                for div in short_stats_divs:
                    label = div.find_element(By.TAG_NAME, "div").text
                    if label == "Auction Price":
                        price = div.find_elements(By.TAG_NAME, "div")[1].text
                        break

                player_data.append({
                    "name": name,
                    "link": link,
                    "category": category,
                    "auction_price": price
                    })
            except Exception as e:
                print(f"Error extracting data for a player: {e}")
                continue

            print("done")
            print(f"Total players extracted: {len(player_data)}")
            print(player_data)

            df = pd.DataFrame(player_data)
    
            df['name'] = df['link'].apply(lambda x: x.split('/')[-1].replace('-', ' ').title())
    
            columns_order = ['name', 'link', 'category', 'auction_price']
            df = df[columns_order]
            output_file='player_data.csv'    
            df.to_csv(output_file, index=False)
            print(f"Data exported to {output_file}")
    
    def clean_auction_data(self):
        df = pd.read_csv(r"C:\Users\KIIT\Documents\cmu-api-test\player_data.csv")
        df['name'] = df['name'].apply(lambda x: re.sub(r'\s+\d+$', '', x))
        df['link'] = df['link'].str.replace('file:///', 'https://www.kabaddiadda.com/')
        df.to_csv('updated_player_data.csv', index=False)
        print("exported.")
    def get_all_auction_data(self):
        '''
        appends all kabaddi-adda links with ?tab=auction
        '''
        df = pd.read_csv(r"C:\Users\KIIT\Documents\cmu-api-test\updated_player_data.csv")
        df['auction_link'] = df['link'] + '?tab=auction'
        print(df.head())
        df.to_csv('auction_link_player_data.csv', index=False)
        print('exported.')

    def auction_mykhel(self, url):
        '''
            Function to get the basic tables from mykhel.com
        '''
        self.driver.get(url)

        # waiting for table to load
        table = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "oi_cms_table"))
        )

        # finding all the rows in the table
        rows = table.find_elements(By.TAG_NAME, "tr")
        data = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) == 6:  # Ensure it's a data row
                player_data = {
                    "Player Name": cells[0].text,
                    "Category": cells[1].text,
                    "Position": cells[2].text,
                    "Base Price": cells[3].text,
                    "Team": cells[4].text,
                    "Bought For": cells[5].text
                }
                data.append(player_data)
        return pd.DataFrame(data)

    def merge_auction(self):
        folder_path = 'prokabaddidata\\loan_info_stuff_csv'
        merged_df = pd.DataFrame()
        for i in range(1, 8):
            file_path = os.path.join(folder_path, f'kabaddi_auction_data_checkpoint_{i}.csv')
            if os.path.exists(file_path):
                df = pd.read_csv(file_path)
                merged_df = pd.concat([merged_df, df], ignore_index=True)

        output_path = 'final-kabaddi_auction_data_merged.csv'  # Specify the output file name
        merged_df.to_csv(output_path, index=False)

        print(f'Merged file saved to {output_path}')

    def extract_player_name(self, url):
        '''
        used for extracting player names from urls (kabaddi-adda)
        '''
        match = re.search(r'/player/([^-]+(?:-[^-]+)*)-\d+', url)
        if match:
            return match.group(1).replace('-', ' ').title()
        return None

    def get_clean_auction_data(self):
        df = pd.read_csv("loan_info_stuff_csv/kabaddi_auction_data_FINAL_NAMES.csv")

        # Step 1: Remove numbers from Player_Name
        df['Player_Name'] = df['Player_Name'].apply(lambda x: re.sub(r'\d+', '', x))

        # Display the result after step 1
        print("After removing numbers:")
        print(df['Player_Name'].head())
        print("\n")

        # Step 2: Remove dashes from Player_Name
        df['Player_Name'] = df['Player_Name'].apply(lambda x: x.replace('-', ' ').strip())

        # Display the final result
        print("After removing dashes:")
        print(df['Player_Name'].head())
        df.to_csv('processed_auction_data.csv', index=False)

    def get_player_auction_info(self, player_name):
        """
        Retrieves auction information for a specified player.
        The search is case-insensitive and handles cases where the player name might be partially matched.

        Args:
            player_name (str): The name of the player for whom auction information is to be retrieved.

        Returns:
            pandas.DataFrame or str: If information about the player is found, returns a DataFrame containing the
            auction details for that player. If no information is found, returns a message indicating that no
            information was found for the specified player.
        """
        dataframe = pd.read_csv("loan_info_stuff_csv/FINAL-processed_auction_data.csv")
        player_info = dataframe[dataframe['Player_Name'].str.contains(player_name.lower(), case=False, na=False)]

        if player_info.empty:
            return f"No information found for player: {player_name}"
        return player_info

    def get_season_auction_data(self, season=None, top=None):
        """
        yet to handle units.
        """
        df = pd.read_csv("loan_info_stuff_csv/FINAL-processed_auction_data.csv")
        result = df.copy()

        result['Price'] = result['Price'].str.replace(' L', '').astype(float)

        if season:
            result = result[result['Tournament'] == f'Pro Kabaddi Season {season}']

        # Sort by Price in descending order
        result = result.sort_values('Price', ascending=False)

        # If top is specified, limit the results
        if top:
            result = result.head(top)

        # Reset the index
        result = result.reset_index(drop=True)

        return result

    def get_stats_from_player_profile(self, profile_url):
        self.driver.get(profile_url)
        sleep(2)
        labels = [
            i.get_attribute("innerText")
            for i in self.driver.find_elements(By.CLASS_NAME, "graph-label")
            if i is not None
        ]
        values = [
            i.get_attribute("innerText")
            for i in self.driver.find_elements(By.CLASS_NAME, "graph-value")
            if i is not None
        ]
        team = (
            self.driver.find_elements(By.CLASS_NAME, "name-section")[0]
            .get_attribute("innerText")
            .replace("\n", " ")
        )
        return {labels[0]: values[0], labels[1]: values[1], "teamName": team}

    def team_season_standings(self, team=None, rank=None):
        """
        Returns the latest season standings.
        Parameters:
        team (str, optional): The name of a specific team to get data for. Case-insensitive.
        rank (int, optional): The rank (1-12) to get the team data for.
        """
        if team is not None and rank is not None:
            return "Please provide either a team name or a rank, but not both. By default, all the teams will be listed."
        self.driver.get("https://www.prokabaddi.com/")
        sleep(2)
        team_name = [
            i.get_attribute("innerText")
            for i in self.driver.find_elements(By.CLASS_NAME, "team-name")
            if i is not None
        ]
        play = [
            i.get_attribute("innerText")
            for i in self.driver.find_elements(By.CLASS_NAME, "matches-play")
            if i is not None
        ]
        play = play[::-1][: len(play) - 1][::-1]
        won = [
            i.get_attribute("innerText")
            for i in self.driver.find_elements(By.CLASS_NAME, "matches-won")
            if i is not None
        ]
        won = won[::-1][: len(won) - 1][::-1]
        lost = [
            i.get_attribute("innerText")
            for i in self.driver.find_elements(By.CLASS_NAME, "matches-lost")
            if i is not None
        ]
        lost = lost[::-1][: len(lost) - 1][::-1]
        draw = [
            i.get_attribute("innerText")
            for i in self.driver.find_elements(By.CLASS_NAME, "matches-draw")
            if i is not None
        ]
        draw = draw[::-1][: len(draw) - 1][::-1]
        points = [
            i.get_attribute("innerText")
            for i in self.driver.find_elements(By.CLASS_NAME, "points")
            if i is not None
        ]
        points = points[::-1][: len(points) - 1][::-1]
        team_property_dict = {
            team_name[i].lower(): {
                "TeamName": team_name[i],
                "play": int(play[i]),
                "won": int(won[i]),
                "lost": int(lost[i]),
                "draw": int(draw[i]),
                "points": int(points[i]),
            }
            for i in range(len(team_name))
        }
        if team is None and rank is None:
            return team_property_dict
        if team != None:
            if team.lower() in team_property_dict:
                return team_property_dict.get(team.lower())
            else:
                return "Enter a valid team name!"
        if (rank != None) and (1 <= rank <= 12):
            sorted_teams = sorted(
                team_property_dict.values(), key=lambda x: x["points"], reverse=True
            )
            print(f"Rank : {rank}")
            return sorted_teams[int(rank)]
        else:
            return "Enter rank between 1 and 12!"

    def get_all_season_team_stats(self, url):
        self.driver.get(url)
        with open("get_team_performance.js", "r") as f:
            js_code = f.read()
        return self.driver.execute_script(js_code)

    def team_line_up(self, season=None):
        return self._tableau_data_extraction(
            "https://public.tableau.com/views/DEMO_PKL_S9/TeamLine-up?%3Adisplay_static_image=y&%3Aembed=true&%3Aembed=y&%3Alanguage=en-US&publish=yes%20&%3AshowVizHome=n&%3AapiID=host0#navType=0&navSrc=Parse",
            season=2,
        )

    def team_level_stats(self, season=None):
        return self._tableau_data_extraction(
            url="https://public.tableau.com/views/DEMO_PKL_S9/Teamlevelstats?%3Adisplay_static_image=y&%3Aembed=true&%3Aembed=y&%3Alanguage=en-US&publish=yes%20&%3AshowVizHome=n&%3AapiID=host0#navType=0&navSrc=Parse",
            season=4,
        )

    def player_performance(self, team=None):
        return self._tableau_data_extraction(
            "https://public.tableau.com/views/DEMO_PKL_S9/PlayerPerformance?%3Adisplay_static_image=y&%3Aembed=true&%3Aembed=y&%3Alanguage=en-US&publish=yes%20&%3AshowVizHome=n&%3AapiID=host0#navType=0&navSrc=Parse",
            3,
        )

    def _tableau_data_extraction(self, url, season=None, iterations=0):
        """
        Extract data from the specified Tableau dashboard using Selenium.

        Parameters:
        - url (str): The URL of the Tableau dashboard to be accessed.
        - iterations (int): The number of iterations to perform for data extraction.

        Returns:
        - results (list): A list of data extracted in each iteration.
        """
        self.driver.get(url)
        sleep(10)
        self.driver.find_elements(By.CLASS_NAME, "tabComboBoxNameContainer")[0].click()
        self.driver.find_elements(By.CLASS_NAME, "FICheckRadio")[5].click()

        if season is not None:
            self.driver.find_elements(By.CLASS_NAME, "FICheckRadio")[season].click()
            sleep(2)
            self.driver.execute_script(open("script.js", "r").read())
            self.driver.save_screenshot(f"screenshot_{season}.png")
            sleep(7)
            self.driver.save_screenshot("2.png")
            sleep(2)
            try:
                self.driver.execute_script(
                    "document.getElementsByClassName('f1b5ibck')[0].click()"
                )
            except:
                pass
                sleep(2)
            self.driver.save_screenshot("3.png")
            sleep(2)
            try:
                self.driver.find_elements(By.CLASS_NAME, "tabComboBoxNameContainer")[
                    0
                ].click()
            except:
                pass
            sleep(2)
            try:
                self.driver.find_elements(By.CLASS_NAME, "FICheckRadio")[season].click()
            except Exception as e:
                print(e)
            print("done")

        if season is None:
            results = []
            for y in range(1, iterations + 1):
                print(f"Iteration {y} started")
                self.driver.find_elements(By.CLASS_NAME, "FICheckRadio")[y].click()
                sleep(2)
                with open("script.js", "r") as f:
                    js_code = f.read()
                data = self.driver.execute_script(js_code)
                results.append(data)
                sleep(7)
                self.driver.save_screenshot(f"screenshot_{y}.png")
                sleep(2)
                try:
                    self.driver.execute_script(
                        "document.getElementsByClassName('f1b5ibck')[0].click()"
                    )
                except:
                    pass
                sleep(2)
                try:
                    self.driver.find_elements(
                        By.CLASS_NAME, "tabComboBoxNameContainer"
                    )[0].click()
                except:
                    pass
                sleep(2)
                try:
                    self.driver.find_elements(By.CLASS_NAME, "FICheckRadio")[y].click()
                except:
                    pass
                print(f"Iteration {y} completed")

            return results

    def load_data(self, TeamDetails=False, TeamMembers=False, PlayerDetails=True):
        """
        Load specified CSV files into pandas DataFrames based on the provided boolean parameters.

        Parameters:
        - TeamDetails (bool): Loads the 'teamDetails.csv' file. Default is True.
        - TeamMembers (bool): Loads the 'teamMembers.csv' file. Default is True.
        - PlayerDetails (bool): Loads the 'playerDetails.csv' file. Default is True.

        Returns:
        - tuple: A tuple containing the loaded DataFrames in the order (player_details_df, team_details_df, team_members_df).
        """
        # default_download_directory = r"C:\Users\KIIT\Downloads"
        if PlayerDetails:
            player_details_df = pd.read_csv(
                f"./playerDetails.csv"
            )
            self.player_details_df = player_details_df
            print("Loaded playerDetails.csv")
        else:
            player_details_df = None

        if TeamDetails:
            team_details_df = pd.read_csv(
                f"teamDetails.csv"
            )
            self.team_details_df = team_details_df
            print("Loaded teamDetails.csv")
        else:
            team_details_df = None

        if TeamMembers:
            team_members_df = pd.read_csv(
                f"teamMembers.csv"
            )
            self.team_members_df = team_members_df
            print("Loaded teamMembers.csv")

        if PlayerDetails:
            
            team_members_df = pd.read_csv(
                f"playerDetails.csv"
            )
            self.player_details_df = player_details_df
            print("Loaded playerDetails.csv")

        else:
            team_members_df = None
        print("loaded all")
        return (player_details_df, team_details_df, team_members_df)

    def get_player_details(self):
        self.driver.get(
            "https://www.prokabaddi.com/stats/0-102-player-total-points-statistics"
        )
        element = self.driver.find_element(By.CLASS_NAME, "loadmore")
        for i in range(16):
            self.driver.execute_script("arguments[0].click();", element)
        soup = BeautifulSoup(self.driver.page_source, "html.parser")

        for info in soup.find_all("div", class_="info-name"):
            first_name_elem = info.find("p", class_="name first-name")
            last_name_elem = info.find("p", class_="name last-name")

            if first_name_elem and last_name_elem:
                first_name = first_name_elem.text.strip()
                last_name = last_name_elem.text.strip()
                full_name = f"{first_name} {last_name}"
                with open("parsed.txt", "a") as f:
                    f.write(full_name + "\n")
        playerDetails = pd.read_csv(
            "parsed.txt", encoding="ISO-8859-1", names=["playerName"]
        )
        if os.path.exists("parsed.txt"):
            os.remove("parsed.txt")
        dfObj = pd.DataFrame(data=[])
        dfObj["PlayerName"] = playerDetails[playerDetails.columns[0]]

        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        for item in soup.find_all("div", class_="table-data matches-played"):
            [elem.extract() for elem in soup.find("div")]
            file = open("parsed.txt", "a")
            file.write(item.text)
            file.write("\n")
            file.close()
        playerDetails = pd.read_csv(
            "parsed.txt", encoding="ISO-8859-1", sep="\t", names=["MatchesPlayed"]
        )
        dfObj["MatchesPlayed"] = playerDetails[playerDetails.columns[0]]
        if os.path.exists("parsed.txt"):
            os.remove("parsed.txt")

        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        for item in soup.find_all("div", class_="table-data rank"):
            [elem.extract() for elem in soup.find("div")]
            file = open("parsed.txt", "a")
            file.write(item.text)
            file.write("\n")
            file.close()
        playerDetails = pd.read_csv(
            "parsed.txt", encoding="ISO-8859-1", sep="\t", names=["Rank"]
        )
        dfObj["Rank"] = playerDetails[playerDetails.columns[0]]
        if os.path.exists("parsed.txt"):
            os.remove("parsed.txt")

        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        for item in soup.find_all("div", class_="category"):
            [elem.extract() for elem in soup.find("div")]
            file = open("parsed.txt", "a")
            file.write(item.text)
            file.write("\n")
            file.close()
        playerDetails = pd.read_csv(
            "parsed.txt", encoding="ISO-8859-1", sep="\t", names=["PlayerProfile"]
        )
        if os.path.exists("parsed.txt"):
            os.remove("parsed.txt")
        dfObj["PlayerProfile"] = playerDetails[playerDetails.columns[0]]

        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        for item in soup.find_all("div", class_="table-data total-points"):
            [elem.extract() for elem in soup.find("div")]
            file = open("parsed.txt", "a")
            file.write(item.text)
            file.write("\n")
            file.close()
        playerDetails = pd.read_csv(
            "parsed.txt", encoding="ISO-8859-1", sep="\t", names=["TotalPoints"]
        )
        if os.path.exists("parsed.txt"):
            os.remove("parsed.txt")
        dfObj["TotalPoints"] = playerDetails[playerDetails.columns[0]]

        self.driver.get(
            "https://www.prokabaddi.com/stats/0-21-successful-raids-statistics"
        )
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        for item in soup.find_all("div", class_="table-data total-points"):
            [elem.extract() for elem in soup.find("div")]
            file = open("parsed.txt", "a")
            file.write(item.text)
            file.write("\n")
            file.close()
        playerDetails = pd.read_csv(
            "parsed.txt",
            encoding="ISO-8859-1",
            sep="\t",
            names=["Successful raids"],
        )
        if os.path.exists("parsed.txt"):
            os.remove("parsed.txt")
        dfObj["SuccessfulRaidPoints"] = playerDetails[playerDetails.columns[0]]

        self.driver.get(
            "https://www.prokabaddi.com/stats/0-22-raid-points-statistics"
        )
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        for item in soup.find_all("div", class_="table-data total-points"):
            [elem.extract() for elem in soup.find("div")]
            file = open("parsed.txt", "a")
            file.write(item.text)
            file.write("\n")
            file.close()
        playerDetails = pd.read_csv(
            "parsed.txt", encoding="ISO-8859-1", sep="\t", names=["raid points"]
        )
        if os.path.exists("parsed.txt"):
            os.remove("parsed.txt")
        dfObj["RaidPoints"] = playerDetails[playerDetails.columns[0]]

        self.driver.get(
            "https://www.prokabaddi.com/stats/0-23-successful-tackles-statistics"
        )
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        for item in soup.find_all("div", class_="table-data total-points"):
            [elem.extract() for elem in soup.find("div")]
            file = open("parsed.txt", "a")
            file.write(item.text)
            file.write("\n")
            file.close()
        playerDetails = pd.read_csv(
            "parsed.txt",
            encoding="ISO-8859-1",
            sep="\t",
            names=["successful tackles"],
        )
        if os.path.exists("parsed.txt"):
            os.remove("parsed.txt")
        dfObj["SuccessfulTackles"] = playerDetails[playerDetails.columns[0]]

        self.driver.get(
            "https://www.prokabaddi.com/stats/0-103-tackle-points-statistics"
        )
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        for item in soup.find_all("div", class_="table-data total-points"):
            [elem.extract() for elem in soup.find("div")]
            file = open("parsed.txt", "a")
            file.write(item.text)
            file.write("\n")
            file.close()
        playerDetails = pd.read_csv(
            "parsed.txt", encoding="ISO-8859-1", sep="\t", names=["tackle points"]
        )
        if os.path.exists("parsed.txt"):
            os.remove("parsed.txt")
        dfObj["TacklePoints"] = playerDetails[playerDetails.columns[0]]

        self.driver.get(
            "https://www.prokabaddi.com/stats/0-22-avg-raid-points-statistics"
        )
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        for item in soup.find_all("div", class_="table-data total-points"):
            [elem.extract() for elem in soup.find("div")]
            file = open("parsed.txt", "a")
            file.write(item.text)
            file.write("\n")
            file.close()
        playerDetails = pd.read_csv(
            "parsed.txt",
            encoding="ISO-8859-1",
            sep="\t",
            names=["avg. raid points"],
        )
        if os.path.exists("parsed.txt"):
            os.remove("parsed.txt")
        dfObj["AverageRaidPoints"] = playerDetails[playerDetails.columns[0]]

        self.driver.get(
            "https://www.prokabaddi.com/stats/0-139-avg-tackle-points-statistics"
        )
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        for item in soup.find_all("div", class_="table-data total-points"):
            [elem.extract() for elem in soup.find("div")]
            file = open("parsed.txt", "a")
            file.write(item.text)
            file.write("\n")
            file.close()
        playerDetails = pd.read_csv(
            "parsed.txt",
            encoding="ISO-8859-1",
            sep="\t",
            names=["avg. tackle points"],
        )
        if os.path.exists("parsed.txt"):
            os.remove("parsed.txt")
        dfObj["AverageTacklePoints"] = playerDetails[playerDetails.columns[0]]

        self.driver.get(
            "https://www.prokabaddi.com/stats/0-132-do-or-die-raid-points-statistics"
        )
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        for item in soup.find_all("div", class_="table-data total-points"):
            [elem.extract() for elem in soup.find("div")]
            file = open("parsed.txt", "a")
            file.write(item.text)
            file.write("\n")
            file.close()
        playerDetails = pd.read_csv(
            "parsed.txt",
            encoding="ISO-8859-1",
            sep="\t",
            names=["do or die points"],
        )
        if os.path.exists("parsed.txt"):
            os.remove("parsed.txt")
        dfObj["DODRaidPoints"] = playerDetails[playerDetails.columns[0]]

        self.driver.get(
            "https://www.prokabaddi.com/stats/0-104-super-raids-statistics"
        )
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        for item in soup.find_all("div", class_="table-data total-points"):
            [elem.extract() for elem in soup.find("div")]
            file = open("parsed.txt", "a")
            file.write(item.text)
            file.write("\n")
            file.close()
        playerDetails = pd.read_csv(
            "parsed.txt", encoding="ISO-8859-1", sep="\t", names=["super raids"]
        )
        if os.path.exists("parsed.txt"):
            os.remove("parsed.txt")
        dfObj["SuperRaids"] = playerDetails[playerDetails.columns[0]]

        self.driver.get(
            "https://www.prokabaddi.com/stats/0-28-super-tackles-statistics"
        )
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        for item in soup.find_all("div", class_="table-data total-points"):
            [elem.extract() for elem in soup.find("div")]
            file = open("parsed.txt", "a")
            file.write(item.text)
            file.write("\n")
            file.close()
        playerDetails = pd.read_csv(
            "parsed.txt", encoding="ISO-8859-1", sep="\t", names=["super tackles"]
        )
        if os.path.exists("parsed.txt"):
            os.remove("parsed.txt")
        dfObj["SuperTackles"] = playerDetails[playerDetails.columns[0]]

        self.driver.get(
            "https://www.prokabaddi.com/stats/0-100-super-10s-statistics"
        )
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        for item in soup.find_all("div", class_="table-data total-points"):
            [elem.extract() for elem in soup.find("div")]
            file = open("parsed.txt", "a")
            file.write(item.text)
            file.write("\n")
            file.close()
        playerDetails = pd.read_csv(
            "parsed.txt", encoding="ISO-8859-1", sep="\t", names=["super 10s"]
        )
        if os.path.exists("parsed.txt"):
            os.remove("parsed.txt")
        dfObj["Super10s"] = playerDetails[playerDetails.columns[0]]

        self.driver.get("https://www.prokabaddi.com/stats/0-101-high-5s-statistics")
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        for item in soup.find_all("div", class_="table-data total-points"):
            [elem.extract() for elem in soup.find("div")]
            file = open("parsed.txt", "a")
            file.write(item.text)
            file.write("\n")
            file.close()
        playerDetails = pd.read_csv(
            "parsed.txt", encoding="ISO-8859-1", sep="\t", names=["high 5s"]
        )
        if os.path.exists("parsed.txt"):
            os.remove("parsed.txt")
        dfObj["High5s"] = playerDetails[playerDetails.columns[0]]

        dfObj.drop(index=0, inplace=True)

        return dfObj

    def get_team_standings(self):
        df = pd.read_csv(r"C:\Users\KIIT\Documents\ProKabaddi_API\pypi\prokabaddidata\DATA\DATA__prokabaddi_dot_com\improved_standings\standings_csvs\teams\json_s1_teams.csv")
        print(df.head())
        column_headers = df.columns.to_list()
        print("The Column Header :", column_headers)





# Usage example
if __name__ == "__main__":
    aggregator = KabaddiDataAggregator()

    # result = aggregator.get_player_info("pardeep-narwal")
    # print(result)
    # z = aggregator.get_player_details()
    # print(z)
    #print(aggregator.get_player_auction_info("Paul"))
    #print(aggregator.get_season_auction_data(season=8, top=10))
    #aggregator.get_team_standings()
    df = pd.read_csv(r"C:\Users\KIIT\Documents\ProKabaddi_API\pypi\prokabaddidata\DATA\DATA__prokabaddi_dot_com\teams\seasons_1_to_4_final.csv")
    column_headers = df.columns.to_list()
    print("The Column Header :", column_headers)
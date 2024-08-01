# kabaddi_data.py


from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import json

class KabaddiDataAggregator:
    def __init__(self, headless=True):
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument('--headless')
        self.driver = webdriver.Firefox(options=options)

    def __del__(self):
        self.driver.quit()

    def get_all_team_names(self):
        self.driver.get("https://www.prokabaddi.com/teams")
        elements = self.driver.find_elements(By.CLASS_NAME, 'card-text')
        return [element.text.replace("\n", " ") for element in elements]

    def get_all_team_url(self):
        self.driver.get("https://www.prokabaddi.com/stats")
        return [i.replace("/players", "") for i in [i.get_attribute('href') for i in self.driver.find_elements(By.TAG_NAME, 'a') if i is not None] if i is not None and "players" in i]

    def get_all_player_team_url(self):
        self.driver.get("https://www.prokabaddi.com/stats")
        return [i for i in [i.get_attribute('href') for i in self.driver.find_elements(By.TAG_NAME, 'a') if i is not None] if i is not None and "players" in i]

    def get_players_team_info_and_profile_url(self):
        players_info = []
        urls = self.get_all_player_team_url()
        for url in urls:
            self.driver.get(url)
            try:
                player_profile_urls = [x for x in [i.get_attribute("href") for i in self.driver.find_elements(By.TAG_NAME, "a") if i is not None] if x is not None and "profile" in x and "/players/" in x]
                player_names = [i.get_attribute("innerText").replace("\n", " ") for i in self.driver.find_elements(By.CLASS_NAME, "squad-name") if i is not None]
                for name, profile_url in zip(player_names, player_profile_urls):
                    players_info.append({"name": name, "profileURL": profile_url, "teamURL": url})
            except Exception as e:
                print(f"Error processing URL {url}: {str(e)}")
        return players_info

    def get_stats_from_player_profile(self, profile_url):
        self.driver.get(profile_url)
        sleep(2)
        labels = [i.get_attribute("innerText") for i in self.driver.find_elements(By.CLASS_NAME, "graph-label") if i is not None]
        values = [i.get_attribute("innerText") for i in self.driver.find_elements(By.CLASS_NAME, "graph-value") if i is not None]
        team = self.driver.find_elements(By.CLASS_NAME, "name-section")[0].get_attribute("innerText").replace("\n", " ")
        return {labels[0]: values[0], labels[1]: values[1], "teamName": team}

    def team_season_standings(self, team=None, rank=None):
        if team is not None and rank is not None:
            return "Please provide either a team name or a rank, but not both. By default, all the teams will be listed."
        
        self.driver.get("https://www.prokabaddi.com/")
        sleep(2)
        team_names = [i.get_attribute("innerText") for i in self.driver.find_elements(By.CLASS_NAME, "team-name") if i is not None]
        plays = [int(i.get_attribute("innerText")) for i in self.driver.find_elements(By.CLASS_NAME, "matches-play") if i is not None][:-1]
        wins = [int(i.get_attribute("innerText")) for i in self.driver.find_elements(By.CLASS_NAME, "matches-won") if i is not None][:-1]
        losses = [int(i.get_attribute("innerText")) for i in self.driver.find_elements(By.CLASS_NAME, "matches-lost") if i is not None][:-1]
        draws = [int(i.get_attribute("innerText")) for i in self.driver.find_elements(By.CLASS_NAME, "matches-draw") if i is not None][:-1]
        points = [int(i.get_attribute("innerText")) for i in self.driver.find_elements(By.CLASS_NAME, "points") if i is not None][:-1]

        team_standings = [
            {
                "TeamName": name,
                "play": play,
                "won": won,
                "lost": lost,
                "draw": draw,
                "points": point
            }
            for name, play, won, lost, draw, point in zip(team_names, plays, wins, losses, draws, points)
        ]

        if team is None and rank is None:
            return team_standings
        if team is not None:
            return next((t for t in team_standings if t["TeamName"].lower() == team.lower()), "Enter a valid team name!")
        if 1 <= rank <= 12:
            sorted_teams = sorted(team_standings, key=lambda x: x['points'], reverse=True)
            return sorted_teams[rank - 1]
        else:
            return "Enter rank between 1 and 12!"

    def get_all_season_team_stats(self, url):
        self.driver.get(url)
        with open("get_team_performance.js", "r") as f:
            js_code = f.read()
        return self.driver.execute_script(js_code)

    def team_line_up(self):
        return self._tableau_data_extraction("https://public.tableau.com/views/DEMO_PKL_S9/TeamLine-up?%3Adisplay_static_image=y&%3Aembed=true&%3Aembed=y&%3Alanguage=en-US&publish=yes%20&%3AshowVizHome=n&%3AapiID=host0#navType=0&navSrc=Parse", 5)

    def team_level_stats(self):
        return self._tableau_data_extraction("https://public.tableau.com/views/DEMO_PKL_S9/Teamlevelstats?%3Adisplay_static_image=y&%3Aembed=true&%3Aembed=y&%3Alanguage=en-US&publish=yes%20&%3AshowVizHome=n&%3AapiID=host0#navType=0&navSrc=Parse", 3)

    def player_performance(self):
        return self._tableau_data_extraction("https://public.tableau.com/views/DEMO_PKL_S9/PlayerPerformance?%3Adisplay_static_image=y&%3Aembed=true&%3Aembed=y&%3Alanguage=en-US&publish=yes%20&%3AshowVizHome=n&%3AapiID=host0#navType=0&navSrc=Parse", 3)

    def _tableau_data_extraction(self, url, iterations):
        self.driver.get(url)
        sleep(10)
        self.driver.find_elements(By.CLASS_NAME, "tabComboBoxNameContainer")[0].click()
        self.driver.find_elements(By.CLASS_NAME, "FICheckRadio")[5].click()
        
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
                self.driver.execute_script("document.getElementsByClassName('f1b5ibck')[0].click()")
            except:
                pass
            sleep(2)
            try:
                self.driver.find_elements(By.CLASS_NAME, "tabComboBoxNameContainer")[0].click()
            except:
                pass
            sleep(2)
            try:
                self.driver.find_elements(By.CLASS_NAME, "FICheckRadio")[y].click()
            except:
                pass
            print(f"Iteration {y} completed")
        
        return results

# Usage example
if __name__ == "__main__":
    aggregator = KabaddiDataAggregator()
    team_names = aggregator.get_all_team_names()
    print("Team Names:", team_names)
    
    standings = aggregator.team_season_standings()
    print("Season Standings:", json.dumps(standings, indent=2))
    
    # Add more usage examples as needed
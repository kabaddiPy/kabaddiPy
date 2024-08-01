from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

options = webdriver.FirefoxOptions()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)


def get_all_team_names():
    driver.get("https://www.prokabaddi.com/teams")
    elements = driver.find_elements(By.CLASS_NAME, "card-text")
    return [element.text.replace("\n", " ") for element in elements]


def get_all_team_url():
    driver.get("https://www.prokabaddi.com/stats")
    return [
        i.replace("/players", "")
        for i in [
            i.get_attribute("href")
            for i in driver.find_elements(By.TAG_NAME, "a")
            if i != None
        ]
        if i != None
        if "players" in i
    ]


def get_all_player_team_url():
    driver.get("https://www.prokabaddi.com/stats")
    return [
        i.replace("/players")
        for i in [
            i.get_attribute("href")
            for i in driver.find_elements(By.TAG_NAME, "a")
            if i != None
        ]
        if i != None
        if "players" in i
    ]


def get_players_team_info_and_profile_url():
    n = []
    lis = get_all_player_team_url()
    for url in lis:
        driver.get(url)
        try:
            player_profile_urls = [
                x
                for x in [
                    i.get_attribute("href")
                    for i in driver.find_elements(By.TAG_NAME, "a")
                    if i is not None
                ]
                if x is not None and "profile" in x and "/players/" in x
            ]
            player_name = [
                i.get_attribute("innerText").replace("\n", " ")
                for i in driver.find_elements(By.CLASS_NAME, "squad-name")
                if i is not None
            ]
            for i in range(0, len(player_name)):
                n.append(
                    {
                        "name": player_name[i],
                        "profileURL": player_profile_urls[i],
                        "teamURL": url,
                    }
                )
        except:
            pass
    return n


def get_stats_from_player_profile(profile_url):
    driver.get(profile_url)
    sleep(2)
    label = [
        i.get_attribute("innerText")
        for i in driver.find_elements(By.CLASS_NAME, "graph-label")
        if i is not None
    ]
    value = [
        i.get_attribute("innerText")
        for i in driver.find_elements(By.CLASS_NAME, "graph-value")
        if i is not None
    ]
    team = (
        driver.find_elements(By.CLASS_NAME, "name-section")[0]
        .get_attribute("innerText")
        .replace("\n", " ")
    )
    return {label[0]: value[0], label[1]: value[1], "teamName": team}


def team_season_standings(team=None, rank=None):
    """
    Returns the latest season standings.
    Parameters:
    team (str, optional): The name of a specific team to get data for. Case-insensitive.
    rank (int, optional): The rank (1-12) to get the team data for.
    """
    if team is not None and rank is not None:
        return "Please provide either a team name or a rank, but not both. By default, all the teams will be listed."
    driver.get("https://www.prokabaddi.com/")
    sleep(2)
    team_name = [
        i.get_attribute("innerText")
        for i in driver.find_elements(By.CLASS_NAME, "team-name")
        if i is not None
    ]
    play = [
        i.get_attribute("innerText")
        for i in driver.find_elements(By.CLASS_NAME, "matches-play")
        if i is not None
    ]
    play = play[::-1][: len(play) - 1][::-1]
    won = [
        i.get_attribute("innerText")
        for i in driver.find_elements(By.CLASS_NAME, "matches-won")
        if i is not None
    ]
    won = won[::-1][: len(won) - 1][::-1]
    lost = [
        i.get_attribute("innerText")
        for i in driver.find_elements(By.CLASS_NAME, "matches-lost")
        if i is not None
    ]
    lost = lost[::-1][: len(lost) - 1][::-1]
    draw = [
        i.get_attribute("innerText")
        for i in driver.find_elements(By.CLASS_NAME, "matches-draw")
        if i is not None
    ]
    draw = draw[::-1][: len(draw) - 1][::-1]
    points = [
        i.get_attribute("innerText")
        for i in driver.find_elements(By.CLASS_NAME, "points")
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


def get_all_season_team_stats(url):
    driver.get(url)
    return driver.execute_script(open("get_team_performance.js", "r").read())


def TeamLineUp():
    driver.get(
        "https://public.tableau.com/views/DEMO_PKL_S9/TeamLine-up?%3Adisplay_static_image=y&%3Aembed=true&%3Aembed=y&%3Alanguage=en-US&publish=yes%20&%3AshowVizHome=n&%3AapiID=host0#navType=0&navSrc=Parse"
    )
    sleep(4)
    driver.find_elements(By.CLASS_NAME, "tabComboBoxNameContainer")[0].click()
    driver.find_elements(By.CLASS_NAME, "FICheckRadio")[5].click()
    for y in range(1, 6):
        print(str(y) + " - a")
        driver.find_elements(By.CLASS_NAME, "FICheckRadio")[y].click()
        sleep(2)
        print(str(y) + " - b")
        driver.execute_script(open("script.js", "r").read())
        print(str(y) + " - c")
        sleep(7)
        driver.save_screenshot("2.png")
        sleep(2)
        try:
            driver.execute_script(
                "document.getElementsByClassName('f1b5ibck')[0].click()"
            )
        except:
            pass
        sleep(2)
        driver.save_screenshot("1.png")
        sleep(2)
        try:
            driver.find_elements(By.CLASS_NAME, "tabComboBoxNameContainer")[0].click()
        except:
            pass
        print(str(y) + " - d")
        sleep(2)
        try:
            driver.find_elements(By.CLASS_NAME, "FICheckRadio")[y].click()
        except:
            pass
        print(str(y) + " - e")
    return "done"


def Teamlevelstats():
    driver.get(
        "https://public.tableau.com/views/DEMO_PKL_S9/Teamlevelstats?%3Adisplay_static_image=y&%3Aembed=true&%3Aembed=y&%3Alanguage=en-US&publish=yes%20&%3AshowVizHome=n&%3AapiID=host0#navType=0&navSrc=Parse"
    )
    sleep(4)
    driver.find_elements(By.CLASS_NAME, "tabComboBoxNameContainer")[0].click()
    driver.find_elements(By.CLASS_NAME, "FICheckRadio")[5].click()
    for y in range(1, 4):
        print(str(y) + " - a")
        driver.find_elements(By.CLASS_NAME, "FICheckRadio")[y].click()
        sleep(2)
        print(str(y) + " - b")
        driver.execute_script(open("script.js", "r").read())
        print(str(y) + " - c")
        sleep(7)
        driver.save_screenshot("2.png")
        sleep(2)
        try:
            driver.execute_script(
                "document.getElementsByClassName('f1b5ibck')[0].click()"
            )
        except:
            pass
        sleep(2)
        driver.save_screenshot("1.png")
        sleep(2)
        try:
            driver.find_elements(By.CLASS_NAME, "tabComboBoxNameContainer")[0].click()
        except:
            pass
        print(str(y) + " - d")
        sleep(2)
        try:
            driver.find_elements(By.CLASS_NAME, "FICheckRadio")[y].click()
        except:
            pass
        print(str(y) + " - e")
    return "done"


def PlayerPerformance():
    driver.get(
        "https://public.tableau.com/views/DEMO_PKL_S9/PlayerPerformance?%3Adisplay_static_image=y&%3Aembed=true&%3Aembed=y&%3Alanguage=en-US&publish=yes%20&%3AshowVizHome=n&%3AapiID=host0#navType=0&navSrc=Parse"
    )
    sleep(10)
    driver.find_elements(By.CLASS_NAME, "tabComboBoxNameContainer")[0].click()
    driver.find_elements(By.CLASS_NAME, "FICheckRadio")[5].click()
    for y in range(1, 4):
        print(str(y) + " - a")
        driver.find_elements(By.CLASS_NAME, "FICheckRadio")[y].click()
        sleep(2)
        print(str(y) + " - b")
        driver.execute_script(open("script.js", "r").read())
        print(str(y) + " - c")
        sleep(7)
        driver.save_screenshot("2.png")
        sleep(2)
        try:
            driver.execute_script(
                "document.getElementsByClassName('f1b5ibck')[0].click()"
            )
        except:
            pass
        sleep(2)
        driver.save_screenshot("1.png")
        sleep(2)
        try:
            driver.find_elements(By.CLASS_NAME, "tabComboBoxNameContainer")[0].click()
        except:
            pass
        print(str(y) + " - d")
        sleep(2)
        try:
            driver.find_elements(By.CLASS_NAME, "FICheckRadio")[y].click()
        except:
            pass
        print(str(y) + " - e")
    return "done"

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup
from time import sleep
import time
import json
import pandas as pd
import glob
import os
import re



def scrape_auction_data(self, url, player_name):
        #url = "https://www.kabaddiadda.com/player/pawan-kumar-sehrawat-1000070?tab=auction"
        try:
            self.driver.get(url)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            try:
                table = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "player-auction-v2-table"))
                )
                rows = table.find_elements(By.TAG_NAME, "tr")[1:]  # Skip header row

                data = []
                for row in rows:
                    cols = row.find_elements(By.TAG_NAME, "td")
                    if len(cols) >= 4:
                        tournament = cols[0].text
                        team = cols[1].text
                        price = cols[2].text
                        status = cols[3].find_element(By.TAG_NAME, "span").text
                        data.append([player_name, tournament, team, price, status])

                return data
            except (TimeoutException, NoSuchElementException):
                print(f"Auction data not found for URL: {url}")
                return []
        except Exception as e:
            print(f"Error processing URL {url}: {str(e)}")
            return []
        
df = pd.read_csv(r"./auction_link_player_data.csv")
player_links = df['auction_link'].tolist()
print(player_links[0:1000])
all_data = []
player_links_one = player_links[0:50]
print(len(player_links_one))
i = 0
for url in player_links_one:
    print(f"i = {i}")
    player_name = player_links_one[i]
    player_data = aggregator.scrape_auction_data(url, player_name)
    all_data.extend(player_data)
    time.sleep(5)
    i+=1

df2 = pd.DataFrame(all_data, columns=['Player_Name','Tournament', 'Team', 'Price', 'Status'])
print(df2)
df2.to_csv('names-one-kabaddi_auction_data.csv', index=False)
print("done.")
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
import json

def get_soup(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    return BeautifulSoup(response.content, 'html.parser')

def scrape_table(soup):
    table_body = soup.find('div', class_='table-body')
    if not table_body:
        print("Table body not found. The page structure might have changed.")
        return []
    data = []
    for row in table_body.find_all('div', class_='table-row'):
        rank = row.find('div', class_='rank').text.strip() if row.find('div', class_='rank') else ''
        name_div = row.find('div', class_='info-name')
        name = name_div.text.strip().replace('\n', ' ') if name_div else ''
        team_logo = row.find('div', class_='team-logo')
        team = team_logo.find('img')['data-src'].split('/')[-1].split('.')[0] if team_logo and team_logo.find('img') else ''
        matches_played = row.find('div', class_='matches-played').text.strip() if row.find('div', class_='matches-played') else ''
        stat_value = row.find('div', class_='total-points').text.strip() if row.find('div', class_='total-points') else ''
        data.append([rank, name, team, matches_played, stat_value])
    return data

def get_seasons(soup):
    seasons = {}
    select_box = soup.find('div', class_='waf-select-box')
    if not select_box:
        print("Select box for seasons not found. Trying to extract from script tag.")
        scripts = soup.find_all('script')
        for script in scripts:
            if 'window.__INITIAL_STATE__' in script.text:
                json_text = script.text.split('window.__INITIAL_STATE__ = ')[1].split('};')[0] + '}'
                data = json.loads(json_text)
                if 'statsFilterSeasons' in data:
                    for season in data['statsFilterSeasons']:
                        seasons[season['id']] = season['name']
                return seasons
    else:
        for item in select_box.find_all('li', class_='list-item'):
            link = item.find('a')['href']
            season_id = re.search(r'/stats/(\d+)-', link).group(1)
            season_name = item.text.strip()
            seasons[season_id] = season_name
    return seasons

base_url = "https://www.prokabaddi.com/stats/{}-{}-statistics"

stat_types = {
    102: "Total Points",
    21: "Successful Raids",
    22: "Raid Points",
    23: "Successful Tackles",
    103: "Tackle Points",
    139: "Avg Tackle Points",
    132: "Do-or-Die Raid Points",
    104: "Super Raids",
    28: "Super Tackles",
    100: "Super 10s",
    101: "High 5s"
}

# update from new mac


# Get the list of all seasons
initial_url = base_url.format(44, 21)  # Using season 10 and successful raids as initial page
initial_soup = get_soup(initial_url)
seasons = get_seasons(initial_soup)

if not seasons:
    print("No seasons found. The website structure might have changed significantly.")
    exit()

print(f"Found {len(seasons)} seasons: {', '.join(seasons.values())}")

all_data = []

for season_id, season_name in seasons.items():
    print(f"Scraping data for {season_name}")
    for stat_id, stat_name in stat_types.items():
        url = base_url.format(season_id, stat_id)
        soup = get_soup(url)
        data = scrape_table(soup)
        for row in data:
            row.extend([stat_name, season_name])
        all_data.extend(data)
        time.sleep(1)  # Be polite to the server

df = pd.DataFrame(all_data, columns=['Rank', 'Name', 'Team', 'Matches Played', 'Stat Value', 'Stat Type', 'Season'])

# Pivot the dataframe to have one row per player per season with all stats as columns
df_pivot = df.pivot_table(
    index=['Name', 'Team', 'Matches Played', 'Season'],
    columns='Stat Type',
    values='Stat Value',
    aggfunc='first'
).reset_index()

df_pivot.to_csv('kabaddi_all_seasons_stats.csv', index=False)
print("Data has been successfully scraped and saved to 'kabaddi_all_seasons_stats.csv'")
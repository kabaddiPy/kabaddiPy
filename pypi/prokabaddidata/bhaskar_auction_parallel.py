from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pandas as pd
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

class KabaddiDataAggregator:
    def __init__(self, headless=True):
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        self.driver = webdriver.Firefox(options=options)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.driver.quit()

    def scrape_auction_data(self, url):
        print(f"Scraping data for URL: {url}")
        try:
            self.driver.get(url)
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

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
                        data.append([url, tournament, team, price, status])

                print(f"Completed scraping for URL: {url}")
                return data if data else [[url, "NA", "NA", "NA", "NA"]]
            except (TimeoutException, NoSuchElementException):
                print(f"No auction data found for URL: {url}")
                return [[url, "NA", "NA", "NA", "NA"]]
        except Exception as e:
            print(f"Error scraping data for URL: {url}. Error: {e}")
            return [[url, "NA", "NA", "NA", "NA"]]

def fetch_player_data(urls, num_threads=50):
    all_data = []
    print(f"Starting to scrape {len(urls)} players with {num_threads} threads.")
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        future_to_url = {executor.submit(aggregator.scrape_auction_data, url): url for url in urls}
        for i, future in enumerate(as_completed(future_to_url), 1):
            try:
                result = future.result()
                all_data.extend(result)
                print(f"Progress: {i}/{len(urls)} players scraped.")
            except Exception as e:
                print(f"Error fetching data for {future_to_url[future]}: {e}")
    print("Completed scraping all players in this batch.")
    return all_data

if __name__ == "__main__":
    with KabaddiDataAggregator() as aggregator:
        df = pd.read_csv(r"./auction_link_player_data.csv")
        player_links = df["auction_link"].tolist()
        print(f"Total players to process: {len(player_links)}")

        chunk_size = 500
        all_data = []

        for start_idx in range(0, len(player_links), chunk_size):
            chunk_links = player_links[start_idx:start_idx + chunk_size]
            print(f"Processing batch {start_idx // chunk_size + 1} with {len(chunk_links)} players.")

            chunk_data = fetch_player_data(chunk_links)
            all_data.extend(chunk_data)

            # Save checkpoint data
            checkpoint_filename = f"kabaddiaddacheckpoints/kabaddi_auction_data_checkpoint_{start_idx // chunk_size + 1}.csv"
            df_checkpoint = pd.DataFrame(
                all_data, columns=["Player_Name", "Tournament", "Team", "Price", "Status"]
            )
            df_checkpoint.to_csv(checkpoint_filename, index=False)
            print(f"Checkpoint saved: {checkpoint_filename}")

        # Save final dataset
        df_final = pd.DataFrame(
            all_data, columns=["Player_Name", "Tournament", "Team", "Price", "Status"]
        )
        df_final.to_csv("final_kabaddi_auction_data.csv", index=False)
        print("Data extraction complete. Final CSV saved.")

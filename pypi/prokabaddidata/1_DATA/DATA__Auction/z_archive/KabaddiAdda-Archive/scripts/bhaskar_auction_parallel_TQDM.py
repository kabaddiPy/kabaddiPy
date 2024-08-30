from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pandas as pd
import time
# import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm.auto import tqdm


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
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            try:
                table = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, "player-auction-v2-table")
                    )
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
        future_to_url = {
            executor.submit(aggregator.scrape_auction_data, url): url for url in urls
        }
        for i, future in enumerate(as_completed(future_to_url), 1):
            try:
                result = future.result()
                all_data.extend(result)
                print(f"Progress: {i}/{len(urls)} players scraped.")
            except Exception as e:
                print(f"Error fetching data for {future_to_url[future]}: {e}")
    print("Completed scraping all players in this batch.")
    return all_data


def process_chunk(chunk_links):
    results = []
    with tqdm(total=len(chunk_links), desc="Processing players", leave=False) as pbar:
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_link = {
                executor.submit(fetch_player_data, [link]): link for link in chunk_links
            }
            for future in as_completed(future_to_link):
                result = future.result()
                results.extend(result)
                pbar.update(1)
    return results


if __name__ == "__main__":
    with KabaddiDataAggregator() as aggregator:
        df = pd.read_csv(f"./data_kabaddi_adda/old/auction_link_player_data.csv")
        player_links = df["auction_link"].tolist()
        print(f"Total players to process: {len(player_links)}")

        chunk_size = 500
        all_data = []

        with tqdm(total=len(player_links), desc="Overall progress") as overall_pbar:
            for start_idx in range(0, len(player_links), chunk_size):
                chunk_links = player_links[start_idx : start_idx + chunk_size]
                print(
                    f"\nProcessing batch {start_idx // chunk_size + 1} with {len(chunk_links)} players."
                )

                chunk_data = process_chunk(chunk_links)
                all_data.extend(chunk_data)

                # Save checkpoint data
                checkpoint_filename = f"kabaddiaddacheckpoints/kabaddi_auction_data_checkpoint_{start_idx // chunk_size + 1}.csv"
                df_checkpoint = pd.DataFrame(
                    all_data,
                    columns=["Player_Name", "Tournament", "Team", "Price", "Status"],
                )
                df_checkpoint.to_csv(checkpoint_filename, index=False)
                print(f"Checkpoint saved: {checkpoint_filename}")

                overall_pbar.update(len(chunk_links))

        # Save final dataset
        df_final = pd.DataFrame(
            all_data, columns=["Player_Name", "Tournament", "Team", "Price", "Status"]
        )
        df_final.to_csv("final_kabaddi_auction_data.csv", index=False)
        print("Data extraction complete. Final CSV saved.")

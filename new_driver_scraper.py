import time
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains

def setup_driver():
    print("Setting up the Chrome driver...")
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    return webdriver.Chrome(options=options)

def get_dropdown_options(driver, dropdown_class):
    print(f"Getting dropdown options for class: {dropdown_class}")
    try:
        dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, dropdown_class))
        )
        dropdown.click()
        options = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "list-item"))
        )
        return [option.find_element(By.TAG_NAME, "a").get_attribute("href") for option in options]
    except (TimeoutException, NoSuchElementException) as e:
        print(f"Error getting dropdown options: {e}")
        return []

def scrape_table(driver):
    print("Scraping table data...")
    try:
        table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "stats-table"))
        )
        headers = [header.text for header in table.find_elements(By.CSS_SELECTOR, ".table-head .table-data p")]
        rows = []
        for row in table.find_elements(By.CSS_SELECTOR, ".table-body .table-row"):
            row_data = [data.text for data in row.find_elements(By.CLASS_NAME, "table-data")]
            rows.append(row_data)
        return pd.DataFrame(rows, columns=headers)
    except (TimeoutException, NoSuchElementException) as e:
        print(f"Error scraping table: {e}")
        return pd.DataFrame()

def click_load_more(driver):
    print("Attempting to click 'Load More' button...")
    try:
        load_more = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "loadmore"))
        )
        actions = ActionChains(driver)
        actions.move_to_element(load_more).click().perform()
        time.sleep(2)
        return True
    except (TimeoutException, NoSuchElementException, ElementClickInterceptedException) as e:
        print(f"Error clicking 'Load More' button: {e}")
        return False

def save_data(data, filename):
    print(f"Saving data to {filename}...")
    data.to_csv(filename, index=False)
    print(f"Data saved successfully to {filename}")

def main():
    driver = setup_driver()
    base_url = "https://www.prokabaddi.com/stats/44-21-player-successful-raids-statistics"
    driver.get(base_url)

    all_data = []
    season_count = 0
    stat_type_count = 0

    # Create a directory to store intermittent CSV files
    os.makedirs("intermittent_data", exist_ok=True)

    # Get all season links
    season_links = get_dropdown_options(driver, "waf-select-box")
    print(f"Found {len(season_links)} seasons to scrape")

    for season_link in season_links:
        season_count += 1
        driver.get(season_link)
        time.sleep(2)
        
        # Get all stat type links for this season
        stat_type_links = get_dropdown_options(driver, "waf-select-box")
        print(f"Found {len(stat_type_links)} stat types for season {season_count}")
        
        for stat_link in stat_type_links:
            stat_type_count += 1
            driver.get(stat_link)
            time.sleep(2)
            
            # Extract season and stat type from URL
            url_parts = stat_link.split('/')[-1].split('-')
            season = url_parts[0]
            stat_type = ' '.join(url_parts[2:-1])
            
            print(f"Scraping data for Season {season}, Stat Type: {stat_type}")
            
            df = scrape_table(driver)
            if not df.empty:
                df['Season'] = season
                df['Stat Type'] = stat_type
                all_data.append(df)
            
            # Check if there's a "Load More" button and click it to get all data
            page_count = 1
            while click_load_more(driver):
                page_count += 1
                print(f"Loading page {page_count} for Season {season}, Stat Type: {stat_type}")
                additional_df = scrape_table(driver)
                if not additional_df.empty:
                    additional_df['Season'] = season
                    additional_df['Stat Type'] = stat_type
                    all_data.append(additional_df)

            # Save intermittent data after each stat type
            intermittent_df = pd.concat(all_data, ignore_index=True)
            save_data(intermittent_df, f"intermittent_data/prokabaddi_stats_s{season_count}_st{stat_type_count}.csv")

        # Save intermittent data after each season
        intermittent_df = pd.concat(all_data, ignore_index=True)
        save_data(intermittent_df, f"intermittent_data/prokabaddi_stats_season{season_count}.csv")

    driver.quit()

    # Combine all dataframes for the final CSV
    final_df = pd.concat(all_data, ignore_index=True)
    
    # Save to final CSV
    save_data(final_df, 'pro_kabaddi_stats_final.csv')
    
    print("Scraping completed. All data saved successfully.")

if __name__ == "__main__":
    main()
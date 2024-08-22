import requests
from bs4 import BeautifulSoup
import json
import re
import time


def extract_match_id(href):
    match = re.search(r"/matchcentre/(\d+)-scorecard", href)
    return match.group(1) if match else None


def extract_json_from_script(script_content):
    start = script_content.find("window.statsWidgetData = ")
    if start == -1:
        return None
    start += len("window.statsWidgetData = ")

    bracket_count = 0
    end = start
    for i, char in enumerate(script_content[start:]):
        if char == "{":
            bracket_count += 1
        elif char == "}":
            bracket_count -= 1
            if bracket_count == 0:
                end = start + i + 1
                break

    if bracket_count != 0:
        return None

    json_str = script_content[start:end]

    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        return None


def get_json_data(match_id):
    url = f"https://www.prokabaddi.com/matchcentre/{match_id}-scorecard"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": "https://www.prokabaddi.com/schedule-fixtures-results",
        "X-Requested-With": "XMLHttpRequest",
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        script_tag = soup.find(
            "script", string=lambda text: text and "window.statsWidgetData" in text
        )

        if script_tag:
            return extract_json_from_script(script_tag.string)

    print(f"Failed to retrieve data for match ID {match_id}")
    return None


def process_html_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, "html.parser")
    match_links = soup.find_all("a", href=re.compile(r"/matchcentre/\d+-scorecard"))

    match_data = {}
    for link in match_links:
        href = link["href"]
        match_id = extract_match_id(href)
        if match_id:
            json_data = get_json_data(match_id)
            if json_data:
                match_data[match_id] = json_data
            time.sleep(1)  # Add a delay to avoid overwhelming the server

    return match_data


# Usage
file_path = "hi.html"
match_data = process_html_file(file_path)

# Save the results to a JSON file
with open("match_data_SCRIPT.json", "w", encoding="utf-8") as f:
    json.dump(match_data, f, ensure_ascii=False, indent=2)

print("Data has been saved to match_data_SCRIPT.json")

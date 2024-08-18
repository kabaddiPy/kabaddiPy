import requests
from bs4 import BeautifulSoup
import pandas as pd

# Step 1: Fetch the HTML content
url = "https://www.prokabaddi.com/stats/44-21-player-successful-raids-statistics"  # Replace with the actual URL
response = requests.get(url)
html_content = response.text

print(html_content)

# Step 2: Parse the HTML content
soup = BeautifulSoup(html_content, "html.parser")

print(soup)
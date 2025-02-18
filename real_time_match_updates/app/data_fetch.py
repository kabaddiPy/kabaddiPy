import requests

KABADDI_API_URL = 'https://api.kabaddi.example/live'  # Replace with the actual API URL

def get_live_scores():
    try:
        response = requests.get(KABADDI_API_URL, timeout=5)  # Added timeout
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching live data: {e}")
        return {
            "score": "N/A",
            "players": []
        }

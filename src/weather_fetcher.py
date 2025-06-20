import os, json, logging
from datetime import datetime
import requests
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
DATA_DIR = "data"

def fetch_weather(city: str) -> dict:
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    resp = requests.get(BASE_URL, params=params)
    resp.raise_for_status()
    return resp.json()

def save_local(city: str, data: dict):
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    os.makedirs(DATA_DIR, exist_ok=True)
    filename = f"{city}_{timestamp}.json"
    path = os.path.join(DATA_DIR, filename)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    logger.info(f"Saved data to {path}")

def main(cities=None):
    if not cities:
        cities = ["Dhaka"]
    for city in cities:
        try:
            data = fetch_weather(city)
            save_local(city, data)
        except Exception as e:
            logger.error(f"Error fetching for {city}: {e}")

if __name__ == "__main__":
    main(["Dhaka", "London", "New York"])

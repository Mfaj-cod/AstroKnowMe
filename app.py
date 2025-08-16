from flask import Flask, render_template
import requests
from datetime import datetime as dt
import logging
import os
from dotenv import load_dotenv

#logging setting
logging.basicConfig(                    
    level=logging.WARNING,            # Minimum logging level
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler("astro_know_me.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("AstroKnowMe")

app = Flask(__name__)

load_dotenv()  # Load variables from .env
API_KEY = os.getenv("NASA_API_KEY", "DEMO_KEY")

#safe json requestor:-
def safe_json_request(url, params=None):
    try:
        r = requests.get(url, params=params, headers={"Accept": "application/json"}, timeout=10)
        if r.status_code == 200:
            try:
                return r.json()
            except requests.exceptions.JSONDecodeError:
                print(f"JSON decode error for {url}")
                return {}
        else:
            print(f"API Error {url}: Status {r.status_code}")
            return {}
    except requests.exceptions.RequestException as e:
        print(f"API Request Failed {url}: {e}")
        return {}


#functions:-

#astronomy picture of the day
def get_apod():
    return safe_json_request("https://api.nasa.gov/planetary/apod", {"api_key": API_KEY})

#near earth objects
def get_neo():
    return safe_json_request(
        "https://api.nasa.gov/neo/rest/v1/feed",
        {"api_key": API_KEY, "start_date": dt.now().date(), "end_date": dt.now().date()}
    )

#exoplanets discovered
def get_exoplanets():
    url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
    query = """
        SELECT TOP 5 pl_name, hostname, disc_year, disc_facility
        FROM ps
        ORDER BY disc_year DESC
    """
    params = {
        "query": query,
        "format": "json"
    }
    try:
        r = requests.post(url, data=params, headers={"Accept": "application/json"}, timeout=10)
        if r.status_code == 200:
            return r.json()
        else:
            print(f"Exoplanet API Error: {r.status_code} - {r.text}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Exoplanet API Request Failed: {e}")
        return []

# Mars Weather
def get_mars_weather():
    return safe_json_request("https://api.maas2.apollorion.com/")

def get_global_imagery():
    return safe_json_request("https://api.nasa.gov/EPIC/api/natural/images", {"api_key": API_KEY}) or []


#routes:-
@app.route("/")
def overview():
    apod = get_apod()
    neo = get_neo()
    exoplanets = get_exoplanets()
    mars = get_mars_weather()
    epic = get_global_imagery()

    logger.info(f"New user clicked on link.")
    return render_template(
        "overview.html",
        apod=apod,
        neo=neo,
        exoplanets=exoplanets,
        mars=mars,
        epic=epic
    )

@app.route("/PictureOfTheDay")
def picture_of_the_day():
    apod = get_apod()
    if not apod or "url" not in apod:
        apod = {
            "title": "No Data",
            "date": "",
            "media_type": "",
            "url": "",
            "explanation": "The APOD API did not return data. Please try again later."
        }
    logger.info(f"User viewed the apod.")
    return render_template("picture_of_day.html", apod=apod)



@app.route("/NearEarthObjects")
def near_earth_objects():
    neo_data = get_neo()
    # Flatten today's asteroid data
    today_key = list(neo_data.get("near_earth_objects", {}).keys())[0] if neo_data else None
    asteroids = neo_data.get("near_earth_objects", {}).get(today_key, []) if today_key else []
    logger.info(f"New user viewed near earth objects.")
    return render_template("near_earth_objects.html", asteroids=asteroids, date=today_key)

@app.route("/Exoplanets")
def exoplanets():
    planets = get_exoplanets()
    logger.info(f"New user viewed exoplanets.")
    return render_template("exoplanets.html", planets=planets)

@app.route("/MarsWeather")
def mars_weather():
    mars = get_mars_weather()
    logger.info(f"New user viewed mars weather.")
    return render_template("mars_weather.html", mars=mars)

@app.route("/GlobalImagery")
def global_imagery():
    epic_data = get_global_imagery()
    # Construct full image URLs
    images = []
    if epic_data:
        for img in epic_data[:9]:  # limit to latest 9 for performance
            date_parts = img['date'].split()[0].split('-')  # YYYY-MM-DD
            year, month, day = date_parts
            image_url = f"https://epic.gsfc.nasa.gov/archive/natural/{year}/{month}/{day}/jpg/{img['image']}.jpg"
            images.append({
                "url": image_url,
                "caption": img.get('caption', 'Earth Image'),
                "date": img['date']
            })
    logger.info(f"New user viewed global imagery.")
    return render_template("global_imagery.html", images=images)


def get_cosmic_weather():
    
    data = {
        "solar_wind": None,
        "k_index": None,
        "alerts": []
    }

    try:
        # Solar wind speed
        sw_url = "https://services.swpc.noaa.gov/products/solar-wind/plasma-1-day.json"
        sw_data = safe_json_request(sw_url)
        if isinstance(sw_data, list) and len(sw_data) > 1:
            latest = sw_data[-1]
            data["solar_wind"] = latest[1]  # Speed km/s

        # K-index
        kp_url = "https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json"
        kp_data = safe_json_request(kp_url)
        if isinstance(kp_data, list) and len(kp_data) > 1:
            latest_kp = kp_data[-1]
            data["k_index"] = latest_kp[1]

        # alerts
        alerts_url = "https://services.swpc.noaa.gov/products/alerts.json"
        alerts_data = safe_json_request(alerts_url)
        if isinstance(alerts_data, list) and len(alerts_data) > 1:
            for alert in alerts_data[1:6]:  # Take top 5
                data["alerts"].append({
                    "message": alert[3],
                    "issue_time": alert[0]
                })

    except Exception as e:
        print(f"Cosmic weather fetch error: {e}")
    logger.info(f"New user viewed cosmic weather.")
    return data

@app.route("/CosmicWeather")
def cosmic_weather():
    weather = get_cosmic_weather()
    logger.info(f"New user viewed cosmic weather.")
    return render_template("cosmic_weather.html", weather=weather)


if __name__ == "__main__":
    app.run(debug=True)


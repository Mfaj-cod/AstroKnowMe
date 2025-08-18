# 🚀 AstroKnowMe

AstroKnowMe is an **interactive, responsive Flask web app** that brings real-time astronomical and space data from NASA and NOAA right to your browser.  
It’s a one-stop dashboard for cosmic exploration — from the latest astronomy picture to near-Earth asteroid tracking and space weather.

---

## 🌌 Features

- **Overview Dashboard** — Quick summary of all data sources.
- **Picture of the Day** — Fetches NASA's Astronomy Picture of the Day (APOD) with description.
- **Near Earth Objects** — Live asteroid approach data from NASA NeoWs.
- **Cosmic Weather** — Solar wind, geomagnetic activity, and alerts from NOAA SWPC.
- **Exoplanets** — Recently discovered planets from NASA Exoplanet Archive.
- **Mars Weather** — Latest (archived) InSight mission weather data.
- **Global Imagery** — Recent Earth images from NASA’s EPIC camera.
- **Fully Responsive** — Works on desktop and mobile.
- **Dark Space Theme** — Gradient accents, hover effects, and a creative logo.

---

## 🛠 Tech Stack

- **Backend:** Python 3, Flask
- **Frontend:** HTML, Bootstrap 5, CSS
- **APIs Used:**
  - [NASA APOD](https://api.nasa.gov/)
  - [NASA NeoWs](https://api.nasa.gov/)
  - [NASA EPIC](https://epic.gsfc.nasa.gov/)
  - [NASA Exoplanet Archive](https://exoplanetarchive.ipac.caltech.edu/)
  - [InSight Mars Weather (archived)](https://api.maas2.apollorion.com/)
  - [NOAA SWPC Space Weather](https://services.swpc.noaa.gov/)

---

## 📦 Installation
⚡ Installation & Setup

Clone the repository:

git clone https://github.com/Mfaj-cod/AstroKnowMe
cd AstroKnowMe

Create a virtual environment:

python -m venv venv


Activate the virtual environment:

Windows:

venv\Scripts\activate


Mac/Linux:

source venv/bin/activate


Install dependencies:

pip install -r requirements.txt


Set environment variables (NASA API key required):

export NASA_API_KEY='YOUR_API_KEY'


Run the application:

python app.py


Visit in browser:

http://127.0.0.1:5000

🌐 Live Demo

Explore the live application here: https://www.astroknowme.live

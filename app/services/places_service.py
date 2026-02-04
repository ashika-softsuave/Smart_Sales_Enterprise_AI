import requests
from app.core.config import settings


def fetch_nearby_stores(lat: float, lng: float, limit: int = 6):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{lat},{lng}",
        "radius": 5000,
        "type": "supermarket",
        "key": settings.GOOGLE_MAPS_API_KEY
    }

    res = requests.get(url, params=params).json()

    if res["status"] != "OK":
        return []

    return [
        {
            "name": place["name"],
            "lat": place["geometry"]["location"]["lat"],
            "lng": place["geometry"]["location"]["lng"]
        }
        for place in res["results"][:limit]
    ]

import requests
from app.core.config import settings

def fetch_nearby_stores(location: str, limit: int = 6):
    """
    Uses Google Places API to fetch nearby stores
    """

    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": f"supermarket in {location}",
        "key": settings.GOOGLE_MAPS_API_KEY
    }

    res = requests.get(url, params=params).json()

    if res["status"] != "OK":
        raise Exception("Failed to fetch nearby stores")

    stores = []
    for place in res["results"][:limit]:
        stores.append(place["name"])

    return stores

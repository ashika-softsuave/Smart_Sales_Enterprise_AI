"""
Handles conversational location context
and Google Maps place resolution
"""
import requests
from app.core.config import settings


# ---- In-memory chat context (per user) ----
USER_LOCATION_CONTEXT = {}


# ---- Geocoding with India bias (IMPORTANT) ----
def geocode_location(query: str) -> dict:
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": query,
        "key": settings.GOOGLE_MAPS_API_KEY
    }

    res = requests.get(url, params=params).json()

    if res["status"] != "OK":
        raise ValueError(f"Unable to locate place: {query}")

    location = res["results"][0]["geometry"]["location"]

    return {
        "address": res["results"][0]["formatted_address"],
        "lat": location["lat"],
        "lng": location["lng"]
    }


# ---- Fetch nearby stores dynamically ----
def fetch_nearby_stores(lat: float, lng: float, limit: int = 6):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{lat},{lng}",
        "radius": 5000,  # 5km
        "type": "supermarket",
        "key": settings.GOOGLE_MAPS_API_KEY
    }

    res = requests.get(url, params=params).json()

    if res["status"] != "OK":
        raise ValueError("No nearby stores found")

    return [
        {
            "name": place["name"],
            "lat": place["geometry"]["location"]["lat"],
            "lng": place["geometry"]["location"]["lng"]
        }
        for place in res["results"][:limit]
    ]


# ---- Chat context helpers ----
def set_waiting_for_location(user_id: int):
    USER_LOCATION_CONTEXT[user_id] = {
        "awaiting_location": True
    }


def set_user_location(user_id: int, location: str):
    USER_LOCATION_CONTEXT[user_id] = {
        "awaiting_location": False,
        "location": location
    }


def get_user_location_context(user_id: int):
    return USER_LOCATION_CONTEXT.get(user_id)

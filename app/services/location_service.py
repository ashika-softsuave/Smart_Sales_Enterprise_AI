"""
Handles temporary conversational context
(like waiting for user's location)
"""
import requests
from app.core.config import settings


def geocode_location(query: str) -> str:
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": query,
        "key": settings.GOOGLE_MAPS_API_KEY
    }

    res = requests.get(url, params=params).json()

    if res["status"] != "OK":
        raise Exception(f"Unable to locate place: {query}")

    return res["results"][0]["formatted_address"]

USER_LOCATION_CONTEXT = {}

def fetch_nearby_stores(location: str, limit: int = 6):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": f"supermarket near {location}",
        "key": settings.GOOGLE_MAPS_API_KEY
    }

    res = requests.get(url, params=params).json()

    if res["status"] != "OK":
        raise Exception("No stores found")

    return [
        place["name"]
        for place in res["results"][:limit]
    ]

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

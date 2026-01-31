import requests
from app.core.config import settings


def get_directions(origin: str, destination: str, waypoints: list[str]):
    """
    Fetch route directions from Google Maps API
    and return distance, duration, polyline, steps
    """

    url = "https://maps.googleapis.com/maps/api/directions/json"

    params = {
        "origin": origin,
        "destination": destination,
        "waypoints": "|".join(waypoints),
        "key": settings.GOOGLE_MAPS_API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data.get("status") != "OK":
        raise Exception(f"Google Maps API Error: {data.get('status')}")

    route = data["routes"][0]
    legs = route["legs"]

    # ✅ Distance (km)
    total_distance = sum(
        leg["distance"]["value"] for leg in legs
    ) / 1000

    # ✅ Duration (minutes)
    total_duration = sum(
        leg["duration"]["value"] for leg in legs
    ) / 60

    # ✅ Steps extraction (FIX)
    steps = []
    for leg in legs:
        for step in leg.get("steps", []):
            steps.append({
                "instruction": step["html_instructions"],
                "distance": step["distance"]["text"],
                "duration": step["duration"]["text"],
                "start_location": step["start_location"],
                "end_location": step["end_location"]
            })

    return {
        "distance_km": round(total_distance, 2),
        "duration_minutes": round(total_duration),
        "polyline": route["overview_polyline"]["points"],
        "steps": steps
    }


def calculate_route_km(origin: str, destination: str, waypoints: list[str]) -> float:
    """
    Lightweight distance calculator (no steps)
    """

    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": origin,
        "destination": destination,
        "waypoints": "|".join(waypoints),
        "key": settings.GOOGLE_MAPS_API_KEY
    }

    res = requests.get(url, params=params).json()

    if res.get("status") != "OK":
        raise Exception(f"Google Maps API Error: {res.get('status')}")

    distance = sum(
        leg["distance"]["value"]
        for leg in res["routes"][0]["legs"]
    ) / 1000

    return round(distance, 2)

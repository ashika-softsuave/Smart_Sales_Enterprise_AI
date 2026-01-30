import requests
import os
from app.core.config import settings

GOOGLE_MAPS_API__KEY=os.getenv("GOOGLE_MAPS_API_KEY")

def get_directions(origin:str,destination:str,waypoints:list[str]):
    url="https://maps.googleapis.com/maps/api/directions/json"

    params={
        "origin": origin,
        "destination":destination,
        "waypoints":"|".join(waypoints),
        "key": settings.GOOGLE_MAPS_API_KEY
    }

    response=requests.get(url,params=params)
    data=response.json()

    if data["status"]!="OK":
        raise Exception("Google Maps API Error")

    route=data["routes"][0]
    leg_data=route["legs"]

    total_didtsance=sum(
        leg["distance"]["value"] for leg in leg_data
    )/1000 #meters->km

    total_duration=sum(
        leg["duration"]["value"]for leg in leg_data
    )/60 #seconda->minutes

    return{
        "distance_km":round(total_distance,2),
        "durationminutes": round(total_duration),
        "polyline":route["overview_polyline"]["points"],
        "steps":steps
    }

def calculate_route_km(origin, destination, waypoints):
    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": origin,
        "destination": destination,
        "waypoints": "|".join(waypoints),
        "key": settings.GOOGLE_MAPS_API_KEY
    }

    res = requests.get(url, params=params).json()

    distance = sum(
        leg["distance"]["value"]
        for leg in res["routes"][0]["legs"]
    ) / 1000

    return round(distance, 2)
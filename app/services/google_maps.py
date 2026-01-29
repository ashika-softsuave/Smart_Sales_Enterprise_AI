import requests
import os

GOOGLE_MAPS_API__KEY=os.getenv("GOOGLE_MAPS_API_KEY")

def get_directions(origin:str,destination:str,waypoints:list[str]):
    url="https://maps.googleapis.com/maps/api/directions/json"

    params={
        "origin": origin,
        "destination":destination,
        "waypoints":"|".join(waypoints),
        "key:" GOOGLE_MAPS_API_KEY
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




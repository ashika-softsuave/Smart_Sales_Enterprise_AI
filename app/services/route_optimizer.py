from app.services.google_maps import get_directions

def optimize_route(start_location:str,store_locations:list[str],end_location:str):

    route_data=get_directions(origin=start_location,
                              destination=end_location,
                              waypoint=store_locations
                              )

    return {"start":start_location,
            "end":end_location,
            **route_data}

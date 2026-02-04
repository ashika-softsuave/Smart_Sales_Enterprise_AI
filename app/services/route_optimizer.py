from app.services.google_maps import get_directions


def optimize_route(
    start_location: str,
    store_locations: list[str],
    end_location: str
):
    """
    start_location, end_location, waypoints MUST be lat,lng strings
    """

    route_data = get_directions(
        origin=start_location,
        destination=end_location,
        waypoints=store_locations
    )

    return route_data

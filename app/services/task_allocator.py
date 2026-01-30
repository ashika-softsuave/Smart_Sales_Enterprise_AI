from app.services.route_optimizer import optimize_route


def allocate_task(salesman_id: int):
    """
    Temporary static allocator
    (Can be replaced with DB logic later)
    """

    start_location = "Sholinganallur, Chennai"
    end_location = "Navalur, Chennai"

    store_locations = [
        "Reliance Store Navalur",
        "Anbu Supermarket OMR"
    ]

    raw_route = optimize_route(
        start_location=start_location,
        store_locations=store_locations,
        end_location=end_location
    )

    # Normalize route into schema-friendly format
    route = []
    for place in raw_route:
        route.append({
            "location": place,
            "latitude": None,
            "longitude": None
        })

    return {
        "assigned_target": 10,
        "tasks_reached": 0,
        "tasks_pending": 10,
        "route_assigned": route
    }

from app.services.route_optimizer import optimize_route
from app.services.places_service import fetch_nearby_stores
from app.services.location_service import geocode_location


def allocate_task_from_chat(
    salesman_id: int,
    user_location: str,
    task_limit: int = 6
):
    """
    Full AI-driven task allocation from natural language location
    """

    # 1️⃣ Resolve vague human location → exact Google Maps address
    resolved_location = geocode_location(user_location)

    # 2️⃣ Fetch nearby stores dynamically
    store_locations = fetch_nearby_stores(
        resolved_location,
        limit=task_limit
    )

    if not store_locations:
        raise Exception("No stores found near your location")

    # 3️⃣ Optimize route
    route_data = optimize_route(
        start_location=resolved_location,
        store_locations=store_locations,
        end_location=resolved_location
    )

    # 4️⃣ Normalize route for frontend / chat
    route = [{"location": resolved_location, "latitude": None, "longitude": None}]

    for store in store_locations:
        route.append({
            "location": store,
            "latitude": None,
            "longitude": None
        })

    route.append({
        "location": resolved_location,
        "latitude": None,
        "longitude": None
    })

    # 5️⃣ Final response
    return {
        "assigned_target": len(store_locations),
        "tasks_reached": 0,
        "tasks_pending": len(store_locations),
        "route_assigned": route,
        "summary": {
            "distance_km": route_data["distance_km"],
            "duration_minutes": route_data["duration_minutes"]
        }
    }

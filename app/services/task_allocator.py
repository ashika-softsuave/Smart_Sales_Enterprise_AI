from app.services.route_optimizer import optimize_route

def allocate_task(salesman_id:int):
    start_location="Sholinganallur,Chennai"
    end_location="Navalur,Chennai"

    store_locations=[
        "Reliance Store Navalur",
        "Anbu Supermarket OMR"
    ]
    route=optimize_route(
        start_location=start_location,
        store_locations=store_locations,
        end_location=end_location)

    return{
        "assigned_target":10,
        "tasks_reached":0,
        "tasks_pending":10,
        "route_assigned":route
    }
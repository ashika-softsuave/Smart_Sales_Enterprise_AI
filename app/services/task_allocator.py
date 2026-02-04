from sqlalchemy.orm import Session
from datetime import datetime, date

from app.models.salesman import Salesman
from app.models.team_product import TeamProduct
from app.models.product import Product
from app.models.daily_sales_log import DailySalesLog

from app.services.route_optimizer import optimize_route
from app.services.location_service import geocode_location
from app.services.places_service import fetch_nearby_stores


def allocate_task_from_chat(
    salesman_id: int,
    user_location: str,
    db: Session,
    task_limit: int = 6
):
    """
    AI-driven daily task allocation for salesman
    """

    # =========================
    # 1. Fetch salesman
    # =========================
    salesman = (
        db.query(Salesman)
        .filter(Salesman.id == salesman_id)
        .first()
    )

    if not salesman:
        raise Exception("Salesman not found.")

    if not salesman.team_id:
        raise Exception(
            "You are not assigned to any team yet. Please contact your manager."
        )

    # =========================
    # 2. Fetch products assigned to team
    # =========================
    team_products = (
        db.query(Product, TeamProduct.daily_target)
        .join(TeamProduct, Product.id == TeamProduct.product_id)
        .filter(TeamProduct.team_id == salesman.team_id)
        .all()
    )

    assigned_products = [
        {
            "product": product.product_name,
            "daily_target": daily_target
        }
        for product, daily_target in team_products
    ]

    # =========================
    # 3. Resolve location
    # =========================
    resolved = geocode_location(user_location)

    if not resolved or "lat" not in resolved or "lng" not in resolved:
        raise Exception(
            "Unable to understand your location. Please try a nearby landmark."
        )

    start_latlng = f'{resolved["lat"]},{resolved["lng"]}'

    # =========================
    # 4. Fetch nearby stores
    # =========================
    stores = fetch_nearby_stores(
        lat=resolved["lat"],
        lng=resolved["lng"],
        limit=task_limit
    )

    if not stores:
        return {
            "assigned_target": 0,
            "tasks_reached": 0,
            "tasks_pending": 0,
            "assigned_products": assigned_products,
            "route_assigned": [],
            "summary": {
                "distance_km": 0,
                "duration_minutes": 0
            },
            "note": "No nearby stores found for today."
        }

    valid_stores = [
        s for s in stores
        if s.get("lat") is not None and s.get("lng") is not None
    ]

    if not valid_stores:
        raise Exception(
            "Stores found, but location data was incomplete."
        )

    store_latlngs = [
        f'{s["lat"]},{s["lng"]}' for s in valid_stores
    ]

    # =========================
    # 5. Optimize route
    # =========================
    route_data = optimize_route(
        start_location=start_latlng,
        store_locations=store_latlngs,
        end_location=start_latlng
    )

    distance_km = route_data.get("distance_km", 0)

    # =========================
    # 6. Build route response
    # =========================
    route = [{
        "location": resolved["address"],
        "latitude": resolved["lat"],
        "longitude": resolved["lng"]
    }]

    for s in valid_stores:
        route.append({
            "location": s["name"],
            "latitude": s["lat"],
            "longitude": s["lng"]
        })

    route.append(route[0])

    # =========================
    # 7. DAILY SALES LOG (FIXED)
    # =========================
    today = date.today()

    log = (
        db.query(DailySalesLog)
        .filter(
            DailySalesLog.salesman_id == salesman_id,
            DailySalesLog.work_date == today,
            DailySalesLog.end_time.is_(None)
        )
        .first()
    )

    if not log:
        log = DailySalesLog(
            salesman_id=salesman_id,
            work_date=today,
            start_time=datetime.utcnow(),
            travel_km=distance_km
        )
        db.add(log)
    else:
        # accumulate travel km safely
        log.travel_km = (log.travel_km or 0) + distance_km

    db.commit()
    db.refresh(log)

    # =========================
    # 8. Final response
    # =========================
    return {
        "assigned_target": len(valid_stores),
        "tasks_reached": 0,
        "tasks_pending": len(valid_stores),
        "assigned_products": assigned_products,
        "route_assigned": route,
        "summary": {
            "distance_km": round(distance_km, 2),
            "duration_minutes": route_data.get("duration_minutes", 0)
        }
    }

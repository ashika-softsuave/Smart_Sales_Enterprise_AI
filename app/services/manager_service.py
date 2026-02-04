from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException

from app.models.team import Team
from app.models.salesman import Salesman
from app.models.store import Store
from app.models.product import Product
from app.models.daily_sales_log import DailySalesLog


# ============================
# MANAGER DASHBOARD (FIXED)
# ============================
def get_manager_dashboard(manager_id: int, db: Session):
    teams = db.query(Team).filter(Team.manager_id == manager_id).all()
    if not teams:
        raise HTTPException(status_code=404, detail="No teams found")

    team_data = []

    for t in teams:
        # ✅ Aggregate sales from DailySalesLog
        stats = (
            db.query(
                func.coalesce(func.sum(DailySalesLog.items_sold), 0).label("sold"),
                func.coalesce(func.sum(DailySalesLog.items_pending), 0).label("pending")
            )
            .join(Salesman, Salesman.id == DailySalesLog.salesman_id)
            .filter(Salesman.team_id == t.id)
            .one()
        )

        sold = stats.sold
        pending = stats.pending
        total = sold + pending

        # ✅ Fetch teammates properly
        salesmen = (
            db.query(Salesman)
            .filter(Salesman.team_id == t.id)
            .all()
        )

        teammates = [
            {
                "salesman_id": s.id,
                "name": s.name,
                "email": s.email
            }
            for s in salesmen
        ]

        team_data.append({
            "team_id": t.id,
            "team_name": t.team_name,
            "tasks_reached": sold,
            "total_tasks": total,
            "teammates": teammates
        })

    return {
        "manager_id": manager_id,
        "teams": team_data
    }


# ============================
# MANAGER SALESMEN (UNCHANGED)
# ============================
def get_manager_salesmen(manager_id: int, db: Session):
    teams = db.query(Team).filter(Team.manager_id == manager_id).all()
    team_ids = [t.id for t in teams]

    salesmen = db.query(Salesman).filter(Salesman.team_id.in_(team_ids)).all()

    return {
        "salesmen": [
            {
                "salesman_id": s.id,
                "name": s.name,
                "email": s.email,
                "daily_travel_km": s.daily_travel_km
            } for s in salesmen
        ]
    }


# ============================
# STORE STATUS (UNCHANGED)
# ============================
def get_store_status(db: Session):
    stores = db.query(Store).all()

    result = []
    for s in stores:
        product = db.query(Product).filter(Product.id == s.product_id).first()
        result.append({
            "store_name": s.store_name,
            "product": product.product_name if product else None,
            "is_assigned": s.is_assigned
        })

    return {"stores": result}


# ============================
# MANUAL TEAM UPDATE (UNCHANGED)
# ============================
def update_team_progress(team_id: int, tasks_reached: int, total_tasks: int, db: Session):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    team.tasks_reached = tasks_reached
    team.total_tasks = total_tasks
    db.commit()

    return {"message": "Team progress updated"}

from sqlalchemy.orm import Session
from app.models.team import Team
from app.models.salesman import Salesman
from app.models.store import Store
from app.models.product import Product
from fastapi import HTTPException


def get_manager_dashboard(manager_id: int, db: Session):
    teams = db.query(Team).filter(Team.manager_id == manager_id).all()
    if not teams:
        raise HTTPException(status_code=404, detail="No teams found")

    return {
        "manager_id": manager_id,
        "teams": [
            {
                "team_id": t.id,
                "team_name": t.team_name,
                "tasks_reached": t.tasks_reached,
                "total_tasks": t.total_tasks,
                "teammates": t.teammates_names
            } for t in teams
        ]
    }


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
                "daily_travel_km": s.daily_travel
            } for s in salesmen
        ]
    }


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


def update_team_progress(team_id: int, tasks_reached: int, total_tasks: int, db: Session):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    team.tasks_reached = tasks_reached
    team.total_tasks = total_tasks
    db.commit()

    return {"message": "Team progress updated"}

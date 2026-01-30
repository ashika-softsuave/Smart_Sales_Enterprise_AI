from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.manager_service import (
    get_manager_dashboard,
    get_manager_salesmen,
    get_store_status,
    update_team_progress
)

router = APIRouter()


@router.get("/dashboard")
def dashboard(manager_id: int, db: Session = Depends(get_db)):
    return get_manager_dashboard(manager_id, db)


@router.get("/salesmen/{manager_id}")
def salesmen(manager_id: int, db: Session = Depends(get_db)):
    return get_manager_salesmen(manager_id, db)


@router.get("/stores")
def stores(db: Session = Depends(get_db)):
    return get_store_status(db)


@router.post("/update-team-progress")
def update_progress(team_id: int, tasks_reached: int, total_tasks: int, db: Session = Depends(get_db)):
    return update_team_progress(team_id, tasks_reached, total_tasks, db)

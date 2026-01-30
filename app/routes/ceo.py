from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.ceo_service import (
    get_ceo_dashboard,
    get_all_salesmen,
    get_company_summary,
    export_company_data
)

router = APIRouter()

@router.get("/dashboard")
def ceo_dashboard(db: Session = Depends(get_db)):
    return get_ceo_dashboard(db)

@router.get("/salesmen")
def all_salesmen(db: Session = Depends(get_db)):
    return get_all_salesmen(db)

@router.get("/summary")
def company_summary(db: Session = Depends(get_db)):
    return get_company_summary(db)

@router.get("/export")
def export_data(db: Session = Depends(get_db)):
    return export_company_data(db)

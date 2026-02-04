from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import require_role, get_current_user
from app.models.team import Team
from app.models.team_product import TeamProduct
from app.models.salesman import Salesman
from app.models.product import Product

from app.services.manager_service import (
    get_manager_dashboard,
    get_manager_salesmen,
    get_store_status,
    update_team_progress
)
from app.models.product import Product
from app.core.security import require_role

router = APIRouter(prefix="/manager", tags=["Manager"])


# 🔹 Dashboard
@router.get("/dashboard")
def dashboard(
    db: Session = Depends(get_db),
    manager=Depends(require_role(["manager"]))
):
    return get_manager_dashboard(manager.id, db)


# 🔹 Manager's salesmen
@router.get("/salesmen")
def salesmen(
    db: Session = Depends(get_db),
    manager=Depends(require_role(["manager"]))
):
    return get_manager_salesmen(manager.id, db)


# 🔹 Create team
@router.post("/create-team")
def create_team(
    team_name: str,
    db: Session = Depends(get_db),
    manager=Depends(require_role(["manager"]))
):
    team = Team(
        name=team_name,        # ✅ FIX HERE
        team_name=team_name,   # optional, keep for UI if needed
        manager_id=manager.id
    )

    db.add(team)
    db.commit()
    db.refresh(team)

    return {
        "message": "Team created successfully",
        "team_id": team.id,
        "team_name": team.name
    }


# 🔹 Assign salesman to team
@router.post("/assign-salesman")
def assign_salesman(
    salesman_id: int,
    team_id: int,
    db: Session = Depends(get_db),
    manager=Depends(require_role(["manager"]))
):
    salesman = db.query(Salesman).filter(
        Salesman.id == salesman_id,
        Salesman.role == "salesman"
    ).first()

    if not salesman:
        raise HTTPException(status_code=404, detail="Invalid salesman")

    salesman.team_id = team_id
    db.commit()

    return {"message": "Salesman assigned to team"}

@router.post("/create-product")
def create_product(
    product_name: str,
    category: str,
    price: float,
    db: Session = Depends(get_db),
    manager=Depends(require_role(["manager"]))
):
    product = Product(
        product_name=product_name,
        category=category,
        price=price
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    return {
        "message": "Product created successfully",
        "product_id": product.id,
        "product_name": product.product_name
    }

# 🔹 Assign product to team
@router.post("/assign-product")
def assign_product(
    team_id: int,
    product_id: int,
    daily_target: int,
    db: Session = Depends(get_db),
    manager=Depends(require_role(["manager"]))
):
    mapping = TeamProduct(
        team_id=team_id,
        product_id=product_id,
        daily_target=daily_target
    )
    db.add(mapping)
    db.commit()

    return {"message": "Product assigned to team"}

@router.get("/products")
def list_products(
    db: Session = Depends(get_db),
    manager=Depends(require_role(["manager"]))
):
    products = db.query(Product).all()

    return {
        "products": [
            {
                "product_id": p.id,
                "name": p.product_name,
                "category": p.category,
                "price": p.price
            }
            for p in products
        ]
    }


# 🔹 Store status
@router.get("/stores")
def stores(db: Session = Depends(get_db)):
    return get_store_status(db)


# 🔹 Update team progress
@router.post("/update-team-progress")
def update_progress(
    team_id: int,
    tasks_reached: int,
    total_tasks: int,
    db: Session = Depends(get_db),
    manager=Depends(require_role(["manager"]))
):
    return update_team_progress(team_id, tasks_reached, total_tasks, db)
# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
#
# from app.core.database import get_db
# from app.services.manager_service import (
#     get_manager_dashboard,
#     get_manager_salesmen,
#     get_store_status,
#     update_team_progress
# )
#
# router = APIRouter()
#
#
# @router.get("/dashboard")
# def dashboard(manager_id: int, db: Session = Depends(get_db)):
#     return get_manager_dashboard(manager_id, db)
#
#
# @router.get("/salesmen/{manager_id}")
# def salesmen(manager_id: int, db: Session = Depends(get_db)):
#     return get_manager_salesmen(manager_id, db)
#
#
# @router.get("/stores")
# def stores(db: Session = Depends(get_db)):
#     return get_store_status(db)
#
#
# @router.post("/update-team-progress")
# def update_progress(team_id: int, tasks_reached: int, total_tasks: int, db: Session = Depends(get_db)):
#     return update_team_progress(team_id, tasks_reached, total_tasks, db)

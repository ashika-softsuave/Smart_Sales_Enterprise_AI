from sqlalchemy.orm import Session
from app.models.salesman import Salesman
from app.models.team_product import TeamProduct

def get_salesman_daily_target(db: Session, salesman_id: int) -> int:
    salesman = db.query(Salesman).filter(Salesman.id == salesman_id).first()

    if not salesman or not salesman.team_id:
        return 0

    result = (
        db.query(TeamProduct.daily_target)
        .filter(TeamProduct.team_id == salesman.team_id)
        .all()
    )

    return sum(r[0] for r in result)

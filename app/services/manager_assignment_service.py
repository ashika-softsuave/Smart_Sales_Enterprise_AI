from sqlalchemy.orm import Session
from app.models.team_product import TeamProduct

def assign_product_to_team(
    db: Session,
    team_id: int,
    product_id: int,
    daily_target: int
):
    assignment = TeamProduct(
        team_id=team_id,
        product_id=product_id,
        daily_target=daily_target
    )
    db.add(assignment)
    db.commit()
    db.refresh(assignment)

    return assignment

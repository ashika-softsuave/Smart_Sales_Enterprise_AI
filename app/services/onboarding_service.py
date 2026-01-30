from sqlalchemy.orm import Session
from app.models.salesman import Salesman
from app.core.security import hash_password

def onboard_user(data, db: Session):
    existing_user = db.query(Salesman).filter(
        Salesman.email == data.email
    ).first()

    if existing_user:
        return {
            "status": "error",
            "message": "User already exists"
        }

    user = Salesman(
        name=data.name,
        email=data.email,
        password=hash_password(data.password),
        role=data.role,
        team_id=data.team_id
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "status": "success",
        "message": "You are successfully onboarded 🎉",
        "user_id": user.id
    }

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import (
    verify_password,
    hash_password,
    create_access_token,
    get_db
)
from app.models.salesman import Salesman
from app.schemas.auth_schema import LoginRequest, LoginResponse, ChatOnboardRequest

router = APIRouter()

# Login API
@router.post("/login", response_model=LoginResponse)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    user = db.query(Salesman).filter(
        Salesman.email == request.email
    ).first()

    if not user or not verify_password(
        request.password, user.password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    token = create_access_token(
        data={"sub": user.id, "role": user.role}
    )

    return LoginResponse(
        access_token=token,
        token_type="bearer",
        role=user.role
    )

# Chatbot onboarding
@router.post("/chat-onboard")
def chat_onboard(
    request: ChatOnboardRequest,
    db: Session = Depends(get_db)
):
    existing_user = db.query(Salesman).filter(
        Salesman.email == request.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )

    new_user = Salesman(
        name=request.name,
        email=request.email,
        password=hash_password(request.password),
        role=request.role,
        team_id=request.team_id
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "Salesman onboarded successfully",
        "salesman_id": new_user.id
    }

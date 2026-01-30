from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import (
    verify_password,
    hash_password,
    create_access_token
)
from app.models.salesman import Salesman
from app.schemas.auth_schema import (
    LoginRequest,
    LoginResponse,
    RegisterRequest
)

router = APIRouter()


# REGISTER
@router.post("/register", status_code=201)
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):
    existing_user = db.query(Salesman).filter(
        Salesman.email == request.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = Salesman(
        name=request.name,
        email=request.email,
        hashed_password=hash_password(request.password),
        role=request.role,
        team_id=request.team_id
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "user_id": new_user.id
    }


# LOGIN
@router.post("/login", response_model=LoginResponse)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    user = db.query(Salesman).filter(
        Salesman.email == request.email
    ).first()

    if not user or not verify_password(
        request.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    token = create_access_token(
        data={"sub": str(user.id), "role": user.role}
    )

    return LoginResponse(
        access_token=token,
        token_type="bearer",
        role=user.role
    )


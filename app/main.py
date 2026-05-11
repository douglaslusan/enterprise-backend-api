from fastapi import FastAPI, Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database.database import engine, Base
from app.database.dependencies import get_db

from app.models.user_model import User

from app.schemas.user_schema import UserCreate
from app.schemas.user_schema import UserLogin

from app.repositories.user_repository import create_user
from app.repositories.user_repository import get_user_by_email

from app.auth.security import (
    verify_password,
    create_access_token
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Enterprise Backend API",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "API running successfully"
    }


@app.post("/users")
def create_new_user(
        user: UserCreate,
        db: Session = Depends(get_db)
):

    return create_user(db, user)

@app.post("/login")
def login(
        user: UserLogin,
        db: Session = Depends(get_db)
):

    db_user = get_user_by_email(
        db,
        user.email
    )

    if not db_user:

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    valid_password = verify_password(
        user.password,
        db_user.password
    )

    if not valid_password:

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    access_token = create_access_token(
        data={
            "sub": db_user.email
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
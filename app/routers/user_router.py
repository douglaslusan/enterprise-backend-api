from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.database.database import SessionLocal

from app.schemas.user_schema import UserCreate
from app.schemas.user_response import UserResponse
from app.schemas.user_update import UserUpdate

from app.services.user_service import (
    create_user_service,
    get_all_users_service,
    get_user_by_id_service,
    delete_user_service,
    update_user_service,
    authenticate_user
)

from app.auth.security import create_access_token, create_refresh_token, verify_token
from app.auth.dependencies import get_current_user
from app.auth.permissions import require_admin

from app.exceptions.user_exceptions import (
    UserAlreadyExistsException
)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/", response_model=UserResponse)
def create_new_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    try:
        return create_user_service(db, user)

    except UserAlreadyExistsException as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = authenticate_user(
        db,
        form_data.username,
        form_data.password
    )

    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    access_token = create_access_token(
        data={"sub": user.email}
    )

    refresh_token = create_refresh_token(
        data={"sub": user.email}
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=UserResponse)
def read_users_me(
    current_user = Depends(get_current_user)
):

    return current_user


@router.get("/", response_model=list[UserResponse])
def get_all_users(
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):

    return get_all_users_service(db)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):

    user = get_user_by_id_service(
        db,
        user_id
    )

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user_route(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):

    updated_user = update_user_service(
        db,
        user_id,
        user_data
    )

    if not updated_user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return updated_user


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):

    result = delete_user_service(
        db,
        user_id
    )

    if not result:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return result

@router.post("/refresh")
def refresh_token(token: str):

    email = verify_token(token)

    if not email:

        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )

    new_access_token = create_access_token(
        data={"sub": email}
    )

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }
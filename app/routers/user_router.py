from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException
from app.exceptions.user_exceptions import (
    UserAlreadyExistsException
)

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
    update_user_service
)

from app.auth.dependencies import get_current_user
from app.auth.security import create_access_token

from app.repositories.user_repository import authenticate_user

from fastapi import HTTPException

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
        return {"error": "Invalid credentials"}

    access_token = create_access_token(
        data={"sub": user.email}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=UserResponse)
def read_users_me(current_user = Depends(get_current_user)):
    return current_user

@router.get("/", response_model=list[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    return get_all_users_service(db)

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id_service(db, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    result = delete_user_service(db, user_id)

    if not result:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return result

@router.put("/{user_id}", response_model=UserResponse)
def update_user_route(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db)
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
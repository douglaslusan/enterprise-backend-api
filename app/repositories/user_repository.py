from sqlalchemy.orm import Session

from app.models.user_model import User
from app.schemas.user_schema import UserCreate
from app.auth.security import hash_password, verify_password


def create_user(db: Session, user: UserCreate):

    hashed_password = hash_password(
        user.password
    )

    db_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password,
        role=user.role
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None

    if not verify_password(password, user.password):
        return None

    return user


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session):
    return db.query(User).all()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def delete_user(db: Session, user):
    db.delete(user)
    db.commit()


def update_user(db: Session, user):
    db.commit()
    db.refresh(user)
    return user


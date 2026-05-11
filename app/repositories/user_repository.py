from sqlalchemy.orm import Session

from app.models.user_model import User
from app.schemas.user_schema import UserCreate

from app.auth.security import hash_password


def create_user(
        db: Session,
        user: UserCreate
):

    hashed_password = hash_password(user.password)

    db_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password
    )

    db.add(db_user)

    db.commit()

    db.refresh(db_user)

    return db_user


def get_user_by_email(
        db: Session,
        email: str
):

    return db.query(User).filter(
        User.email == email
    ).first()
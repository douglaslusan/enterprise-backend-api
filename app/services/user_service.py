from sqlalchemy.orm import Session

from app.auth.security import hash_password

from app.repositories.user_repository import (
    create_user,
    get_user_by_email
)

from app.exceptions.user_exceptions import (
    UserAlreadyExistsException
)

from app.repositories.user_repository import update_user

from app.schemas.user_schema import UserCreate


from app.repositories.user_repository import (
    get_users,
    get_user_by_id,
    delete_user
)


def create_user_service(db, user):

    existing_user = get_user_by_email(
        db,
        user.email
    )

    if existing_user:
        raise UserAlreadyExistsException(
            "User already exists"
        )

    hashed_password = hash_password(
        user.password
    )

    user.password = hashed_password

    return create_user(db, user)


def get_all_users_service(db):
    return get_users(db)


def get_user_by_id_service(db, user_id):
    return get_user_by_id(db, user_id)


def delete_user_service(db, user_id):
    user = get_user_by_id(db, user_id)

    if not user:
        return None

    delete_user(db, user)

    return {"message": "User deleted"}

def update_user_service(db, user_id, user_data):
    user = get_user_by_id(db, user_id)

    if not user:
        return None

    if user_data.email:
        user.email = user_data.email

    if user_data.password:
        user.password = hash_password(
            user_data.password
        )

    return update_user(db, user)
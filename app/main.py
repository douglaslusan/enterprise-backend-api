from fastapi import FastAPI

from app.models.user_model import Base
from app.database.database import engine
from app.routers.user_router import router as user_router

from app.exceptions.user_exceptions import (
    UserAlreadyExistsException
)

from app.handlers.exception_handlers import (
    user_already_exists_handler
)

app = FastAPI()

app.add_exception_handler(
    UserAlreadyExistsException,
    user_already_exists_handler
)

app.include_router(user_router)
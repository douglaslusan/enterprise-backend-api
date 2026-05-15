from fastapi import FastAPI

from app.models.user_model import Base
from app.database.database import engine
from app.routers.user_router import router as user_router


app = FastAPI()

app.include_router(user_router)
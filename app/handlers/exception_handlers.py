from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions.user_exceptions import (
    UserAlreadyExistsException
)


async def user_already_exists_handler(
    request: Request,
    exc: UserAlreadyExistsException
):

    return JSONResponse(
        status_code=400,
        content={
            "detail": str(exc)
        }
    )
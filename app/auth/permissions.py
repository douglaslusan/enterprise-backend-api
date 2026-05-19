from fastapi import Depends, HTTPException

from app.auth.dependencies import get_current_user


def require_admin(
    current_user = Depends(get_current_user)
):

    if current_user.role != "admin":

        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    return current_user
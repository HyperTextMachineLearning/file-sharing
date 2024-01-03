# This file contains helper methods, custom exceptions, CONSTANTS

from fastapi import HTTPException, status
import re
from datetime import date
import sqlalchemy

from sqlalchemy.orm.session import Session

from . import database, models

AVAILABLE = 0
AUTO_DELETED = 1
DELETED_BY_USER = 2

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Failed to validate credential",
    headers={"WWW-Authenticate": "Bearer"},
)


username_invalid_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Invalid Username; Exclude Spaces & Special Characters except Underscore."
)

def username_is_valid(username: str):
    pattern = re.compile("^[a-z0-9_]{3,15}$")
    return True if pattern.match(username) else False


def delete_file(file: models.File, db: Session) -> models.File:
    file.availability = AUTO_DELETED
    file.file = sqlalchemy.null()
    db.commit()
    db.refresh(file)
    return file


def check_file_is_downloadable(file: models.File, db: Session):
    if file.availability == AVAILABLE:
        if file.expiry_date > date.today():
            return
        else:
            file = delete_file(file, db)
    if file.availability == AUTO_DELETED:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File deleted due to expiry"
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File deleted by owner"
        )
# This file contains helper methods, custom exceptions, CONSTANTS

from fastapi import HTTPException, status
import re
from datetime import date
import sqlalchemy
from sqlalchemy.orm.session import Session
import os

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


def delete_file(file: models.File, db: Session, delete_code: int) -> models.File:
    file.availability = delete_code
    file.file = sqlalchemy.null()
    db.commit()
    db.refresh(file)
    return file


def check_file_is_downloadable(file: models.File, db: Session):
    if file.availability == AVAILABLE:
        if file.expiry_date > date.today():
            return
        else:
            file = delete_file(file, db, AUTO_DELETED)
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


def delete_residue_file(file_path: str):
    try:
        os.remove(file_path)
    except OSError as e:
        # If it fails, inform the user.
        print(f"Error: {e.filename} - {e.strerror}.")


def create_downloadable_file(file_from_db: models.File):
    """Creates a downloadable file and returns the path to it"""
    output_file_path = os.path.join(os.getcwd(), "app", "response_files", file_from_db.file_name)
    with open(output_file_path, "wb") as output_file:
        output_file.write(file_from_db.file)
    return output_file_path


def check_file_existence(file_record: models.File):
    """Checks whether a file record exists or not. If it does not exist raises an HTTPException"""
    if file_record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
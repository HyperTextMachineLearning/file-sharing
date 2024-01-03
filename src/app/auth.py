from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, oauth2
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app import models, schemas, security
from app.database import get_db
from .utils import credentials_exception

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(
            token, security.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        username: str = payload.get("username")
        if username is None: 
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

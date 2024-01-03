from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from ..app.utils import username_is_valid, username_invalid_exception
from ..app import auth, models, schemas, security
from ..app.database import get_db

router = APIRouter(tags=["Registration & Login"])

@router.post("/register")
async def register(user_in: schemas.UserIn, db: Session = Depends(get_db)):
    if not username_is_valid(user_in.username):
        raise username_invalid_exception
    db_user = auth.get_user(db, user_in.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered.")
    hashed_password = security.get_password_hash(user_in.password)
    db_user = models.User(
        **user_in.dict(exclude={"password"}), hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "Registration successful; Proceed to Login"}

@router.post("/login", response_model=schemas.Token)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.get_user(db, username=user_credentials.username)
    password_matched: bool = security.pwd_context.verify(user_credentials.password, user.hashed_password)
    
    if not user or not password_matched:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect Username or Password"
        )
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRY_MINUTES)
    access_token = security.create_access_token(
        data={"username": user.username}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "Bearer"
    }

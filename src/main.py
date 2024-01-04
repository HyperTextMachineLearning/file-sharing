from fastapi import FastAPI

from app import models, database
from routes import authentication, operations

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

app.include_router(authentication.router)
app.include_router(operations.router)


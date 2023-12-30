from fastapi import FastAPI
from fastapi.param_functions import Body, Path
from app.schemas import AuthCredentials
app = FastAPI()

@app.post("/register")
async def register(): 
    ...


@app.post("/login")
async def login(): 
    ...


@app.post("/upload")
async def upload(): 
    ...
    # return code

    
@app.get("/download/{code}")
async def download(code: int): 
    ...


@app.delete("/delete/{code}")
async def deleteFile(code: int = Path(..., gt=1000, le=9999)): 
    ...


@app.get("/list-auto-deleted-files/")
async def listAutoDeletedFiles(): 
    ...

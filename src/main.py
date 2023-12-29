from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# -------- DELETE requests ---------

@app.delete("/delete/{code}")
async def deleteFile(code: int): ...

# -------- GET requests ---------

@app.get("/download/{code}")
async def download(code: int): ...

@app.get("/list-auto-deleted-files/")
async def listAutoDeletedFiles(): ...

# -------- POST requests ---------

@app.post("/register")
async def register(): ...

@app.post("/login")
async def login(): ...

@app.post("/upload")
async def upload(): 
    ...
    # return code
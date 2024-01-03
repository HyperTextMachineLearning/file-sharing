from typing import List
from fastapi import APIRouter, Path, Depends, Form, UploadFile, status
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm.session import Session
from datetime import date

from app import auth, models, database, utils, schemas

router = APIRouter(tags=["User Operations"])

@router.post("/upload")
async def upload(
    file: UploadFile,
    date: date = Form(gt=date.today()),
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
    ):

    file_to_upload = models.File(
        file_name=file.filename,
        expiry_date=date,
        uploader=current_user.username,
        file=file.file,
    )

    db.add(file_to_upload)
    db.commit()
    db.refresh(file_to_upload)

    return { "result": "File Uploaded Successfully", "code": file_to_upload.code}

    
@router.get("/download/{code}")
async def download(
    code: int = Path(..., gt=1000, le=9999),
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
    ): 
    file_from_db = db.query(models.File).filter(models.File.code == code).first()
    utils.check_file_is_downloadable(file_from_db, db)
    return FileResponse(file_from_db.file)


@router.delete("/delete/{code}")
async def deleteFile(
    code: int = Path(..., gt=1000, le=9999),
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
    ): 
    file_record = db.query(models.File).filter(models.File.code == code).first()
    if file_record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    if (file_record.availability == utils.AVAILABLE):
        if (current_user.username == file_record.uploader):
            file_record = utils.delete_file(file_record, db)
            return {"message": "File Deleted Successfully!"}
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Failed to delete. File can only be deleted by owner"
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="File has already been deleted"
    )
        
    
@router.get("/list-my-files", response_model=List[schemas.File])
async def listFiles(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
    ):
    files = db.query(models.File).filter(models.File.uploader == current_user.username).all()
    return files


@router.get("/list-auto-deleted-files", response_model=List[schemas.File])
async def listAutoDeletedFiles(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
    ): 
    files = db.query(models.File).filter(models.File.availability == utils.AUTO_DELETED).all()
    return files
    
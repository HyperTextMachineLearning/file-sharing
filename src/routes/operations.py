import io
from typing import List
from fastapi import APIRouter, Path, Depends, Form, UploadFile, status, BackgroundTasks
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm.session import Session
from datetime import date

from app import auth, models, database, utils, schemas

router = APIRouter(tags=["User Operations"])

@router.post("/upload")
async def upload(
    file: UploadFile,
    year: int = Form(ge=date.today().year, lt=2124),
    month: int = Form(ge=1, le=12),
    day: int = Form(ge=1, le=31),
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
    ):
    recvd_date = utils.validate_date(year, month, day)
    if recvd_date <= date.today(): return {"message": "Please provide a future date"}
    file_to_upload = models.File(
        file_name=file.filename,
        expiry_date=recvd_date,
        uploader=current_user.username,
        file=file.file.read(),
    )

    db.add(file_to_upload)
    db.commit()
    db.refresh(file_to_upload)

    return { "result": "File Uploaded Successfully", "code": file_to_upload.code}


@router.get("/download/{code}")
async def download(
    background_tasks: BackgroundTasks,
    code: int = Path(..., ),
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db),
    ): 
    file_from_db = db.query(models.File).filter(models.File.code == code).first()
    utils.check_file_existence(file_from_db)
    utils.check_file_is_downloadable(file_from_db, db)
    output_file_path = utils.create_downloadable_file(file_from_db=file_from_db)
    background_tasks.add_task(utils.delete_residue_file, output_file_path)
    return FileResponse(output_file_path, filename=file_from_db.file_name)


@router.delete("/delete/{code}")
async def deleteFile(
    code: int = Path(..., ),
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
    ): 
    file_record = db.query(models.File).filter(models.File.code == code).first()
    utils.check_file_existence(file_record)
    if (file_record.availability == utils.AVAILABLE):
        if (current_user.username == file_record.uploader):
            file_record = utils.delete_file(file_record, db, utils.DELETED_BY_USER)
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
    files = db.query(models.File).filter(models.File.availability == utils.AUTO_DELETED
                                    and models.File.uploader == current_user.username).all()
    return files
    
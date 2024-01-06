#!/home/byt3/Projects/file-sharing/venv/bin/python3
# Replace {/home/byt3/Projects} with the directory you've cloned the project in

from typing import List
import sqlalchemy
from sqlalchemy.orm import Session
from datetime import date

from app import models, database, utils

expired_files: List[models.File]
db: Session = database.get_db()

expired_files = db.query(models.File).filter(date.today() > models.File.expiry_date
                                        and models.File.availability == utils.AVAILABLE).all()

if len(expired_files) == 0: quit()

for file in expired_files:
    file.file = sqlalchemy.null()
    file.availability = utils.AUTO_DELETED

db.commit()
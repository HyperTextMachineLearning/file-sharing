from sqlalchemy import Column
from sqlalchemy import Integer, String, LargeBinary, Date, Boolean

from app.database import Base

class User(Base):
    __tablename__ = "users"

    email = Column(String, primary_key=True, index=True)
    hashed_password = Column(String)

class File(Base):
    __tablename__ = "files"

    code = Column(Integer, primary_key=True, index=True)
    file_name = Column(String)
    expiry_date = Column(Date, index=True)
    expired = Column(Boolean)
    uploader = Column()
    file = Column(LargeBinary, nullable=True)
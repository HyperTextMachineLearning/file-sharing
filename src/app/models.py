from sqlalchemy import Column, Integer, String, LargeBinary, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base

class User(Base):
    __tablename__ = "users"

    username = Column(String, primary_key=True, index=True)
    hashed_password = Column(String)
    children = relationship("File", back_populates="parent")

class File(Base):
    __tablename__ = "files"

    code = Column(Integer, primary_key=True, index=True, autoincrement=True)
    file_name = Column(String)
    expiry_date = Column(Date, index=True)
    availability = Column(Integer, default=0) # 0 - Not Expired, 1 - Auto-Expired, 2 - Deleted by User
    uploader = Column(String, ForeignKey("users.username"))
    file = Column(LargeBinary, nullable=True)
    parent = relationship("User", back_populates="children")
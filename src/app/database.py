from sqlalchemy import create_engine, orm, LargeBinary
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "postgresql://myuser:password@localhost/file_sharing"

engine = create_engine(DATABASE_URL)

SessionLocal = orm.sessionmaker(autocommit=False, autoflush=False, engine=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
from sqlalchemy import create_engine, orm, LargeBinary
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "postgres://user:pass@host/db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = orm.sessionmaker(autocommit=False, autoflush=False, engine=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
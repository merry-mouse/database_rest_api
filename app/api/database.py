from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

USER = "postgres"
PASSWORD = "password"
HOST = "localhost"
PORT = "5432"
DB_NAME = "postgres"

DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.api import crud, schemas

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


@pytest.fixture
def db():
    db_session = SessionLocal()
    yield db_session
    db_session.close()


def test_get_kitten(db):
    new_kitten = schemas.KittenCreate(
        name="Kitten",
        age=2,
        color="Orange",
        fur="short",
    )
    kitten = crud.create_kitten(db, new_kitten)
    kitten_from_db = crud.get_kitten(db, kitten.id)
    assert kitten_from_db.name == "Kitten"
    assert kitten_from_db.age == 2

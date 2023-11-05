# reusable functions to interact with the data in the database
import models
import schemas
from sqlalchemy.orm import Session


def get_kitten(db: Session, kitten_id: int):
    return db.query(models.Kitten).filter(models.Kitten.id == kitten_id).first()


def get_kittens(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Kitten).offset(skip).limit(limit).all()


def create_kitten(db: Session, kitten: schemas.KittenCreate):
    db_kitten = models.Kitten(**kitten.model_dump())
    db.add(db_kitten)
    db.commit()
    db.refresh(db_kitten)
    return db_kitten


def update_kitten(
    db: Session,
    kitten_id: int,
    kitten_data: schemas.KittenUpdate,
):
    db_kitten = db.query(models.Kitten).filter(models.Kitten.id == kitten_id).first()
    if not db_kitten:
        return None
    for key, value in kitten_data.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(db_kitten, key, value)
    db.commit()
    db.refresh(db_kitten)
    return db_kitten


def delete_kitten(db: Session, kitten_id: int):
    db_kitten = db.query(models.Kitten).filter(models.Kitten.id == kitten_id).first()
    if db_kitten:
        db.delete(db_kitten)
        db.commit()
        return True
    return False

import crud
import database
import models
import schemas
from database import engine
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/kittens/", response_model=schemas.KittenCreateUpdateResponse)
def create_kitten(kitten: schemas.KittenCreate, db: Session = Depends(database.get_db)):
    return {
        "message": "Kitten updated succesfully",
        "kitten": crud.create_kitten(db, kitten),
    }


@app.get("/kittens", response_model=list[schemas.Kitten])
def list_kittens(db: Session = Depends(database.get_db)):
    return crud.get_kittens(db)


@app.get("/kittens/{kitten_id}", response_model=schemas.Kitten)
def get_kitten_detail(kitten_id: int, db: Session = Depends(database.get_db)):
    db_kitten = crud.get_kitten(db, kitten_id)
    if db_kitten is None:
        raise HTTPException(status_code=404, detail="Kitten not found")
    return db_kitten


@app.delete("/kittens/{kitten_id}", response_model=dict)
def delete_kitten(kitten_id: int, db: Session = Depends(database.get_db)):
    if crud.delete_kitten(db, kitten_id):
        return {"message": "Kitten detailed succesfully"}
    else:
        raise HTTPException(status_code=404, detail="Kitten not found")


@app.put(
    "/kittens/{kitten_id}",
    response_model=schemas.KittenCreateUpdateResponse,
)
def update_kitten(
    kitten_id: int,
    kitten: schemas.KittenUpdate,
    db: Session = Depends(database.get_db),
):
    db_kitten = crud.update_kitten(db, kitten_id, kitten)
    if db_kitten is None:
        raise HTTPException(status_code=404, detail="Kitten not found")
    return {"message": "Kitten updated succesfully", "kitten": db_kitten}

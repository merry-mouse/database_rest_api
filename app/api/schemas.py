# Pydantic model
from typing import Optional

from pydantic import BaseModel


class KittenBase(BaseModel):
    name: str
    age: int
    color: str
    fur: str


class KittenCreate(KittenBase):
    # schema for creating kitten record
    pass


class KittenUpdate(BaseModel):
    # schema for updating existing kitten record
    name: Optional[str] = None
    age: Optional[int] = None
    color: Optional[str] = None
    fur: Optional[str] = None


class KittenInDB(KittenBase):
    # representing a kitten in a record from the database
    id: int


class Kitten(KittenInDB):
    # representing a kitten record from the db
    pass


class KittenCreateUpdateResponse(BaseModel):
    # response model for put request
    message: str
    kitten: Kitten

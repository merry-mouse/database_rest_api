# db model
from database import Base
from sqlalchemy import Column, Integer, String


class Kitten(Base):
    __tablename__ = "kittens"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    color = Column(String)
    fur = Column(String)

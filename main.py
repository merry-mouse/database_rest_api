from databases import Database
from fastapi import FastAPI
from sqlalchemy import Column, Integer, MetaData, String, Table, create_engine, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:password@localhost:5432/postgres"

metadata = MetaData()

kittens_table = Table(
    "kittens",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("name", String),
    Column("age", Integer),
    Column("color", String),
    Column("fur", String),
)

engine = create_engine(DATABASE_URL)
metadata.create_all(bind=engine)

database = Database(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.post("/kittens/")
async def create_kitten(kitten: dict):
    query = insert(kittens_table).values(**kitten)
    last_record_id = await database.execute(query)
    return {"id": last_record_id, **kitten}


@app.get("/kittens/")
async def list_kittens():
    query = kittens_table.select()
    results = await database.fetch_all(query)
    return results


@app.get("/kittens/{kitten_id}")
async def get_kitten_detail(kitten_id: int):
    query = select([kittens_table]).where(kittens_table.c.id == kitten_id)
    result = await database.fetch_one(query)
    if result:
        return result
    else:
        return {"error": "Kitten not found!"}

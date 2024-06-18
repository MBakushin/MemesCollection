from fastapi import FastAPI

from core.config import settings
from core.database import engine, Base
from api import router as api_router


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(api_router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Meme API!"}

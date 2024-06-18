from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from uuid import uuid4

import schemas
import crud
from core.database import get_db
from core.s3 import upload_file_to_s3
from core.config import settings


router = APIRouter()


@router.get("/", response_model=List[schemas.MemeInDB])
def read_memes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    memes = crud.get_memes(db, skip=skip, limit=limit)
    return memes


@router.get("/{meme_id}", response_model=schemas.MemeInDB)
def read_meme(meme_id: int, db: Session = Depends(get_db)):
    db_meme = crud.get_meme(db, meme_id=meme_id)
    if db_meme is None:
        raise HTTPException(status_code=404, detail="Meme not found")
    return db_meme


@router.post("/", response_model=schemas.MemeInDB)
def create_meme(
        meme: schemas.MemeCreate,
        file: UploadFile = File(...),
        db: Session = Depends(get_db)
):
    file_extension = file.filename.split(".")[-1]
    object_name = f"{uuid4()}.{file_extension}"
    image_url = upload_file_to_s3(file.file, settings.S3_BUCKET_NAME,
                                  object_name)

    if image_url is None:
        raise HTTPException(status_code=500, detail="Failed to upload file")

    return crud.create_meme(db=db, meme=meme, image_url=image_url)


@router.put("/{meme_id}", response_model=schemas.MemeInDB)
def update_meme(
        meme_id: int,
        meme: schemas.MemeUpdate,
        db: Session = Depends(get_db)
):
    db_meme = crud.get_meme(db, meme_id=meme_id)
    if db_meme is None:
        raise HTTPException(status_code=404, detail="Meme not found")
    return crud.update_meme(db=db, meme_id=meme_id, meme=meme)


@router.delete("/{meme_id}", response_model=schemas.MemeInDB)
def delete_meme(meme_id: int, db: Session = Depends(get_db)):
    db_meme = crud.get_meme(db, meme_id=meme_id)
    if db_meme is None:
        raise HTTPException(status_code=404, detail="Meme not found")
    return crud.delete_meme(db=db, meme_id=meme_id)

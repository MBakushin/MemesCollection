from sqlalchemy.orm import Session
from .models import Meme
from .schemas import meme as schemas

def get_meme(db: Session, meme_id: int):
    return db.query(Meme).filter(Meme.id == meme_id).first()

def get_memes(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Meme).offset(skip).limit(limit).all()

def create_meme(db: Session, meme: schemas.MemeCreate, image_url: str):
    db_meme = Meme(title=meme.title, description=meme.description, image_url=image_url)
    db.add(db_meme)
    db.commit()
    db.refresh(db_meme)
    return db_meme

def update_meme(db: Session, meme_id: int, meme: schemas.MemeUpdate):
    db_meme = db.query(Meme).filter(Meme.id == meme_id).first()
    db_meme.title = meme.title
    db_meme.description = meme.description
    db.commit()
    db.refresh(db_meme)
    return db_meme

def delete_meme(db: Session, meme_id: int):
    db_meme = db.query(Meme).filter(Meme.id == meme_id).first()
    db.delete(db_meme)
    db.commit()
    return db_meme

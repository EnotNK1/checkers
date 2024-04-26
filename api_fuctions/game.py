from sqlalchemy.orm import Session
from database.functional import s
from fastapi import HTTPException
from fastapi import Depends


def get_db():
    db = s()
    try:
        yield db
    finally:
        db.close()


def create_game_func(db: Session = Depends(get_db)):
    pass


def get_game_func(db: Session = Depends(get_db)):
    pass


def make_move_func(db: Session = Depends(get_db)):
    pass

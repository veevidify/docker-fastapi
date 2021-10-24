from fastapi import FastAPI, Depends, HTTPException, status

from sqlalchemy.orm import Session
from typing import List

from . import repo, models, schemas
from .db import SessionLocal, db_engine

models.Base.metadata.create_all(bind=db_engine)

app = FastAPI()

# route controller depends on db capabilities
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db_session: Session = Depends(get_db_session)):
    exist_user = repo.get_user_by_email(db_session, user.email)
    if (exist_user):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Email exist"
        )

    return repo.create_user(db=db_session, user=user)

@app.get("/users/", response_model=List[schemas.User])
def read_users(offset: int = 0, limit: int = 100, db_session: Session = Depends(get_db_session)):
    users = repo.get_users(db=db_session)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_single_user(user_id: int, db_session: Session = Depends(get_db_session)):
    db_user = repo.get_user(db=db_session, user_id=user_id)
    if (db_user is None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    return db_user

@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(user_id: int, item: schemas.ItemCreate, db_session: Session = Depends(get_db_session)):
    return repo.create_user_item(db=db_session, item=item, user_id=user_id)

@app.get("/items/", response_model=List[schemas.Item])
def read_items(offset: int = 0, limit: int = 100, db_session: Session = Depends(get_db_session)):
    items = repo.get_items(db, offset=offset, limit=limit)
    return items

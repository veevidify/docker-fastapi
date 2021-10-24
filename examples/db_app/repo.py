from sqlalchemy.orm import Session

from . import models, schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, user_email: str):
    return db.query(models.User).filter(models.User.email == user_email).first()

def get_users(db: Session, offset: int = 0, limit: int = 100):
    return db.query(models.User).offset(offset).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    mock_hashed_pw =  "hashed" + user.password
    db_user = models.User(
        email=user.email,
        hashed_password=mock_hashed_pw
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def get_items(db: Session, offset: int = 0, limit: int = 100):
    return db.query(models.Item).offset(offset).limit(limit).all()

def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(
        **item.dict(),
        owner_id=user_id
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item

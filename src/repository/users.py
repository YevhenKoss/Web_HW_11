from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel


async def get_users(db: Session):
    users = db.query(User).all()
    return users


async def get_user_by_id(user_id: int, db: Session):
    user = db.query(User).filter_by(id=user_id).first()
    return user


async def get_user_by_name(first_name, last_name, db: Session):
    user = db.query(User).filter_by(first_name=first_name, last_name=last_name).first()
    return user


async def create(body: UserModel, db: Session):
    user = User(**body.dict())
    db.add(user)
    db.commit()
    return user


async def update(user_id: int, body: UserModel, db: Session):
    user = await get_user_by_id(user_id, db)
    if user:
        user.first_name = body.first_name
        user.last_name = body.last_name
        db.commit()
    return user


async def remove(user_id: int, db: Session):
    user = await get_user_by_id(user_id, db)
    if user:
        db.delete(user)
        db.commit()
    return user


async def get_user_by_first_name(first_name, db: Session):
    user = db.query(User).filter_by(first_name=first_name).all()
    return user


async def get_user_by_last_name(last_name, db: Session):
    user = db.query(User).filter_by(last_name=last_name).all()
    return user

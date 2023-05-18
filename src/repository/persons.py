from sqlalchemy.orm import Session

from src.database.models import Person, User
from src.schemas import PersonModel


async def get_persons(db: Session, user: User):
    persons = db.query(Person).filter_by(user_id=user.id).all()
    return persons


async def get_person_by_id(person_id: int, db: Session, user: User):
    person = db.query(Person).filter_by(id=person_id, user_id=user.id).first()
    return person


async def get_person_by_name(first_name, last_name, db: Session, user: User):
    person = db.query(Person).filter_by(first_name=first_name, last_name=last_name, user_id=user.id).first()
    return person


async def create(body: PersonModel, db: Session, user: User):
    person = Person(**body.dict(), user_id=user.id)
    db.add(person)
    db.commit()
    return person


async def update(person_id: int, body: PersonModel, db: Session, user: User):
    person = await get_person_by_id(person_id, db, user.id)
    if person:
        person.first_name = body.first_name
        person.last_name = body.last_name
        db.commit()
    return person


async def remove(person_id: int, db: Session, user: User):
    person = await get_person_by_id(person_id, db, user.id)
    if person:
        db.delete(person)
        db.commit()
    return person


async def get_person_by_first_name(first_name, db: Session, user: User):
    person = db.query(Person).filter_by(first_name=first_name, user_id=user.id).all()
    return person


async def get_person_by_last_name(last_name, db: Session, user: User):
    person = db.query(Person).filter_by(last_name=last_name, user_id=user.id).all()
    return person

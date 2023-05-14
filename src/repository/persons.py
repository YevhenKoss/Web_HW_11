from sqlalchemy.orm import Session

from src.database.models import Person
from src.schemas import PersonModel


async def get_persons(db: Session):
    persons = db.query(Person).all()
    return persons


async def get_person_by_id(person_id: int, db: Session):
    person = db.query(Person).filter_by(id=person_id).first()
    return person


async def get_person_by_name(first_name, last_name, db: Session):
    person = db.query(Person).filter_by(first_name=first_name, last_name=last_name).first()
    return person


async def create(body: PersonModel, db: Session):
    person = Person(**body.dict())
    db.add(person)
    db.commit()
    return person


async def update(person_id: int, body: PersonModel, db: Session):
    person = await get_person_by_id(person_id, db)
    if person:
        person.first_name = body.first_name
        person.last_name = body.last_name
        db.commit()
    return person


async def remove(person_id: int, db: Session):
    person = await get_person_by_id(person_id, db)
    if person:
        db.delete(person)
        db.commit()
    return person


async def get_person_by_first_name(first_name, db: Session):
    person = db.query(Person).filter_by(first_name=first_name).all()
    return person


async def get_person_by_last_name(last_name, db: Session):
    person = db.query(Person).filter_by(last_name=last_name).all()
    return person

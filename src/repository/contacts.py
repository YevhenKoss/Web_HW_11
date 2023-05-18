from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from src.database.models import Person, Contact, User
from src.repository.persons import get_person_by_first_name, get_person_by_last_name
from src.schemas import ContactModel, ContactBlackList


async def get_contacts(user: User, limit: int, offset: int, db: Session):
    contacts = db.query(Contact).filter_by(user_id=user.id).limit(limit).offset(offset).all()
    return contacts


async def get_contact_by_id(user: User, contact_id: int, db: Session):
    contact = db.query(Contact).filter_by(user_id=user.id, id=contact_id).first()
    return contact


async def get_contact_by_email(user: User, email, db: Session):
    contact = db.query(Contact).filter_by(user_id=user.id, email=email).first()
    return contact


async def get_contact_by_phone(user: User, phone, db: Session):
    contact = db.query(Contact).filter_by(user_id=user.id, phone=phone).first()
    return contact


async def create(user: User, body: ContactModel, db: Session):
    contact = Contact(**body.dict(), user_id=user.id)
    db.add(contact)
    db.commit()
    return contact


async def update(user: User, contact_id: int, body: ContactModel, db: Session):
    contact = await get_contact_by_id(user, contact_id, db)
    if contact:
        contact.date_of_birth = body.date_of_birth
        contact.email = body.email
        contact.phone = body.phone
        contact.note = body.note
        contact.blocked = body.blocked
        contact.person_id = body.person_id
        db.commit()
    return contact


async def remove(user: User, contact_id: int, db: Session):
    contact = await get_contact_by_id(user.id, contact_id, db)
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def block(user: User, contact_id: int, body: ContactBlackList, db: Session):
    contact = await get_contact_by_id(user.id, contact_id, db)
    if contact:
        contact.blocked = body.blocked
        db.commit()
    return contact


async def get_contact_by_person(user: User, person: Person, db: Session):
    contact = db.query(Contact).filter_by(user_id=user.id, person=person).all()
    return contact


async def get_contacts_by_email(user: User, email, db: Session):
    contact = db.query(Contact).filter_by(user_id=user.id, email=email).all()
    return contact


async def search_contacts(user: User, data: str, db: Session):
    persons_fn = await get_person_by_first_name(user.id, data, db)
    persons_ln = await get_person_by_last_name(user.id, data, db)
    print(persons_fn, persons_ln)
    persons = persons_fn + persons_ln
    if persons:
        contacts = []
        for person in persons:
            contact = await get_contact_by_person(user.id, person, db)
            contacts.append(contact[0])
    else:
        contacts = await get_contacts_by_email(user.id, data, db)
    if contacts:
        print(contacts)
        return contacts


async def get_contacts_hb_id_list(user: User, db: Session):
    end_day = datetime.now() + timedelta(days=7)
    current_day = datetime.now().date()
    current_year = datetime.now().strftime("%Y")
    end_day = end_day.date()
    contacts = db.query(Contact).filter_by(user_id=user.id).all()
    contacts_id_list = []
    for contact in contacts:
        contact_bd_str = contact.date_of_birth.strftime("%Y-%m-%d")
        contact_bd_new = contact_bd_str.replace(contact.date_of_birth.strftime("%Y"), current_year)
        contact_bd_new_dt = datetime.strptime(contact_bd_new, '%Y-%m-%d').date()
        if current_day <= contact_bd_new_dt <= end_day:
            contacts_id_list.append(contact.id)
    return contacts_id_list


async def get_contacts_hb(user: User, contacts_id_list, limit, offset, db: Session):
    contacts = []
    for contact_id in contacts_id_list:
        contact = db.query(Contact).filter_by(user_id=user.id, id=contact_id).limit(limit).offset(offset).all()
        contacts.append(contact[0])
    return contacts

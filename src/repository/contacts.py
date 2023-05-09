from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from src.database.models import User, Contact
from src.repository.users import get_user_by_first_name, get_user_by_last_name
from src.schemas import ContactModel, ContactBlackList


async def get_contacts(limit: int, offset: int, db: Session):
    contacts = db.query(Contact).limit(limit).offset(offset).all()
    return contacts


async def get_contact_by_id(contact_id: int, db: Session):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    return contact


async def get_contact_by_email(email, db: Session):
    contact = db.query(Contact).filter_by(email=email).first()
    return contact


async def get_contact_by_phone(phone, db: Session):
    contact = db.query(Contact).filter_by(phone=phone).first()
    return contact


async def create(body: ContactModel, db: Session):
    contact = Contact(**body.dict())
    db.add(contact)
    db.commit()
    return contact


async def update(contact_id: int, body: ContactModel, db: Session):
    contact = await get_contact_by_id(contact_id, db)
    if contact:
        contact.date_of_birth = body.date_of_birth
        contact.email = body.email
        contact.phone = body.phone
        contact.note = body.note
        contact.blocked = body.blocked
        contact.user_id = body.user_id
        db.commit()
    return contact


async def remove(contact_id: int, db: Session):
    contact = await get_contact_by_id(contact_id, db)
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def block(contact_id: int, body: ContactBlackList, db: Session):
    contact = await get_contact_by_id(contact_id, db)
    if contact:
        contact.blocked = body.blocked
        db.commit()
    return contact


async def get_contact_by_user(user: User, db: Session):
    contact = db.query(Contact).filter_by(user=user).all()
    return contact


async def get_contacts_by_email(email, db: Session):
    contact = db.query(Contact).filter_by(email=email).all()
    return contact


async def search_contacts(data: str, db: Session):
    users_fn = await get_user_by_first_name(data, db)
    users_ln = await get_user_by_last_name(data, db)
    print(users_fn, users_ln)
    users = users_fn + users_ln
    if users:
        contacts = []
        for user in users:
            contact = await get_contact_by_user(user, db)
            contacts.append(contact[0])
    else:
        contacts = await get_contacts_by_email(data, db)
    if contacts:
        print(contacts)
        return contacts


async def get_contacts_hb_id_list(db: Session):
    end_day = datetime.now() + timedelta(days=7)
    current_day = datetime.now().date()
    current_year = datetime.now().strftime("%Y")
    end_day = end_day.date()
    contacts = db.query(Contact).all()
    contacts_id_list = []
    for contact in contacts:
        contact_bd_str = contact.date_of_birth.strftime("%Y-%m-%d")
        contact_bd_new = contact_bd_str.replace(contact.date_of_birth.strftime("%Y"), current_year)
        contact_bd_new_dt = datetime.strptime(contact_bd_new, '%Y-%m-%d').date()
        if current_day <= contact_bd_new_dt <= end_day:
            contacts_id_list.append(contact.id)
    return contacts_id_list


async def get_contacts_hb(contacts_id_list, limit, offset, db: Session):
    contacts = []
    for contact_id in contacts_id_list:
        contact = db.query(Contact).filter_by(id=contact_id).limit(limit).offset(offset).all()
        contacts.append(contact[0])
    return contacts

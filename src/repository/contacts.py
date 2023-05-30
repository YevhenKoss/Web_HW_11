from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from src.database.models import Person, Contact, User
from src.repository.persons import get_person_by_first_name, get_person_by_last_name
from src.schemas import ContactModel, ContactBlackList


async def get_contacts(user: User, limit: int, offset: int, db: Session):
    """
    The get_contacts function returns a list of contacts for the user.

    :param user: User: Check if the user is logged in
    :param limit: int: Limit the number of contacts returned
    :param offset: int: Specify the number of records to skip before starting to return rows
    :param db: Session: Pass the database session to the function
    :return: All contacts for a given user
    """
    contacts = db.query(Contact).filter_by(user_id=user.id).limit(limit).offset(offset).all()
    return contacts


async def get_contact_by_id(user: User, contact_id: int, db: Session):
    """
    The get_contact_by_id function returns a contact from the database by its id.

    :param user: User: Check if the user is logged in
    :param contact_id: int: Filter the query by contact_id
    :param db: Session: Pass the database session to the function
    :return: A contact object
    """
    contact = db.query(Contact).filter_by(user_id=user.id, id=contact_id).first()
    return contact


async def get_contact_by_email(user: User, email, db: Session):
    """
    The get_contact_by_email function takes in a user and an email address,
    and returns the contact associated with that email address.


    :param user: User: Check if the user is logged in
    :param email: Filter the contacts by email
    :param db: Session: Pass in the database session to the function
    :return: A contact object
    """
    contact = db.query(Contact).filter_by(user_id=user.id, email=email).first()
    return contact


async def get_contact_by_phone(user: User, phone, db: Session):
    """
    The get_contact_by_phone function returns a contact object from the database based on the user's id and phone number.

    :param user: Check if the user is logged in
    :param phone: Filter the contact by phone number
    :param db: Session: Pass the database session to the function
    :return: A contact object if the user_id and phone number match a record in the database
    """
    contact = db.query(Contact).filter_by(user_id=user.id, phone=phone).first()
    return contact


async def create(user: User, body: ContactModel, db: Session):
    """
    The create function creates a new contact in the database.

    :param user: User: Check if the user is logged in
    :param body: ContactModel: Create a new contact object
    :param db: Session: Pass the database session to the function
    :return: A contact object
    """
    contact = Contact(**body.dict(), user_id=user.id)
    db.add(contact)
    db.commit()
    return contact


async def update(user: User, contact_id: int, body: ContactModel, db: Session):
    """
    The update function updates a contact in the database.

    :param user: User: Check if the user is logged in
    :param contact_id: int: Specify which contact to update
    :param body: ContactModel: Get the new values for the contact
    :param db: Session: Access the database
    :return: The updated contact
    """
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
    """
    The remove function removes a contact from the database.

    :param user: User: Check if the user is logged in
    :param contact_id: int: Specify the contact to be removed
    :param db: Session: Pass the database session to the function
    :return: The contact that was deleted
    """
    contact = await get_contact_by_id(user.id, contact_id, db)
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def block(user: User, contact_id: int, body: ContactBlackList, db: Session):
    """
    The block function is used to block a contact.

    :param user: User: Check if the user is logged in
    :param contact_id: int: Get the contact id from the url
    :param body: ContactBlackList: Pass the json object to the block function
    :param db: Session: Access the database
    :return: The updated contact
    """
    contact = await get_contact_by_id(user.id, contact_id, db)
    if contact:
        contact.blocked = body.blocked
        db.commit()
    return contact


async def get_contact_by_person(user: User, person: Person, db: Session):
    """
    The get_contact_by_person function returns a list of contacts for the given user and person.

    :param user: User: Check if the user is logged in
    :param person: Person: Filter the contact list by person
    :param db: Session: Pass the database session to the function
    :return: A list of all contacts that match the person
    """
    contact = db.query(Contact).filter_by(user_id=user.id, person=person).all()
    return contact


async def get_contacts_by_email(user: User, email, db: Session):
    """
    The get_contacts_by_email function returns a list of contacts that match the email provided.

    :param user: User: Check if the user is logged in
    :param email: Filter the contacts by email
    :param db: Session: Pass the database session to the function
    :return: A list of all contacts that match the email address
    """
    contact = db.query(Contact).filter_by(user_id=user.id, email=email).all()
    return contact


async def search_contacts(user: User, data: str, db: Session):
    """
    The search_contacts function searches for contacts by first name, last name, or email.

    :param user: User: Check if the user is logged in
    :param data: str: Pass in the search query
    :param db: Session: Pass the database session to the function
    :return: A list of contacts that match the search criteria
    """
    persons_fn = await get_person_by_first_name(user.id, data, db)
    persons_ln = await get_person_by_last_name(user.id, data, db)
    persons = persons_fn + persons_ln
    if persons:
        contacts = []
        for person in persons:
            contact = await get_contact_by_person(user.id, person, db)
            contacts.append(contact[0])
    else:
        contacts = await get_contacts_by_email(user.id, data, db)
    if contacts:
        return contacts


async def get_contacts_hb_id_list(user: User, db: Session):
    """
    The get_contacts_hb_id_list function returns a list of contact IDs for contacts whose
    birthday is within the next 7 days.

    :param user: User: Check if the user is logged in
    :param db: Session: Pass the database session to the function
    :return: A list of contacts' ids,
    """
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
    """
    The get_contacts_hb function returns a list of contacts whose birthday is within the next 7 days.

    :param user: User: Check if the user is logged in
    :param contacts_id_list: Get the contacts with the ids in that list
    :param limit: Limit the number of contacts returned
    :param offset: Skip the first n results
    :param db: Session: Pass the database session to the function
    :return: A list of contacts
    """
    contacts = []
    for contact_id in contacts_id_list:
        contact = db.query(Contact).filter_by(user_id=user.id, id=contact_id).limit(limit).offset(offset).all()
        contacts.append(contact[0])
    return contacts

from sqlalchemy.orm import Session

from src.database.models import Person, User
from src.schemas import PersonModel


async def get_persons(db: Session, user: User):
    """
    The get_persons function returns a list of all persons in the database.

    :param db: Session: Pass the database session to the function
    :param user: User: Check if the user is logged in
    :return: A list of person objects
    """
    persons = db.query(Person).filter_by(user_id=user.id).all()
    return persons


async def get_person_by_id(person_id: int, db: Session, user: User):
    """
    The get_person_by_id function returns a person object from the database.

    :param person_id: int: Specify the id of the person to be retrieved
    :param db: Session: Access the database
    :param user: User: Check if the user is logged in
    :return: The person object with the given id and user
    """
    person = db.query(Person).filter_by(id=person_id, user_id=user.id).first()
    return person


async def get_person_by_name(first_name, last_name, db: Session, user: User):
    """
    The get_person_by_name function returns a person object from the database by a first name and last name.

    :param first_name: Filter the query to find a person with that first name
    :param last_name: Filter the results of the query by last name
    :param db: Session: Pass in the database session to the function
    :param user: User: Check if the user is logged in
    :return: A person object with the given first name and last name
    """
    person = db.query(Person).filter_by(first_name=first_name, last_name=last_name, user_id=user.id).first()
    return person


async def create(body: PersonModel, db: Session, user: User):
    """
    The create function creates a new person in the database.
        It takes in a body of type PersonModel, which is validated by Pydantic.
        The function also takes in a db Session and user object from FastAPI's dependency injection system.

    :param body: PersonModel: Get the data from the request body
    :param db: Session: Access the database
    :param user: User: Check if the user is logged in
    :return: The newly created person object
    """
    person = Person(**body.dict(), user_id=user.id)
    db.add(person)
    db.commit()
    return person


async def update(person_id: int, body: PersonModel, db: Session, user: User):
    """
    The update function updates a person in the database.

    :param person_id: int: Specify the id of the person to update
    :param body: PersonModel: Get the data from the request body
    :param db: Session: Access the database
    :param user: User: Check if the user is logged in
    :return: An updated person object
    """
    person = await get_person_by_id(person_id, db, user.id)
    if person:
        person.first_name = body.first_name
        person.last_name = body.last_name
        db.commit()
    return person


async def remove(person_id: int, db: Session, user: User):
    """
    The remove function removes a person from the database.

    :param person_id: int: Specify the id of the person to be removed
    :param db: Session: Access the database
    :param user: User: Check if the user is logged in
    :return: The person object that was deleted
    """
    person = await get_person_by_id(person_id, db, user.id)
    if person:
        db.delete(person)
        db.commit()
    return person


async def get_person_by_first_name(first_name, db: Session, user: User):
    """
    The get_person_by_first_name function returns a person by first name

    :param first_name: Filter the results of the query
    :param db: Session: Access the database
    :param user: User: Check if the user is logged in
    :return: A list of all the persons with a given first name
    """
    person = db.query(Person).filter_by(first_name=first_name, user_id=user.id).all()
    return person


async def get_person_by_last_name(last_name, db: Session, user: User):
    """
    The get_person_by_last_name function returns a person by last name

    :param last_name: Filter the results by last name
    :param db: Session: Pass the database session to the function
    :param user: User: Check if the user is logged in
    :return: A list of all the persons with a given last name
    """
    person = db.query(Person).filter_by(last_name=last_name, user_id=user.id).all()
    return person

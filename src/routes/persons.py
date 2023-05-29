from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.repository import persons as repository_persons
from src.schemas import PersonModel, PersonResponse
from src.services.auth import auth_service

router = APIRouter(prefix="/persons", tags=["persons"])


@router.get("/", response_model=List[PersonResponse])
async def get_persons(db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_persons function returns a list of persons.

    :param db: Session: Get the database session
    :param current_user: User: Get the current user from the database
    :return: A list of person objects
    """
    persons = await repository_persons.get_persons(db, current_user)
    return persons


@router.get("/{person_id}", response_model=PersonResponse)
async def get_person(person_id: int = Path(ge=1), db: Session = Depends(get_db),
                     current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_person function returns a person by id.
        If the person does not exist, it raises an HTTP 404 error.


    :param person_id: int: Specify the path parameter
    :param db: Session: Get the database session
    :param current_user: User: Get the current user from the database
    :return: A person by id
    """
    person = await repository_persons.get_person_by_id(person_id, db, current_user)
    if person is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return person


@router.post("/", response_model=PersonResponse, status_code=status.HTTP_201_CREATED)
async def create_person(body: PersonModel, db: Session = Depends(get_db),
                        current_user: User = Depends(auth_service.get_current_user)):
    """
    The create_person function creates a new person in the database.

    :param body: PersonModel: Get the data from the request body
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user
    :return: A person object
    """
    person = await repository_persons.get_person_by_name(body.first_name, body.last_name, db, current_user)
    if person:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User is exists")
    person = await repository_persons.create(body, db, current_user)
    return person


@router.put("/{person_id}", response_model=PersonResponse)
async def update_person(body: PersonModel, person_id: int = Path(ge=1), db: Session = Depends(get_db),
                        current_user: User = Depends(auth_service.get_current_user)):
    """
    The update_person function updates a person in the database.
        The function takes an id and a body as input, and returns the updated person.
        If no person is found with that id, it raises an HTTPException.

    :param body: PersonModel: Specify the type of data that will be passed to the function
    :param person_id: int: Get the person id from the url
    :param db: Session: Get the database session
    :param current_user: User: Get the current user from the database
    :return: The updated person
    """
    person = await repository_persons.update(person_id, body, db, current_user)
    if person is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return person


@router.delete("/{person_id}", response_model=PersonResponse)
async def delete_person(person_id: int = Path(ge=1), db: Session = Depends(get_db),
                        current_user: User = Depends(auth_service.get_current_user)):
    """
    The delete_person function deletes a person from the database.
        The function takes in an integer ID of the person to be deleted, and returns a dictionary containing information about that person.
        If no such user exists, it raises an HTTPException with status code 404.

    :param person_id: int: Get the person id from the path
    :param db: Session: Get a database session
    :param current_user: User: Get the current user information
    :return: A person object
    """
    person = await repository_persons.remove(person_id, db, current_user)
    if person is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return person

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, status, Query
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.repository import contacts as repository_contacts
from src.schemas import ContactModel, ContactResponse, ContactBlackList
from src.services.auth import auth_service

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("/", response_model=List[ContactResponse], dependencies=[Depends(RateLimiter(times=2, seconds=5))],
            description="Two requests per five seconds")
async def get_contacts(current_user: User = Depends(auth_service.get_current_user), limit: int = Query(10, le=300),
                       offset: int = 0, db: Session = Depends(get_db)):
    """
    The get_contacts function returns a list of contacts for the current user.
    The function takes in an optional limit and offset query parameters to paginate through the results.


    :param current_user: User: Get the current user
    :param limit: int: Limit the number of contacts returned
    :param le: Limit the maximum number of contacts that can be returned
    :param offset: int: Specify the number of records to skip before starting to return rows
    :param db: Session: Get the database session
    :return: A list of contacts
    """
    contacts = await repository_contacts.get_contacts(current_user, limit, offset, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse, dependencies=[Depends(RateLimiter(times=2, seconds=5))],
            description="Two requests per five seconds")
async def get_contact(current_user: User = Depends(auth_service.get_current_user), contact_id: int = Path(ge=1),
                      db: Session = Depends(get_db)):
    """
    The get_contact function is used to retrieve a single contact from the database.
    It takes in an id of the contact and returns a Contact object.

    :param current_user: User: Get the current user from the database
    :param contact_id: int: Get the contact id from the path
    :param db: Session: Get the database session
    :return: A contact object
    """
    contact = await repository_contacts.get_contact_by_id(current_user, contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(RateLimiter(times=1, seconds=10))],
            description="One request per ten seconds")
async def create_contact(body: ContactModel, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The create_contact function creates a new contact in the database.

    :param body: ContactModel: Get the data from the request body
    :param db: Session: Pass the database session to the repository layer
    :param current_user: User: Get the current user from the database
    :return: A contact object
    """
    contact_email = await repository_contacts.get_contact_by_email(current_user, body.email, db)
    contact_phone = await repository_contacts.get_contact_by_email(current_user, body.phone, db)
    if contact_email or contact_phone:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Contact is exists")
    contact = await repository_contacts.create(current_user, body, db)
    return contact


@router.put("/{contact_id}", response_model=ContactResponse, dependencies=[Depends(RateLimiter(times=1, seconds=10))],
            description="One request per ten seconds")
async def update_contact(body: ContactModel, contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The update_contact function updates a contact in the database.
        The function takes an id and a body as input, which is then used to update the contact.
        If no such contact exists, it returns 404 Not Found.

    :param body: ContactModel: Validate the request body
    :param contact_id: int: Get the contact id from the url
    :param db: Session: Pass the database session to the repository
    :param current_user: User: Get the current user from the database
    :return: The updated contact object
    """
    contact = await repository_contacts.update(current_user, contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(RateLimiter(times=1, seconds=10))],
            description="One request per ten seconds")
async def delete_contact(current_user: User = Depends(auth_service.get_current_user), contact_id: int = Path(ge=1),
                         db: Session = Depends(get_db)):
    """
    The delete_contact function deletes a contact from the database.

    :param current_user: User: Get the current user
    :param contact_id: int: Get the contact id from the path
    :param db: Session: Get the database session
    :return: None
    """
    contact = await repository_contacts.remove(current_user, contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return None


@router.patch("/{contact_id}/blacklist", response_model=ContactResponse, dependencies=[Depends(RateLimiter(times=1, seconds=10))],
            description="One request per ten seconds")
async def block_contact(body: ContactBlackList, contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                        current_user: User = Depends(auth_service.get_current_user)):
    """
    The block_contact function is used to block a contact.

    :param body: ContactBlackList: Get the data from the request body
    :param contact_id: int: Get the contact id from the url
    :param db: Session: Access the database
    :param current_user: User: Get the user from the database
    :return: A contact object
    """
    contact = await repository_contacts.block(current_user, contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contact


@router.get("/search/", response_model=List[ContactResponse], dependencies=[Depends(RateLimiter(times=1, seconds=5))],
            description="One request per five seconds")
async def search_contact(current_user: User = Depends(auth_service.get_current_user),
                         find: str = Query(min_length=2, max_length=50), db: Session = Depends(get_db)):
    """
    The search_contact function searches for contacts in the database.
        It takes a string as an argument and returns a list of contacts that match the search criteria.

    :param current_user: User: Get the current user
    :param find: str: Search for a contact
    :param max_length: Limit the length of the input string
    :param db: Session: Get the database session
    :return: A list of contacts that match the search criteria
    """
    contacts = await repository_contacts.search_contacts(current_user, find, db)
    if contacts:
        return contacts
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")


@router.get("/birthday/", response_model=List[ContactResponse], dependencies=[Depends(RateLimiter(times=1, seconds=5))],
            description="One request per five seconds")
async def get_birthdays(current_user: User = Depends(auth_service.get_current_user), limit: int = Query(10, le=300),
                        offset: int = 0, db: Session = Depends(get_db)):
    """
    The get_birthdays function returns a list of contacts with birthdays in the next 7 days.
    The function takes an optional limit and offset parameter to control pagination.


    :param current_user: User: Get the current user from the database
    :param limit: int: Limit the number of contacts returned
    :param le: Limit the number of contacts returned
    :param offset: int: Skip the first n contacts in the database
    :param db: Session: Get the database session
    :return: A list of contacts with birthdays in the next 7 days
    """
    contacts_id_list = await repository_contacts.get_contacts_hb_id_list(current_user, db)
    contacts = await repository_contacts.get_contacts_hb(current_user, contacts_id_list, limit, offset, db)
    if contacts:
        return contacts
    else:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No content")

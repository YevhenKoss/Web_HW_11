from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, status, Query
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.repository import contacts as repository_contacts
from src.schemas import ContactModel, ContactResponse, ContactBlackList
from src.services.auth import auth_service

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("/", response_model=List[ContactResponse])
async def get_contacts(current_user: User = Depends(auth_service.get_current_user), limit: int = Query(10, le=300),
                       offset: int = 0, db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contacts(current_user, limit, offset, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(current_user: User = Depends(auth_service.get_current_user), contact_id: int = Path(ge=1),
                      db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact_by_id(current_user, contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactModel, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    contact_email = await repository_contacts.get_contact_by_email(current_user, body.email, db)
    contact_phone = await repository_contacts.get_contact_by_email(current_user, body.phone, db)
    if contact_email or contact_phone:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Contact is exists")
    contact = await repository_contacts.create(current_user, body, db)
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactModel, contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.update(current_user, contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(current_user: User = Depends(auth_service.get_current_user), contact_id: int = Path(ge=1),
                         db: Session = Depends(get_db)):
    contact = await repository_contacts.remove(current_user, contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return None


@router.patch("/{contact_id}/blacklist", response_model=ContactResponse)
async def block_contact(body: ContactBlackList, contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                        current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.block(current_user, contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contact


@router.get("/search/", response_model=List[ContactResponse])
async def search_contact(current_user: User = Depends(auth_service.get_current_user),
                         find: str = Query(min_length=2, max_length=50), db: Session = Depends(get_db)):
    contacts = await repository_contacts.search_contacts(current_user, find, db)
    if contacts:
        return contacts
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")


@router.get("/birthday/", response_model=List[ContactResponse])
async def get_birthdays(current_user: User = Depends(auth_service.get_current_user), limit: int = Query(10, le=300),
                        offset: int = 0, db: Session = Depends(get_db)):
    contacts_id_list = await repository_contacts.get_contacts_hb_id_list(current_user, db)
    contacts = await repository_contacts.get_contacts_hb(current_user, contacts_id_list, limit, offset, db)
    if contacts:
        return contacts
    else:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No content")

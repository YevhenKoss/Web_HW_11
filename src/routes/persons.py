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
    persons = await repository_persons.get_persons(db, current_user)
    return persons


@router.get("/{person_id}", response_model=PersonResponse)
async def get_person(person_id: int = Path(ge=1), db: Session = Depends(get_db),
                     current_user: User = Depends(auth_service.get_current_user)):
    person = await repository_persons.get_person_by_id(person_id, db, current_user)
    if person is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return person


@router.post("/", response_model=PersonResponse, status_code=status.HTTP_201_CREATED)
async def create_person(body: PersonModel, db: Session = Depends(get_db),
                        current_user: User = Depends(auth_service.get_current_user)):
    person = await repository_persons.get_person_by_name(body.first_name, body.last_name, db, current_user)
    if person:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User is exists")
    person = await repository_persons.create(body, db, current_user)
    return person


@router.put("/{person_id}", response_model=PersonResponse)
async def update_person(body: PersonModel, person_id: int = Path(ge=1), db: Session = Depends(get_db),
                        current_user: User = Depends(auth_service.get_current_user)):
    person = await repository_persons.update(person_id, body, db, current_user)
    if person is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return person


@router.delete("/{person_id}", response_model=PersonResponse)
async def delete_person(person_id: int = Path(ge=1), db: Session = Depends(get_db),
                        current_user: User = Depends(auth_service.get_current_user)):
    person = await repository_persons.remove(person_id, db, current_user)
    if person is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return person

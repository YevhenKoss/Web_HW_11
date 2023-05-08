from typing import List

from fastapi import FastAPI, Depends, HTTPException, status, Path, Query
from sqlalchemy import text
from sqlalchemy.orm import Session

from db import get_db
from models import User, Contact
from schemas import UserModel, UserResponse, ContactModel, ContactResponse

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    try:
        # Make request
        result = db.execute(text("SELECT 1")).fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")


@app.get("/users", response_model=List[UserResponse], tags=["users"])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@app.get("/users/{user_id}", response_model=UserResponse, tags=["users"])
async def get_user(user_id: int = Path(ge=1), db: Session = Depends(get_db)):
    user = db.query(User).filter_by(id=user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return user


@app.post("/users", response_model=UserResponse, tags=["users"])
async def create_user(body: UserModel, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(first_name=body.first_name, last_name=body.last_name).first()
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User is exists")
    user = User(**body.dict())
    db.add(user)
    db.commit()
    return user


@app.put("/users/{user_id}", response_model=UserResponse, tags=["users"])
async def update_user(body: UserModel, user_id: int = Path(ge=1), db: Session = Depends(get_db)):
    user = db.query(User).filter_by(id=user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    user.first_name = body.first_name
    user.last_name = body.last_name
    db.commit()
    return user


@app.delete("/users/{user_id}", response_model=UserResponse, tags=["users"])
async def delete_user(user_id: int = Path(ge=1), db: Session = Depends(get_db)):
    user = db.query(User).filter_by(id=user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    db.delete(user)
    db.commit()
    return user


@app.get("/contacts", response_model=List[ContactResponse], tags=["contacts"])
async def get_contacts(limit: int = Query(10, le=300), offset: int = 0, db: Session = Depends(get_db)):
    contacts = db.query(Contact).limit(limit).offset(offset).all()
    return contacts


@app.get("/contacts/{contact_id}", response_model=ContactResponse, tags=["contacts"])
async def get_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contact


@app.post("/contacts", response_model=ContactResponse, tags=["contacts"])
async def create_contact(body: ContactModel, db: Session = Depends(get_db)):
    contact_email = db.query(Contact).filter_by(email=body.email).first()
    contact_phone = db.query(Contact).filter_by(phone=body.phone).first()
    if contact_email or contact_phone:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Contact is exists")
    contact = Contact(**body.dict())
    db.add(contact)
    db.commit()
    return contact


@app.put("/contacts/{contact_id}", response_model=ContactResponse, tags=["contacts"])
async def update_contact(body: ContactModel, contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    contact.email = body.email
    contact.phone = body.phone
    contact.note = body.note
    contact.user_id = body.user_id
    db.commit()
    return contact


@app.delete("/contacts/{contact_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["contacts"])
async def delete_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    db.delete(contact)
    db.commit()
    return None

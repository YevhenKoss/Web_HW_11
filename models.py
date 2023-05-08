from enum import unique

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from db import Base, engine


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    date_of_birth = Column(DateTime, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, unique=True, index=True)
    note = Column(String, index=True, nullable=True, default=None)
    blocked = Column(Boolean, nullable=True, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", backref="contacts")


Base.metadata.create_all(bind=engine)

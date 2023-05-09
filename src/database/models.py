from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


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
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())




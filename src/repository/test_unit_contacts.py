import datetime
import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.repository.contacts import get_contacts, get_contact_by_id, get_contact_by_email, get_contact_by_phone, create, \
    update

from src.schemas import ContactModel


class TestContacts(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.user = MagicMock()
        self.db = MagicMock()
        self.body = MagicMock()

    async def test_get_contacts(self):
        contacts = [Contact() for _ in range(5)]
        self.db.query(Contact).filter_by(self.user).limit().offset().all.return_value = contacts
        result = await get_contacts(self.user, 10, 0, self.db)
        self.assertEqual(result, contacts)

    async def test_get_contact_by_id(self):
        expected_contact = MagicMock()
        self.db.query.return_value.filter_by.return_value.first.return_value = expected_contact
        contact = await get_contact_by_id(self.user, 1, self.db)
        self.db.query.assert_called_once()
        self.db.query.return_value.filter_by.assert_called_once_with(user_id=self.user.id, id=1)
        self.db.query.return_value.filter_by.return_value.first.assert_called_once()
        self.assertEqual(contact, expected_contact)

    async def test_get_contact_by_email(self):
        expected_contact = MagicMock()
        self.db.query.return_value.filter_by.return_value.first.return_value = expected_contact
        contact = await get_contact_by_email(self.user, "test@email.com", self.db)
        self.db.query.assert_called_once()
        self.db.query.return_value.filter_by.assert_called_once_with(user_id=self.user.id, email="test@email.com")
        self.db.query.return_value.filter_by.return_value.first.assert_called_once()
        self.assertEqual(contact, expected_contact)

    async def test_get_contact_by_phone(self):
        expected_contact = MagicMock()
        self.db.query.return_value.filter_by.return_value.first.return_value = expected_contact
        contact = await get_contact_by_phone(self.user, "test_phone", self.db)
        self.db.query.assert_called_once()
        self.db.query.return_value.filter_by.assert_called_once_with(user_id=self.user.id, phone="test_phone")
        self.db.query.return_value.filter_by.return_value.first.assert_called_once()
        self.assertEqual(contact, expected_contact)

    async def test_create_contact(self):
        body = ContactModel(
            date_of_birth="2023-05-29",
            email="test@email.com",
            phone="phone",
            note=None,
            blocked=False,
            person_id=1
        )
        contact = await create(self.user, body, self.db)
        self.assertEqual(contact.date_of_birth, body.date_of_birth)
        self.assertEqual(contact.email, body.email)
        self.assertEqual(contact.phone, body.phone)
        self.assertEqual(contact.note, body.note)
        self.assertEqual(contact.blocked, body.blocked)
        self.assertEqual(contact.person_id, body.person_id)
        self.assertTrue(hasattr(contact, 'id'))

    async def test_update_contact(self):
        body = ContactModel(
            date_of_birth=datetime.date(2023, 5, 29),
            email="test@email.com",
            phone="phone",
            note=None,
            blocked=False,
            person_id=1
        )
        contact = await update(self.user, 1, body, self.db)
        self.assertEqual(contact.date_of_birth, body.date_of_birth)
        self.assertEqual(contact.email, body.email)
        self.assertEqual(contact.phone, body.phone)
        self.assertEqual(contact.note, body.note)
        self.assertEqual(contact.blocked, body.blocked)
        self.assertEqual(contact.person_id, body.person_id)
        self.assertTrue(hasattr(contact, 'id'))


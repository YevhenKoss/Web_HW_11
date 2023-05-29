import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.repository.contacts import get_contacts, get_contact_by_id


class TestContacts(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_get_contacts(self):
        contacts = [Contact() for _ in range(5)]
        self.session.query(Contact).filter_by(self.user).limit().offset().all.return_value = contacts
        result = await get_contacts(self.user, 10, 0, self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact_by_id(self):
        contact = Contact()
        self.session.query().filter_by().first().return_value = contact
        result = await get_contact_by_id(user=self.user, contact_id=1, db=self.session)
        self.assertEqual(result, contact)

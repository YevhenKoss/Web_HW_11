import datetime
import unittest
from unittest.mock import MagicMock

from src.database.models import Contact, Person
from src.repository.contacts import get_contacts, get_contact_by_id, get_contact_by_email, get_contact_by_phone, create, \
    update, remove, block, get_contact_by_person, get_contacts_by_email, get_contacts_hb_id_list, \
    get_contacts_hb
from src.schemas import ContactModel, ContactBlackList


class TestContacts(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.user = MagicMock()
        self.db = MagicMock()
        self.body = MagicMock()
        self.person = Person(first_name="Jon", last_name="Doe")
        self.data = MagicMock(id=1)

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

    async def test_remove_contact(self):
        expected_contact = MagicMock()
        self.db.query.return_value.filter_by.return_value.first.return_value = expected_contact
        contact = await remove(self.user, 1, self.db)
        self.db.query.assert_called_once()
        self.db.query.return_value.filter_by.return_value.first.assert_called_once()
        self.db.delete.assert_called_once_with(expected_contact)
        self.db.commit.assert_called_once()
        self.assertEqual(contact, expected_contact)

    async def test_block_contact(self):
        body = ContactBlackList(
            blocked=False
        )
        contact = await block(self.user, 1, body, self.db)
        self.assertEqual(contact.blocked, body.blocked)

    async def test_get_contact_by_person(self):
        expected_contact = MagicMock()
        self.db.query.return_value.filter_by.return_value.all.return_value = expected_contact
        contact = await get_contact_by_person(self.user, self.person, self.db)
        self.assertEqual(contact, expected_contact)

    async def test_get_contacts_by_email(self):
        expected_contacts = [MagicMock(), MagicMock()]
        self.db.query.return_value.filter_by.return_value.all.return_value = expected_contacts
        contacts = await get_contacts_by_email(self.user, "test@email.com", self.db)
        self.assertEqual(contacts, expected_contacts)

    # async def test_search_contacts(self):
    #     expected_contacts = [MagicMock(id=1)]
    #     persons_fn = [MagicMock(id=1)]
    #     persons_ln = []
    #     self.db.query.return_value.filter_by.return_value.all.return_value = expected_contacts
    #
    #     get_person_by_first_name_mock = MagicMock()
    #     get_person_by_first_name_mock.return_value = persons_fn
    #     search_contacts.get_person_by_first_name = get_person_by_first_name_mock
    #     search_contacts.get_person_by_last_name = MagicMock(return_value=persons_ln)
    #     get_contact_by_person_mock = MagicMock()
    #     get_contact_by_person_mock.return_value = [expected_contacts[0]]
    #     search_contacts.get_contact_by_person = get_contact_by_person_mock
    #     contacts = await search_contacts(self.user, self.data, self.db)
    #     search_contacts.get_person_by_last_name.assert_not_called()
    #     self.assertEqual(contacts, expected_contacts)

    async def test_get_contacts_hb_id_list(self):
        expected_contact_ids = [1]
        contacts = [MagicMock(id=1, date_of_birth=datetime.date(1990, 6, 3))]
        self.db.query.return_value.filter_by.return_value.all.return_value = contacts
        contact_ids = await get_contacts_hb_id_list(self.user, self.db)
        self.db.query.assert_called_once()
        self.db.query.return_value.filter_by.assert_called_once_with(user_id=self.user.id)
        self.db.query.return_value.filter_by.return_value.all.assert_called_once()
        self.assertEqual(contact_ids, expected_contact_ids)

    async def test_get_contacts_hb(self):
        expected_contacts = [MagicMock(id=1)]
        id_list = [1]
        self.db.query.return_value.filter_by.return_value.limit.return_value.offset.return_value.all.return_value = expected_contacts
        contacts = await get_contacts_hb(self.user, id_list, 10, 0, self.db)
        self.assertEqual(contacts, expected_contacts)

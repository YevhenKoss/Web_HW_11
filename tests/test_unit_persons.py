import unittest
from unittest.mock import MagicMock

from src.repository.persons import get_persons, get_person_by_id, get_person_by_name, create, update, remove, \
    get_person_by_first_name, get_person_by_last_name
from src.schemas import PersonModel


class TestPersons(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.user = MagicMock()
        self.db = MagicMock()
        self.body = MagicMock()

    async def test_get_persons(self):
        persons = MagicMock()
        self.db.query.return_value.filter_by.return_value.all.return_value = persons
        result = await get_persons(self.db, self.user)
        self.assertEqual(result, persons)

    async def test_get_person_by_id(self):
        expected_person = MagicMock()
        self.db.query.return_value.filter_by.return_value.first.return_value = expected_person
        person = await get_person_by_id(1, self.db, self.user)
        self.db.query.assert_called_once()
        self.db.query.return_value.filter_by.assert_called_once_with(id=1, user_id=self.user.id)
        self.db.query.return_value.filter_by.return_value.first.assert_called_once()
        self.assertEqual(person, expected_person)

    async def test_get_person_by_name(self):
        expected_person = MagicMock()
        self.db.query.return_value.filter_by.return_value.first.return_value = expected_person
        person = await get_person_by_name("Jon", "Doe", self.db, self.user)
        self.db.query.assert_called_once()
        self.db.query.return_value.filter_by.assert_called_once_with(first_name="Jon", last_name="Doe",
                                                                     user_id=self.user.id)
        self.db.query.return_value.filter_by.return_value.first.assert_called_once()
        self.assertEqual(person, expected_person)

    async def test_create_person(self):
        body = PersonModel(
            first_name="Jon",
            last_name="Doe",
        )
        person = await create(body, self.db, self.user)
        self.assertEqual(person.first_name, body.first_name)
        self.assertEqual(person.last_name, body.last_name)
        self.assertTrue(hasattr(person, 'id'))

    async def test_update_person(self):
        body = PersonModel(
            first_name="Jon",
            last_name="Doe",
        )
        person = await update(1, body, self.db, self.user)
        self.assertEqual(person.first_name, body.first_name)
        self.assertEqual(person.last_name, body.last_name)

    async def test_remove_person(self):
        expected_person = MagicMock()
        self.db.query.return_value.filter_by.return_value.first.return_value = expected_person
        person = await remove(1, self.db, self.user)
        self.db.query.assert_called_once()
        self.db.query.return_value.filter_by.return_value.first.assert_called_once()
        self.db.delete.assert_called_once_with(expected_person)
        self.db.commit.assert_called_once()
        self.assertEqual(person, expected_person)

    async def test_get_person_by_first_name(self):
        expected_person = MagicMock()
        self.db.query.return_value.filter_by.return_value.all.return_value = expected_person
        person = await get_person_by_first_name("Jon", self.db, self.user)
        self.db.query.assert_called_once()
        self.db.query.return_value.filter_by.assert_called_once_with(first_name="Jon", user_id=self.user.id)
        self.assertEqual(person, expected_person)

    async def test_get_person_by_last_name(self):
        expected_person = MagicMock()
        self.db.query.return_value.filter_by.return_value.all.return_value = expected_person
        person = await get_person_by_last_name("Doe", self.db, self.user)
        self.db.query.assert_called_once()
        self.db.query.return_value.filter_by.assert_called_once_with(last_name="Doe", user_id=self.user.id)
        self.assertEqual(person, expected_person)

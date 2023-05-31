import unittest
from unittest.mock import MagicMock, patch
import logging
from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel
from src.repository.users import (
    get_user_by_email,
    create_user,
    confirmed_email,
    update_token, update_avatar
)


class TestUsers(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.db = MagicMock(spec=Session)
        self.user = User(id=1)
        self.user_test = User(
            id=1,
            username='username',
            password='password',
            email='test2@gmail.com',
            confirmed='False',
            avatar='https://example.com/avatar.jpg'

        )

    async def test_get_user_by_email(self):
        expected_user = self.user_test
        query_mock = self.db.query.return_value
        filter_mock = query_mock.filter.return_value
        filter_mock.first.return_value = expected_user
        user = await get_user_by_email("test@email.com", self.db)
        self.assertEqual(user, expected_user)

    async def test_create_user(self):
        expected_user = self.user_test
        add_mock = self.db.add
        commit_mock = self.db.commit
        refresh_mock = self.db.refresh
        user = await create_user(UserModel(**expected_user.__dict__), self.db)
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, expected_user.username)
        self.assertEqual(user.email, expected_user.email)
        self.assertEqual(user.password, expected_user.password)
        self.assertNotEqual(user.avatar, "gravatar")
        self.assertEqual(user.refresh_token, None)
        self.db.add.assert_called_once_with(user)
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()
        add_mock.assert_called_once_with(user)
        commit_mock.assert_called_once()
        refresh_mock.assert_called_once()

    async def test_update_token(self):
        expected_user = self.user_test
        token = 'new token'
        self.db.commit = MagicMock()
        await update_token(expected_user, token, self.db)
        self.assertEqual(expected_user.refresh_token, token)
        self.db.commit.assert_called_once()

    async def test_confirmed_email(self):
        email = "test@email.com"
        user_mock = MagicMock(spec=User)
        user_mock.confirmed = True
        self.db.query().filter().one_or_none.return_value = user_mock
        self.db.commit = MagicMock()
        await confirmed_email(email, self.db)
        self.assertTrue(user_mock.confirmed)
        self.db.commit.assert_called_once()

    async def test_update_avatar(self):
        user = User(email="test@email.com")
        result = await update_avatar("test@email.com", "https://example.com/avatar.png", self.db)
        self.assertEqual(user.avatar, None)
        self.assertEqual("https://example.com/avatar.png", result.avatar)

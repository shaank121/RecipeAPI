from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email(self):
        email = 'shaank121@test.com'
        password = 'Test4454'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_create_user_with_normalize_email(self):
        email = 'shaank121@test.com'
        password = 'Test4454'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_with_invalid_email(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test')

    def test_new_superuser(self):
        """ Test create new Super User"""
        user = get_user_model().objects.create_superuser(
            'test@abc.com', 
            'test'
            )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

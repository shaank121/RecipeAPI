from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


class PublicUserAPITests(TestCase):
    """Test user API Public"""
    def create_user(**params):
        return get_user_model().objects.create_user(**params)
    
    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid paload and successfull"""
        payload = {
            'email': 'test@test1.com',
            'password': 'testpass',
            'name': 'TestName'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        
        user = get_user_model().objects.get(**res.data)
        
        self.assertTrue(user.check_password(payload['test@test1.com', 
                                                    'testpass']))
        self.assertNotIn('testpass', res.data)    

    def test_user_exists(self):
        """Test if user exist """
        payload = {'email': 'test@test1.com','password': 'testpass'}
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test Password more then 5 character"""
        payload = {'email': 'test@test1.com', 'password': 'pw'}
        
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        
        self.assertFalse(user_exists)

    def test_create_for_user(self):
        payload = {'email': 'test@test1.com', 'password': 'testpass'}
        self.create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credential(self):
        self.create_user({'email': 'test@test1.com', 'password': 'testpass'})
        payload = {'email': 'test@test1.com', 'password': 'wrong'}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_craete_token_no_usern(self):
        #create_user('email':'test@test1.com','password':'testpass')
        payload = {'email': 'test@test2.com', 'password': 'testpass'}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_craete_token_missing_field(self):
        #create_user('email':'test@test1.com','password':'testpass')
        payload = {'email': 'test@test3.com', 'password': ''}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)







from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_jwt.settings import api_settings


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


CREATE_URL = reverse('user:create')
TOKEN_URL = reverse('user:auth_token')
ME_URL = reverse('user:me')

def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTest(TestCase):
    """Test the users API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_successful(self):
        """Test creating a user with valid credentials is successfull"""
        payload = {
            'email': 'test@greatsoft.uz',
            'password': 'testpassword',
        }
        res = self.client.post(CREATE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        res.data.pop('token', None)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_create_user_exists(self):
        """Test creating user that exists"""
        payload = {
            'email': 'test@greatsoft.uz',
            'password': 'testpassword',
        }
        create_user(**payload)
        res = self.client.post(CREATE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test creating user with too short password"""
        payload = {
            'email': 'test@greatsoft.uz',
            'password': '123',
        }
        res = self.client.post(CREATE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token(self):
        """Test that token is created for the user"""
        payload = {
            'email':'test@password',
            'password':'testpasss',
        }

        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_create_token_invalid_credetials_given(self):
        """Test creating a token when invalid credentials are given"""
        create_user(email='test@greatsoft.uz', password='testpasss')
        payload = {
            'email':'test@greatsoft.uz',
            'password': 'none'
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test creating a new token if a user does not exist"""
        payload = {
            'email': 'test@greatsoft.uz',
            'password':'testpassword'
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_token_missing_field(self):
        """Test creating token with missing fields"""
        res = self.client.post(TOKEN_URL, {'email': 'test', 'password':''})

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retriver_user_unauthorized(self):
        """Test that authentication is required for users"""
        res = self.client.get(ME_URL)
        
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUsersApiTest(TestCase):
    """Test API requests that requires authentication"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='test@greatsoft.uz', password='password')
        self.client.force_authenticate(user=self.user)
    
    def test_retrive_profile_success(self):
        """Test retriving profile for authenticated user"""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'email': self.user.email,
        })
    
    def test_post_me_not_allowed(self):
        """Test that POST is not allowed on the me url"""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def test_update_user_profile(self):
        """Test updating user profile for authenticated user"""
        payload = {
            'email':'new_email@greatsoft.uz',
            'password':'testpassword_'
        }
        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, payload['email'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

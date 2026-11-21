from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from users.models import User

class UserAuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_registration_successful(self):
        url = reverse('register')
        data = {
            'email': 'newuser@example.com',
            'name': 'New User',
            'phone': '+91 9123456789',
            'password': 'SecurePassword@123',
            'role': 'Attendee'
        }
        res = self.client.post(url, data, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn('tokens', res.data)
        self.assertIn('access', res.data['tokens'])
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())

    def test_registration_password_rule_enforcement(self):
        url = reverse('register')
        # Missing uppercase and digit
        bad_data = {
            'email': 'badpass@example.com',
            'name': 'Bad Password',
            'password': 'simplepassword',
            'role': 'Attendee'
        }
        res = self.client.post(url, bad_data, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', res.data)

    def test_login_successful_and_jwt_tokens(self):
        user = User.objects.create_user(
            email='loginuser@example.com',
            name='Login User',
            password='ValidPassword@123',
            role='Attendee'
        )
        url = reverse('login')
        res = self.client.post(url, {'email': 'loginuser@example.com', 'password': 'ValidPassword@123'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('tokens', res.data)
        self.assertEqual(res.data['user']['email'], 'loginuser@example.com')

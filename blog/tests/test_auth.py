from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_rest_passwordreset.models import ResetPasswordToken

User = get_user_model()

class UserTests(APITestCase):

    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.password_reset_url = reverse('password_reset')
        self.password_reset_confirm_url = reverse('password_reset_confirm')
        self.totp_url = reverse('totp')
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'testuser@example.com'
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_user_registration(self):
        new_user_data = {
            'username': 'newuser',
            'password': 'newpassword',
            'email': 'newuser@example.com'
        }
        response = self.client.post(self.register_url, new_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_user_login(self):
        response = self.client.post(self.login_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.access_token = response.data['access']
        self.refresh_token = response.data['refresh']

    def test_user_logout(self):
        self.test_user_login()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.post(self.logout_url, {'refresh': self.refresh_token}, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

    def test_password_reset(self):
        response = self.client.post(self.password_reset_url, {'email': self.user_data['email']}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_password_reset_confirm(self):
        # Request password reset to get a valid token
        self.client.post(self.password_reset_url, {'email': self.user_data['email']}, format='json')
        # Get the token from the email
        reset_token = ResetPasswordToken.objects.first().key
        response = self.client.post(self.password_reset_confirm_url, {'token': reset_token, 'password': 'ComplexPassword123!'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_totp_device_list(self):
        self.test_user_login()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.get(self.totp_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_totp_device_create(self):
        self.test_user_login()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.post(self.totp_url, {'name': 'My TOTP Device'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TOTPDevice.objects.count(), 1)
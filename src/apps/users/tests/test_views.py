from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from apps.users.serializers import RegisterSerializer


User = get_user_model()


class UserRegistrationViewTest(APITestCase):
    """Class to test user registration view"""

    def setUp(self) -> None:
        self.register_url = reverse("users:register")

    def test_user_registration(self) -> None:
        """Test that user registered successfully"""

        data = {
            "email": "test@example.com",
            "password": "testpass123",
            "confirm_password": "testpass123",
            "first_name": "John",
            "last_name": "Doe",
        }

        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(email=data['email'])
        self.assertEqual(user.email, data['email'])
        self.assertEqual(user.first_name, data['first_name'])
        self.assertEqual(user.last_name, data['last_name'])
        self.assertTrue(user.check_password(data['password']))


class UserLoginTest(APITestCase):
    """Class to test user login"""

    def setUp(self) -> None:
        self.login_url = reverse("users:login")
        self.data = {
            "email": "test@test.com",
            "password": "Testpassword123",
            "is_active": True
        }
        User.objects.create_user(
            email=self.data['email'], password=self.data['password'],
            is_active=self.data['is_active']
        )

    def test_user_login(self) -> None:
        """Test that user can log in successfully"""

        data = {
            "email": self.data['email'],
            "password": self.data['password']
        }
        response = self.client.post(self.login_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_login_failed(self) -> None:
        """Test that user login failed"""

        data = {
            "email": self.data['email'],
            "password": "Newpassword123"
        }
        response = self.client.post(self.login_url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserChangePasswordView(APITestCase):
    """Class to test change password"""

    def setUp(self) -> None:
        self.change_password_url = reverse("users:change_password")
        self.login_url = reverse("users:login")
        self.data = {
            "email": "test@test.com",
            "password": "Testpassword123",
            "is_active": True
        }
        self.user = User.objects.create_user(
            email=self.data['email'], password=self.data['password'],
            is_active=self.data['is_active']
        )

    def test_user_change_password_successfully(self) -> None:
        """Test that user successfully changes password"""

        data = {
            "old_password": self.data["password"],
            "new_password": "NewPassword123"
        }

        login_data = {
            "email": self.data["email"],
            "password": self.data["password"]
        }

        response = self.client.post(self.login_url, login_data)

        access_token = response.data["access"]
        auth_header = f"Bearer {access_token}"

        self.client.credentials(HTTP_AUTHORIZATION=auth_header)

        response = self.client.put(self.change_password_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_change_password_fails(self) -> None:
        """Test that user changes password with error"""

        data = {
            "old_password": "NewPassword123123",
            "new_password": "NewPassword123213"
        }

        login_data = {
            "email": self.data["email"],
            "password": self.data["password"]
        }

        response = self.client.post(self.login_url, login_data)

        access_token = response.data["access"]
        auth_header = f"Bearer {access_token}"

        self.client.credentials(HTTP_AUTHORIZATION=auth_header)

        response = self.client.put(self.change_password_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

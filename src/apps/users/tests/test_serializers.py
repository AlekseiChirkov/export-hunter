from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework import serializers

from apps.users.serializers import RegisterSerializer


User = get_user_model()


class RegisterSerializerTest(TestCase):
    """Class to test register serializer"""

    def test_create_valid_user(self) -> None:
        """Test that user creates with validated data"""

        data = {
            "email": "test@test.com",
            "password": "Testpassword123",
            "confirm_password": "Testpassword123",
            "first_name": "John",
            "last_name": "Doe"
        }

        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        user = serializer.save()
        self.assertEqual(user.email, data['email'])
        self.assertEqual(user.first_name, data['first_name'])
        self.assertEqual(user.last_name, data['last_name'])
        self.assertTrue(user.check_password(data['password']))

    def test_create_user_passwords_not_match(self) -> None:
        """Test that passwords not match raises error"""

        data = {
            "email": "test@test.com",
            "password": "Testpassword123",
            "confirm_password": "testpassword123",
            "first_name": "John",
            "last_name": "Doe"
        }

        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        with self.assertRaises(serializers.ValidationError):
            serializer.save()

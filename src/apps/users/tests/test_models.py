from django.test import TestCase
from django.contrib.auth import get_user_model


User = get_user_model()


class UserModelTest(TestCase):
    """Class to test User model"""

    def setUp(self) -> None:
        self.email = 'test@test.com'
        self.password = 'Testpassword123'
        self.extra_fields = {'first_name': 'John', 'last_name': 'Doe'}

    def test_create_user(self) -> None:
        """Test that user creates successfully"""

        user = User.objects.create_user(
            self.email, self.password, **self.extra_fields
        )

        self.assertEqual(user.email, self.email)
        self.assertEqual(user.first_name, self.extra_fields['first_name'])
        self.assertEqual(user.last_name, self.extra_fields['last_name'])
        self.assertTrue(user.check_password(self.password))

    def test_create_user_no_email(self) -> None:
        """Test that create user no email raises error"""

        with self.assertRaises(ValueError):
            User.objects.create_user(None, self.password, **self.extra_fields)

    def test_create_superuser(self) -> None:
        """Test that superuser creates successfully"""

        user = User.objects.create_superuser(self.email, self.password)

        self.assertEqual(user.email, self.email)
        self.assertTrue(user.check_password(self.password))

    def test_create_superuser_no_staff(self) -> None:
        """Test that no staff raises error"""

        self.extra_fields['is_staff'] = False
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                self.email, self.password, **self.extra_fields
            )

    def test_create_superuser_no_superuser(self) -> None:
        """Test that no superuser raises error"""

        self.extra_fields['is_superuser'] = False
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                self.email, self.password, **self.extra_fields
            )

    def test_user_object_string_representation(self) -> None:
        """Test that user object str method works correctly"""

        user = User.objects.create_user(
            self.email, self.password, **self.extra_fields
        )

        self.assertEqual(str(user), self.email)

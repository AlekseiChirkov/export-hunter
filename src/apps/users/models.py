from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Custom user manager"""

    def create_user(self, email: str, password: str = None,
                    **extra_fields) -> models.QuerySet:
        """
        Method creates simple user
        :param email: user's email that will be used as username
        :type email: str
        :param password: user's password
        :type password: str
        :param extra_fields: extra fields to add
        :type extra_fields: dict
        :return: User object
        :rtype: models.QuerySet
        """

        if not email:
            raise ValueError("Email is required.")

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str,
                         **extra_fields) -> models.QuerySet:
        """
        Method creates django superuser to access admin panel
        :param email: superuser's email will be used as username
        :type email: str
        :param password: superuser's password
        :type password: str
        :param extra_fields: extra fields to add
        :type extra_fields: dict
        :return: User object
        :rtype: models.QuerySet
        """

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """User model class"""

    email = models.EmailField(_('Email address'), unique=True, blank=False)
    phone = models.CharField(max_length=50, blank=True, null=True, unique=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    father_name = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return f"{self.email}"

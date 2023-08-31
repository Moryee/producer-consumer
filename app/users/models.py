from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, username):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.username = username

        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, username):
        user = self.create_user(
            email=email,
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=50)
    probation = models.IntegerField(default=0, help_text='Probation in days')

    class Position(models.TextChoices):
        MANAGER = 'manager', _('Manager')
        EMPLOYEE = 'employee', _('Employee')

    position = models.CharField(
        max_length=50,
        choices=Position.choices,
        default=Position.EMPLOYEE,
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

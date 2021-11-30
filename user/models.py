from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from user.common.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
    )

    first_name = models.CharField(max_length=255, verbose_name='first name')
    last_name = models.CharField(max_length=255, verbose_name='last name')
    phone_number = models.CharField(max_length=255, null=True, blank=True, unique=True, verbose_name='phone number')
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='date of birth')
    is_admin = models.BooleanField(default=False, verbose_name='is admin')
    status = models.BooleanField(default=True, verbose_name='is active')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} / {self.email}"

    @property
    def is_active(self):
        return self.status

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin or self.is_superuser

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

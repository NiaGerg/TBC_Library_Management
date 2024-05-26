from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class User(AbstractUser):
    email = models.EmailField(unique=True)
    personal_number = models.CharField(max_length=20, unique=True)
    birth_date = models.DateField()

    groups = models.ManyToManyField(Group, related_name='user_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='user_permissions')

    REQUIRED_FIELDS = ['email', 'personal_number', 'birth_date', 'first_name', 'last_name']
    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE = (
        ('user', 'user'),
        ('admin', 'admin'),
        ('moderator', 'moderator'),
    )
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    role = models.CharField(max_length=25, choices=ROLE, default='user')

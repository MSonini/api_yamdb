from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE = (
        ('User','User'),
        ('Admin','Admin'),
        ('Moderator','Moderator'),
    )
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    role = models.CharField(max_length=25, choices=ROLE, default='User')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['email', 'username'],
                name='unique_username_email'
            )
        ]
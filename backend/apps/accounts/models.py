import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator


class User(AbstractUser):
    """
    Custom user:
    - UUID primary key
    - unique email
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)

    class Meta:
        # indexing the email field for faster queries
        indexes = [models.Index(fields=["email"], name="user_email_idx")]

    def __str__(self):
        return self.username

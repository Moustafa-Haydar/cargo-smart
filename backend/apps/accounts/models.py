import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator


class User(AbstractUser):
    """
    Custom user:
    - UUID primary key
    - unique email
    - optional FK to RBAC Role
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=150, unique=True, validators=[UnicodeUsernameValidator()])
    email = models.EmailField(unique=True)
    role = models.ForeignKey("rbac.Role", null=True, blank=True, on_delete=models.SET_NULL, related_name="users")

    class Meta:
        # indexing the email field for faster queries
        indexes = [models.Index(fields=["email"], name="user_email_idx")]

    def __str__(self):
        return self.username

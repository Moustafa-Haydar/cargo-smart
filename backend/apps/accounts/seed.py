from typing import Iterable, Dict, Any, Tuple
from django.db import transaction
from django.apps import apps

# ---- seed data ----

USERS = [
    {
        "first_name": "Admin",
        "last_name": "Admin",
        "username": "admin",
        "password": "ssssssss",
        "email": "programmermoustafa@gmail.com",
        "group": "Admin"
    },
    {
        "first_name": "Moustafa",
        "last_name": "Haydar",
        "username": "mustish",
        "password": "ssssssss",
        "email": "moustafahaydar.eng@gmail.com",
        "group": "Ops Manager"
    }
]


@transaction.atomic
def seed_accounts(stdout=None):
    Group = apps.get_model("rbac", "Group")
    User = apps.get_model("accounts", "User")
    UserGroup = apps.get_model("rbac", "UserGroup")

    users = {}

    for u in USERS:

        try:
            group = Group.objects.get(name=u["group"])
        except Group.DoesNotExist:
            raise ValueError(f"Group '{u['group']}' does not exist. User '{u['username']}' not registered.")

        user, created = User.objects.get_or_create(
            username=u["username"],
            defaults={
                "first_name": u["first_name"],
                "last_name": u["last_name"],
                "email": u["email"],
            },
        )

        if created:
            user.set_password(u["password"])
            user.save(update_fields=["password"])

        users[user] = user.id

        UserGroup.objects.get_or_create(user_id=user.id, group_id=group.id)

    return users
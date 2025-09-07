from typing import Iterable, Dict, Any, Tuple
from django.db import transaction
from django.apps import apps
from django.contrib.auth.models import Group as AuthGroup

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
    },
    {
        "first_name": "John",
        "last_name": "Doe",
        "username": "john",
        "password": "ssssssss",
        "email": "john.eng@gmail.com",
        "group": "Driver"
    },
    {
        "first_name": "Adel",
        "last_name": "Smith",
        "username": "adel",
        "password": "ssssssss",
        "email": "adel.eng@gmail.com",
        "group": "Driver"
    },
    {
        "first_name": "Sarah",
        "last_name": "Williams",
        "username": "sarah",
        "password": "ssssssss",
        "email": "sarah.eng@gmail.com",
        "group": "Driver"
    }
]


@transaction.atomic
def seed_accounts(stdout=None):
    RBACGroup = apps.get_model("rbac", "Group")
    User = apps.get_model("accounts", "User")
    UserGroup = apps.get_model("rbac", "UserGroup")

    users = {}

    # First ensure all auth groups exist
    for u in USERS:
        group_name = u["group"]
        # Create both RBAC and Auth groups
        rbac_group = RBACGroup.objects.get(name=group_name)
        auth_group, _ = AuthGroup.objects.get_or_create(name=group_name)

    for u in USERS:
        try:
            rbac_group = RBACGroup.objects.get(name=u["group"])
            auth_group = AuthGroup.objects.get(name=u["group"])
        except (RBACGroup.DoesNotExist, AuthGroup.DoesNotExist):
            raise ValueError(f"Group '{u['group']}' does not exist. User '{u['username']}' not registered.")

        user, created = User.objects.get_or_create(
            username=u["username"],
            email=u["email"],
            defaults={
                "first_name": u["first_name"],
                "last_name": u["last_name"]
            },
        )

        if created:
            user.set_password(u["password"])
            user.save(update_fields=["password"])

        users[user] = user.id

        # Add user to both RBAC and Auth groups
        UserGroup.objects.get_or_create(user_id=user.id, group_id=rbac_group.id)
        user.groups.add(auth_group)

    if stdout:
        stdout.write("Accounts seeding done.")

    return users
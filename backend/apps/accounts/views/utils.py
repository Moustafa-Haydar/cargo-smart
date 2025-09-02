from apps.rbac.models import Group, Permission
from apps.accounts.models import User


def _group_payload(group):
    if not group:
        return None
    return {
        "id": str(group.id),
        "name": getattr(group, "name", None),
        "description": getattr(group, "description", None),
    }


def _user_permissions(user: User):
    """
    Collect permission ids & codenames via the user's groups.
    """
    # SELECT DISTINCT permission fields via join
    perms = (
        Permission.objects.filter(group_permissions__group__user_groups__user=user)
        .distinct()
        .values("id", "app_label", "codename", "name")
    )
    ids = [str(p["id"]) for p in perms]
    codes = [f'{p["app_label"]}.{p["codename"]}' for p in perms]
    return ids, codes


def _user_payload(user: User):
    perm_ids, perm_codes = _user_permissions(user)
    groups = list(
        Group.objects.filter(user_groups__user=user)
        .values("id", "name")
    )
    return {
        "id": str(user.id),
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "email": user.email,
        "groups": groups,
        "permissions": {
            "perm_ids" : perm_ids,
            "perm_codes" : perm_codes
        }
    }
from apps.rbac.models import Group, Permission


def _group_payload(group):
    if not group:
        return None
    return {
        "id": str(group.id),
        "name": getattr(group, "name", None),
        "description": getattr(group, "description", None),
    }


def _user_payload(user):
    groups = list(
        Group.objects
             .filter(user_groups__user_id=user.id)
             .values("id", "name")
    )

    return {
        "id": str(user.id),
        "username": user.username,
        "email": user.email,
        "groups": groups,
    }

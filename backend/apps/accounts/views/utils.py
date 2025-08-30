

def _role_payload(role):
    if not role:
        return None
    return {
        "id": str(role.id),
        "name": getattr(role, "name", None),
        "description": getattr(role, "description", None),
    }

def _user_payload(user):
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": _role_payload(getattr(user, "role", None)),
    }
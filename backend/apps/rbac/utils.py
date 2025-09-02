
def has_perm(user, perm: str) -> bool:
    """perm format: 'app_label.codename' e.g., 'shipments.create'"""
    
    if not (user and user.is_authenticated):
        return False
    
    try:
        app_label, codename = perm.split(".", 1)
    except ValueError:
        return False
    
    return user.groups.filter(
        permissions__app_label=app_label,
        permissions__codename=codename,
    ).exists()

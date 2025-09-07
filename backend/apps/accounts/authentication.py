from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed


class BearerTokenAuthentication(TokenAuthentication):
    """
    Custom token authentication that uses Bearer format instead of Token format
    """
    keyword = 'Bearer'

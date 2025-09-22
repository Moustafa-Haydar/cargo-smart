from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from apps.accounts.authentication import BearerTokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import json
from apps.rbac.models import UserGroup


# Serializer for login request
class MobileLoginSerializer(serializers.Serializer):
    username = serializers.CharField(help_text="Driver username")
    password = serializers.CharField(help_text="Driver password", write_only=True)

# Serializer for login response
class MobileLoginResponseSerializer(serializers.Serializer):
    token = serializers.CharField(help_text="Authentication token")
    user = serializers.DictField(help_text="User information")

@swagger_auto_schema(
    method='post',
    operation_description="Mobile login endpoint for drivers. Returns a token for authentication.",
    request_body=MobileLoginSerializer,
    responses={
        200: openapi.Response(
            description="Login successful",
            schema=MobileLoginResponseSerializer
        ),
        400: openapi.Response(
            description="Bad request - missing username/password or invalid JSON",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        ),
        401: openapi.Response(
            description="Invalid credentials",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        ),
        403: openapi.Response(
            description="Access denied - user is not a driver",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        )
    },
    tags=['Mobile Authentication']
)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
@csrf_exempt
def mobile_login(request):
    """
    Mobile login endpoint for drivers
    Returns a token for authentication
    """
    try:
        data = json.loads(request.body.decode() or "{}")
    except json.JSONDecodeError:
        return Response({"error": "Invalid JSON"}, status=status.HTTP_400_BAD_REQUEST)

    username = (data.get("username") or "").strip()
    password = data.get("password") or ""
    
    if not username or not password:
        return Response({"error": "username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

    # Authenticate user
    user = authenticate(request, username=username, password=password)
    if not user:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    # Check if user is a driver
    user_groups = UserGroup.objects.filter(user=user).select_related('group')
    user_group_names = [ug.group.name for ug in user_groups]
    
    if 'Driver' not in user_group_names:
        return Response({"error": "Access denied. Only drivers can use mobile app."}, status=status.HTTP_403_FORBIDDEN)

    # Get or create token for the user
    token, created = Token.objects.get_or_create(user=user)
    
    return Response({
        'token': token.key,
        'user': {
            'id': str(user.id),
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_active': user.is_active,
            'groups': user_group_names,
        }
    })


@swagger_auto_schema(
    method='post',
    operation_description="Logout endpoint for mobile apps. Deletes the user's authentication token.",
    responses={
        200: openapi.Response(
            description="Logout successful",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        ),
        400: openapi.Response(
            description="Bad request",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        )
    },
    tags=['Mobile Authentication'],
    security=[{'Bearer': []}]
)
@api_view(['POST'])
@authentication_classes([BearerTokenAuthentication])
@permission_classes([IsAuthenticated])
def mobile_logout(request):
    """
    Logout endpoint for mobile apps
    Deletes the user's token
    """
    try:
        # Delete the token
        request.user.auth_token.delete()
        return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='get',
    operation_description="Get current user profile for mobile apps",
    responses={
        200: openapi.Response(
            description="User profile retrieved successfully",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'user': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_STRING),
                            'username': openapi.Schema(type=openapi.TYPE_STRING),
                            'email': openapi.Schema(type=openapi.TYPE_STRING),
                            'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                            'last_name': openapi.Schema(type=openapi.TYPE_STRING),
                            'is_active': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                            'groups': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING))
                        }
                    )
                }
            )
        )
    },
    tags=['Mobile Authentication'],
    security=[{'Bearer': []}]
)
@api_view(['GET'])
@authentication_classes([BearerTokenAuthentication])
@permission_classes([IsAuthenticated])
def mobile_profile(request):
    """
    Get current user profile for mobile apps
    """
    user = request.user
    user_groups = UserGroup.objects.filter(user=user).select_related('group')
    
    return Response({
        'user': {
            'id': str(user.id),
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_active': user.is_active,
            'groups': [ug.group.name for ug in user_groups],
        }
    })

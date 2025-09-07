# apps/accounts/api_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class JWTMeView(APIView):
    authentication_classes = [JWTAuthentication] # JWT only (mobile)
    permission_classes = [IsAuthenticated]

    def get(self, request):
        u = request.user
        return Response({"id": u.id, "username": u.get_username()})

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import RegistrationSerializer


class RegistrationView(APIView):
    """Registers a new user."""

    permission_classes = [AllowAny]

    def post(self, request):
        """Create a new user account."""

        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "User created successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginTokenView(TokenObtainPairView):
    """Logs in a user and sets JWT cookies."""

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """Validate user credentials and set auth cookies."""

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        response_data = {
            'detail': 'Login successfully!',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }
        response = Response(response_data, status=status.HTTP_200_OK)
        self.set_token_cookies(response, serializer.validated_data)
        return response
    
    def set_token_cookies(self, response, token_data):
        """Set access and refresh tokens as HTTP-only cookies."""

        response.set_cookie(
            key="access_token",
            value=token_data["access"],
            httponly=True,
            secure=False,
            samesite="Lax",
        )
        response.set_cookie(
            key="refresh_token",
            value=token_data["refresh"],
            httponly=True,
            secure=False,
            samesite="Lax",
        )


class LogoutView(APIView):
    """Logs out a user by deleting auth cookies."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Delete auth cookies from the response."""

        response = Response({"detail": "Log-Out successfully! All Tokens will be deleted. Refresh token is now invalid."})
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response


class RefreshTokenView(TokenRefreshView):
    """Refreshes the access token using the refresh cookie."""

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """Create a new access token from the refresh cookie."""

        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token is None:
            return Response({"detial": "Refresh token invalid or missing."}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = self.get_serializer(data={'refresh': refresh_token})
        serializer.is_valid(raise_exception=True)
        response = Response({"detail": "Token refreshed"})
        self.set_access_cookie(response, serializer.validated_data["access"])
        return response
        
    def set_access_cookie(self, response, access_token):
        """Set the new access token as an HTTP-only cookie."""
        
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False,
            samesite="Lax",
        )

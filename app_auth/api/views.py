from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import RegisterSerializer


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "User created successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginTokenView(TokenObtainPairView):
    pass


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
       response = Response()
       response.delete_cookie('access_token')
       response.delete_cookie('refresh_token')
       response.data = {'message' : 'Sucessfully logged out'}
       return response


class RefreshTokenView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token is None:
            return Response({"detial": "Refresh token not found"}, status=status.HTTP_400_BAD_REQUEST)

        request.data['refresh'] = refresh_token
        serializer = self.get_serializer(data={'refresh': refresh_token})
        try:
            serializer.is_valid(raise_exception=True)
        except:
            return Response({"detail": "Invalid refresh token "}, status=401)
        
        access_token = serializer.validated_data.get("access")
        response = Response({"detail": "Token refreshed", "access": access_token})
        response.set_cookie(
            key="access_token",
            httponly=True,
            value=access_token,
            secure=False,
            samesite='Lax'
        ),
        return response

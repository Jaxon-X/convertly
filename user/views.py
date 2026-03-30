
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from user.models import CustomUser
from user.serializers import RegisterSerializer, LoginSerializer


def build_auth_payload(user, message):
    tokens = RefreshToken.for_user(user)
    return {
        "username": user.username,
        "email": user.email,
        "is_email_verified": user.is_email_verified,
        "refresh": str(tokens),
        "access": str(tokens.access_token),
        "message": message,
    }


class RegisterView(APIView):
    def post(self, request):
        try:
            serializer = RegisterSerializer(data=request.data)

            if serializer.is_valid():
                user = serializer.save()
                return Response(
                    build_auth_payload(user, "User successfully registered"),
                    status=status.HTTP_201_CREATED,
                )

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error" : str(e)})

class LoginView(APIView):
    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                email = serializer.validated_data['email']
                password = serializer.validated_data['password']

                user = authenticate(request=request, username=email, password=password)
                if user is None:
                    return Response({"error": "username or password are not correct"}, status=status.HTTP_400_BAD_REQUEST)
                return Response(build_auth_payload(user, "User successfully logged in"))
            return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)})



class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error" : "token must have"}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"msg": "Logout successful."}, status=status.HTTP_200_OK)

        except Exception as e:
                return Response({"error" : str(e)})


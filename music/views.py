from rest_framework_jwt.settings import api_settings
#from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import status
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .serializers import SongsSerializer, TokenSerializer, UserSerializer, UserAltSerializer
from .models import Songs


# Get the JWT settings, add these lines after the import/from lines
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class ListSongsView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    queryset = Songs.objects.all()
    serializer_class = SongsSerializer
    permission_classes = (permissions.IsAuthenticated,)

class ListUsersView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    queryset = User.objects.all()
    serializer_class = UserAltSerializer

class RegisterUsersView(generics.CreateAPIView):
    
    #POST api/v1/register/
    
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        
        username = request.data.get("username", "")
        email = request.data.get("email", "")
        password = request.data.get("password", "")

        serialized = UserSerializer(data=request.data)
        if not username or not password or not email:
            print("EMPTU FIELDS")
            return Response(
                data={
                    "message": "username, password and email is required to register a user"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if serialized.is_valid(self):
            new_user = User.objects.create_user(
                username=username, email=email, password=password
            )
            new_user.save()
            print("1:  " , UserSerializer(new_user).data)
            return Response(
                data=UserSerializer(new_user).data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(generics.CreateAPIView):
    """
    POST auth/login/
    """
    serializer_class = UserSerializer
    # This permission class will overide the global permission
    # class setting
    permission_classes = (permissions.AllowAny,)

    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # login saves the user’s ID in the session,
            # using Django’s session framework.
            login(request, user)
            serializer = TokenSerializer(data={
                # using drf jwt utility functions to generate a token
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )})
            serializer.is_valid()
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(generics.CreateAPIView):
    queryset = User.objects.all()
    def get(self, request, *args, **kwargs):
        logout(request)
        return Response(
            data={
                "message": "Logged out succesfully."
            }, status=status.HTTP_200_OK)


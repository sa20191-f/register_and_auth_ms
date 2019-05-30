
from django.core import exceptions
import django.contrib.auth.password_validation as validators
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Songs


class SongsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Songs
        fields = ("title", "artist")

class TokenSerializer(serializers.Serializer):
    """
    This serializer serializes the token data
    """
    token = serializers.CharField(max_length=255)

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'})
    class Meta:
        model = User
        fields = ("username", "email", "password")

    def validate(self, data):
         # here data has all the fields which have validated values
         # so we can create a User instance out of it
         user = User(**data)

         # get the password from the data
         password = data.get('password')

         errors = dict() 
         try:
             # validate the password and catch the exception
             validators.validate_password(password=password, user=User)

         # the exception raised here is different than serializers.ValidationError
         except exceptions.ValidationError as e:
             errors['password'] = list(e.messages)

         if errors:
             raise serializers.ValidationError(errors)

         return super(UserSerializer, self).validate(data)

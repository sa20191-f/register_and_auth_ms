from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Songs(models.Model):
    title = models.CharField(max_length=255, null=False)
    artist = models.CharField(max_length=255, null=False)

    def __str__(self):
        return "{} - {}".format(self.title, self.artist)

# class User(models.Model):
#     email = models.EmailField(unique=True, max_length=75)
#     username = models.CharField(unique=True, max_length=25)
#     date_joined = models.DateTimeField(default=timezone.now)
#     is_active = models.BooleanField(default=True)
#     is_admin = models.BooleanField(default=False)

class UserTokenInfo(models.Model):
    userID = models.IntegerField()
    tokenType = models.IntegerField(default=1)
    token = models.CharField(max_length=1000, null=False)

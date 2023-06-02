from django.db import models
from django.contrib.auth.models import User
# from django.contrib.auth.models import AbstractUser

# Create your models here.

# class Users(AbstractUser):
#     username = models.CharField(max_length=255, unique=True)
#     password = models.CharField(max_length=255)

class FriendShip(models.Model):

    first_user = models.ForeignKey(User, on_delete=models.CASCADE)
    second_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    status = models.IntegerField()

    def __str__(self):
        return f'({self.first_user}, {self.second_user}, {str(self.status)})'
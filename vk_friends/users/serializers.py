from rest_framework import serializers
from .models import FriendShip
# from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer

# class UserRegistrationSerializer(BaseUserRegistrationSerializer):
#     class Meta(BaseUserRegistrationSerializer.Meta):
#         fields = ('username', 'password', )

# class UsersSerializer(serializers.Serializer):
#     username = serializers.CharField(max_length=255)


# class FriendShipSerializer(serializers.Serializer):

#     first_user = serializers.CharField(source='first_user.username', max_length=255)
#     second_user = serializers.CharField(source='second_user.username', max_length=255)
#     status = serializers.IntegerField()


#     def create(self, validated_data):
#         return FriendShip.objects.create(**validated_data)


#     def update(self, instance, validated_data):
#         # instance.title = validated_data.get("title", instance.title)
#         instance.save()
#         return instance

class FriendShipSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendShip
        fields = ("first_user", "second_user", "status")




# class MyTestSerializer(serializers.Serializer):

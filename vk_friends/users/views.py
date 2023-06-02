from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Q
from .serializers import FriendShipSerializer
from .models import FriendShip
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView


class AddFriendAPIView(APIView):

    permission_classes = (IsAuthenticated, )

    def post(self, request):

        id1 = request.user.id
        id2 = request.query_params['second_user']


        if len(FriendShip.objects.filter(first_user=id1, second_user=id2, status=0)):
            # сообщение о том, что заявка уже отправлена
            friendship = FriendShip.objects.get(first_user=id1, second_user=id2, status=0)
        elif len(FriendShip.objects.filter(first_user=id1, second_user=id2, status=1)) or len(FriendShip.objects.filter(first_user=id2, second_user=id1, status=1)):
            # сообщение о том, что вы уже друзья
            try:
                friendship = FriendShip.objects.get(first_user=id1, second_user=id2, status=1)
            except FriendShip.DoesNotExist:
                friendship = FriendShip.objects.get(first_user=id2, second_user=id1, status=1)
        elif len(FriendShip.objects.filter(first_user=id2, second_user=id1, status=0)):
            # обновляем запись: id2 id1 0 -> id2 id1 1
            friendship = FriendShip.objects.get(first_user=id2, second_user=id1, status=0)
            friendship.status = 1
            friendship.save()
            pass
        else:
            friendship = FriendShip.objects.create(first_user=User.objects.get(id=id1),
                                                   second_user=User.objects.get(id=id2),
                                                   status=0)
        serializer = FriendShipSerializer(friendship)
        return Response(serializer.data)


class CheckIncomingAPIView(ListAPIView):
    serializer_class = FriendShipSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        id1 = self.request.user.id
        queryset = FriendShip.objects.filter(second_user=id1, status=0)
        return queryset


class CheckOutgoingAPIView(ListAPIView):
    serializer_class = FriendShipSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        id1 = self.request.user.id
        queryset = FriendShip.objects.filter(first_user=id1, status=0)
        return queryset


class CheckFriendsAPIView(ListAPIView):
    serializer_class = FriendShipSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        id1 = self.request.user.id
        queryset = FriendShip.objects.filter(Q(first_user=id1) | Q(second_user=id1), Q(status=1))
        return queryset


class AcceptFriendAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    def put(self, request):

        id1 = request.user.id
        id2 = request.query_params['friend']

        try:
            friendship = FriendShip.objects.get(first_user=id2, second_user=id1)
        except FriendShip.DoesNotExist:
            data = {"message": "wrong user id or friend-request not found"}
        else:
            if friendship.status:
                data = {"message": "you are already friends"}
            else:
                friendship.status = 1
                friendship.save()
                serializer = FriendShipSerializer(friendship)
                data = serializer.data

        return Response(data)


class RejectFriendAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    def delete(self, request):

        id1 = request.user.id
        id2 = request.query_params['friend']

        try:
            friendship = FriendShip.objects.get(first_user=id2, second_user=id1)
        except FriendShip.DoesNotExist:
            data = {"message": "wrong user id or friend-request not found"}
        else:
            friendship.delete()
            data = {"message": "friend-request was successfully rejected"}

        return Response(data)


class GetFriendShipStatusAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):

        id1 = request.user.id
        id2 = request.query_params['friend']

        try:
            friendship = FriendShip.objects.get(Q(first_user=id1) | Q(first_user=id2),
                                                Q(second_user=id1) | Q(second_user=id2))
        except FriendShip.DoesNotExist:
            data = {"message": "you are not friends"}
        else:
            serializer = FriendShipSerializer(friendship)
            data = serializer.data

        return Response(data)


class DeleteFriendAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    def delete(self, request):

        id1 = request.user.id
        id2 = request.query_params['friend']

        try:
            friendship = FriendShip.objects.get(Q(first_user=id1) | Q(first_user=id2),
                                                Q(second_user=id1) | Q(second_user=id2))
        except FriendShip.DoesNotExist:
            data = {"message": "wrong user id or friend-request not found"}
        else:
            friendship.delete()
            data = {"message": "successfully deleting friend"}
        return Response(data)

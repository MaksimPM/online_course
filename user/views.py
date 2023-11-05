from rest_framework import generics
from user.models import User
from user.permissions import IsOwnerProfile
from user.serializers import UserSerializer, UserSerializerForStranger
from rest_framework.permissions import IsAuthenticated


class UserCreate(generics.CreateAPIView):
    serializer_class = UserSerializer


class UserListAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.user.is_staff:
            serializer_class = UserSerializer
        else:
            serializer_class = UserSerializerForStranger
        return serializer_class


class UserRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()

    def get_serializer_class(self):

        if self.kwargs['id'] == self.request.user.id or self.request.user.is_staff:
            serializer_class = UserSerializer
        else:
            serializer_class = UserSerializerForStranger
        return serializer_class


class UserUpdateAPIView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated, IsOwnerProfile)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDestroyAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated, IsOwnerProfile,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

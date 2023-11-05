from rest_framework import serializers

from courses.serializers import PaymentSerializer
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'avatar', 'phone', 'city', 'payments', 'password')


class UserSerializerForStranger(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'phone', 'city', 'avatar')

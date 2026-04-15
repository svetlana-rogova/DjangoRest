from rest_framework import serializers
from users.models import CustomUser, Payments


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = '__all__'


class PaymentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payments
        fields = '__all__'


class UserPaymentsSerializer(serializers.ModelSerializer):
    payments = PaymentsSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'phone_number', 'avatar', 'country', 'payments']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password', 'phone_number', 'avatar', 'country']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
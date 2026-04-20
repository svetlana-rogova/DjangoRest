from rest_framework import serializers
from users.models import CustomUser, Payments


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели CustomUser. Включает основные данные профиля пользователя.
    """
    class Meta:
        model = CustomUser
        fields = ['last_login', 'username', 'first_name', 'date_joined', 'email', 'country', 'avatar']


class PaymentsSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Payments. Включает основные данные по платежам.
    """
    class Meta:
        model = Payments
        fields = '__all__'


class UserPaymentsSerializer(serializers.ModelSerializer):
    """
    Сериализатор для данных пользователя и связанных с ним платежей.
    """
    payments = PaymentsSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'phone_number', 'avatar', 'country', 'payments']


class RegisterSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации.
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password', 'phone_number', 'avatar', 'country']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

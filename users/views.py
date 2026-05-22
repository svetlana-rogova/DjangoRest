from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView, DestroyAPIView, CreateAPIView, RetrieveAPIView
from users.models import CustomUser, Payments
from users.permissions import IsOwnerOrReadOnly
from users.serializers import UserSerializer, PaymentsSerializer, UserPaymentsSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter


class UserEditView(RetrieveUpdateAPIView):
    """
       Представление для просмотра и редактирования профиля пользователя.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserPaymentsSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self):
        return self.request.user


class PaymentsList(generics.ListAPIView):
    """
       Представление для просмотра списка платежей с возможностью фильтрации и сортировки.
    """
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['paid_course', 'paid_lesson', 'payment_method']
    ordering_fields = ['payment_date']


class UserListView(ListAPIView):
    """
        Представление для просмотра списка пользователей.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserDetailView(RetrieveAPIView):
    """
        Представление для просмотра одного профиля.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class RegisterView(CreateAPIView):
    """
        Представление для регистрации.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class UserDeleteView(DestroyAPIView):
    """
        Представление для удаления профиля.
    """
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self):
        return self.request.user

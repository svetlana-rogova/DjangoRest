from django.urls import path

from users.models import CustomUser
from users.views import UserEditView, PaymentsList

app_name = 'users'

urlpatterns = [
    path('users/', UserEditView.as_view(queryset=CustomUser.objects.all(), serializer_class='UserSerializer'), name='user-list'),
    path('payments/', PaymentsList.as_view(), name='payments-list'),
]


from django.urls import path

from users.models import CustomUser
from users.views import UserEditView

app_name = 'users'

urlpatterns = [
    path('users/', UserEditView.as_view(queryset=CustomUser.objects.all(), serializer_class='UserSerializer'), name='user-list')
]


from django.urls import path

from users.views import UserEditView, PaymentsList, UserListView, UserDetailView, UserDeleteView, RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'users'


urlpatterns = [
    path('users/me/', UserEditView.as_view(), name='user-me'),
    path('payments/', PaymentsList.as_view(), name='payments_list'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', UserListView.as_view(), name='users_list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='users_detail'),
    path('users/delete/', UserDeleteView.as_view(), name='users_delete'),
    path('register/', RegisterView.as_view(), name='register'),
]

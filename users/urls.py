from django.urls import path

from users.views import UserEditView, PaymentsList, UserListView, UserDetailView, UserDeleteView, RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'users'



urlpatterns = [
    path('users/me/', UserEditView.as_view(), name='user-list'),
    path('payments/', PaymentsList.as_view(), name='payments-list'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', UserListView.as_view()),
    path('users/<int:pk>/', UserDetailView.as_view()),
    path('users/delete/', UserDeleteView.as_view()),
    path('register/', RegisterView.as_view()),
]

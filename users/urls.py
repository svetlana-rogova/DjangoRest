from django.urls import path

from users.views import UserEditView, PaymentsList

app_name = 'users'



urlpatterns = [
    path('users/<int:pk>/', UserEditView.as_view(), name='user-list'),
    path('payments/', PaymentsList.as_view(), name='payments-list'),
]


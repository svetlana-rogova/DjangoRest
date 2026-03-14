from rest_framework.generics import RetrieveUpdateAPIView
from users.models import CustomUser
from users.serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated


class UserEditView(RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

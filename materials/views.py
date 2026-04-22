from materials.models import Course, Lesson, Subscription
from materials.paginators import MaterialsPagination
from materials.permissions import IsModerator, IsOwner
from materials.serializers import LessonSerializer, CourseSerializer
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response


class CourseViewSet(viewsets.ModelViewSet):
    """
    Представление для работы с курсами (CRUD операции).
    """
    pagination_class = MaterialsPagination
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action == 'list':
            self.permission_classes = [IsModerator]
        elif self.action == 'delete':
            self.permission_classes = [IsOwner | ~IsModerator]
        elif self.action == 'update':
            self.permission_classes = [IsModerator | IsOwner]
        elif self.action == 'retrieve':
            self.permission_classes = [IsModerator | IsOwner]
        return [permission() for permission in self.permission_classes]


class LessonCreateAPIView(generics.CreateAPIView):
    """
    Представление для добавления урока
    """
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]


class LessonListAPIView(generics.ListAPIView):
    """
    Представление для просмотра уроков
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator]
    pagination_class = MaterialsPagination



class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """
    Представление для просмотра конкретного урока
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """
    Представление для изменения урока
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """
    Представление для удаления урока
    """
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner | ~IsModerator]


class SubscriptionAPIView(APIView):
    """
       Эндпоинт для управления подпиской пользователя на курс.
    """
    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get('course_id')
        course_item = get_object_or_404(Course, id=course_id)

        subs_item = Subscription.objects.filter(owner=user, course=course_item)

            # Если подписка у пользователя на этот курс есть - удаляем ее
        if subs_item.exists():
            subs_item.delete()
            message = 'подписка удалена'
            # Если подписки у пользователя на этот курс нет - создаем ее
        else:
            Subscription.objects.create(owner=user, course=course_item)
            message = 'подписка добавлена'
            # Возвращаем ответ в API
        return Response({"message": message})


from materials.models import Course, Lesson
from materials.permissions import IsModerator, IsOwner
from materials.serializers import LessonSerializer, CourseSerializer
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


class CourseViewSet(viewsets.ModelViewSet):
    """
    Представление для работы с курсами (CRUD операции).
    """
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
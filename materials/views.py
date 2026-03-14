from materials.models import Course, Lesson
from materials.serializers import LessonSerializer, CourseSerializer
from  rest_framework import viewsets
from rest_framework import generics


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer



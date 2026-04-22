from rest_framework import serializers

from materials.models import Lesson, Course
from materials.validators import validate_link


class LessonSerializer(serializers.ModelSerializer):
    """
    Сериализатор для урока.
    """
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [validate_link]


class CourseSerializer(serializers.ModelSerializer):
    """
    Сериализатор для курса.
    """
    count_lesson = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_count_lesson(self, obj):
        return obj.lessons.count()

    class Meta:
        model = Course
        fields = '__all__'

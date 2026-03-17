from rest_framework import serializers

from materials.models import Lesson, Course


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    count_lesson = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_count_lesson(self, obj):
        return obj.lessons.count()

    class Meta:
        model = Course
        fields = '__all__'
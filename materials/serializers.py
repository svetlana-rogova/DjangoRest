from rest_framework import serializers

from materials.models import Lesson, Course, Subscription
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
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Subscription.objects.filter(owner=request.user, course=obj).exists()


    def get_count_lesson(self, obj):
        return obj.lessons.count()

    class Meta:
        model = Course
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    """
    Сериализатор для подписки.
    """
    class Meta:
        model = Subscription
        fields = '__all__'

from django.utils import timezone
from datetime import timedelta
from materials.models import Subscription, Course
from celery import shared_task
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
import os
from dotenv import load_dotenv
load_dotenv()


@shared_task
def send_mail_user(course_id):
    """
    Задача на рассылку сообщений подписчикам при обновлении курса при условии, что курс не обновлялся последние 4 часа
    """
    subscription = Subscription.objects.filter(course_id=course_id)
    course = get_object_or_404(Course, id=course_id)
    subject = 'Обновление курса'
    message = 'Привет. В твой курс добавили новую информацию. Скорее посмотри что изменилось.'
    from_email = os.getenv('MY_EMAIL')
    if timezone.now() - course.updated_at > timedelta(hours=4):
        for sub in subscription:
            recipient_list = [sub.owner.email]
            send_mail(subject, message, from_email, recipient_list)

from users.models import CustomUser
from materials.models import Subscription
from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_mail_user(course_id):
    subscription = Subscription.objects.filter(course_id=course_id)
    for sub in subscription:
        subject = 'Обновление курса'
        message = 'Привет. В твой курс добавили новую информацию. Скорее посмотри что изменилось.'
        from_email = 'mifistofiya@gmail.com'
        recipient_list = [sub.owner.email]
        send_mail(subject, message, from_email, recipient_list)
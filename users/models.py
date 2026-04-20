from django.db import models
from django.contrib.auth.models import AbstractUser

from materials.models import Course, Lesson


class CustomUser(AbstractUser):
    """
    Модель пользователя
    """
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    country = models.CharField(max_length=15, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class Payments(models.Model):
    """
    Модель платежа
    """
    STATUS_CHOICES = [
        ('cash', 'Cash'),
        ('translation', 'Translation'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='payments')
    payment_date = models.DateTimeField(auto_now_add=True)
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='payments', null=True, blank=True)
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='payments', null=True, blank=True)
    payment_amount = models.IntegerField()
    payment_method = models.CharField(max_length=15, choices=STATUS_CHOICES, default='cash')

    def __str__(self):
        return f'Оплата прошла от пользователя: {self.user}, сумма: {self.payment_amount}'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'
from django.db import models



class Course(models.Model):
    """
    Модель курса
    """
    title = models.CharField(max_length=150, verbose_name='Название')
    image = models.ImageField(upload_to='images/', verbose_name='Картинка', blank=True, null=True)
    description = models.TextField(verbose_name='Описание')
    owner = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='course', null=True, blank=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    """
    Модель урока
    """
    title = models.CharField(max_length=150, verbose_name='Название')
    image = models.ImageField(upload_to='images/', verbose_name='Картинка', blank=True, null=True)
    description = models.TextField(verbose_name='Описание')
    video_url = models.URLField(verbose_name="Ссылка на видео")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    owner = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='lesson', null=True, blank=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'



class Subscription(models.Model):
    """
    Модель подписки
    """
    owner = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='subscription')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subscription')

    def __str__(self):
        return f'{self.course}'

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'

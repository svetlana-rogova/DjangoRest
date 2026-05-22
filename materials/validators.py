from rest_framework.serializers import ValidationError


def validate_link(value):
    """
    Проверка на отсутствие в материалах ссылок на сторонние ресурсы, кроме youtube.com.
    """
    fields = ['video_url', 'description', 'title']
    for field in fields:
        materials = value.get(field)
        if materials and 'http' in materials:
            if 'youtube.com' not in materials:
                raise ValidationError('Разрешены только ссылки на YouTube')

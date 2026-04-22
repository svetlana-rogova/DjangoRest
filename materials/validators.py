from rest_framework.serializers import  ValidationError


def validate_video(value):
    video = value.get('video_url')
    if 'youtube.com' not in video:
        raise ValidationError('Разрешены только ссылки на YouTube')

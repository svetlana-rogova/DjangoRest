from django.contrib import admin

from materials.models import Course, Lesson


@admin.register(Course)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'description')
    search_fields = ('title',)

@admin.register(Lesson)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'description', 'video_url', 'course')
    search_fields = ('title',)


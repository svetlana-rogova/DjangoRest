from django.contrib import admin

from users.models import CustomUser, Payments


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone_number', 'avatar', 'country')
    search_fields = ('email',)


@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    list_display = ('user', 'payment_date', 'paid_course', 'paid_lesson', 'payment_amount', 'payment_method')
    search_fields = ('user',)

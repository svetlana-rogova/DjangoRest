from materials.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, SubscriptionAPIView, PaymentCreateAPIView, PaymentStatusAPIView
from rest_framework.routers import DefaultRouter
from django.urls import path


app_name = 'materials'

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
    path('lesson/', LessonListAPIView.as_view(), name='lesson-list'),
    path('lesson/retrieve/<int:pk>', LessonRetrieveAPIView.as_view(), name='lesson-retrieve'),
    path('lesson/update/<int:pk>', LessonUpdateAPIView.as_view(), name='lesson-update'),
    path('lesson/delete/<int:pk>', LessonDestroyAPIView.as_view(), name='lesson-delete'),
    path('subscription/', SubscriptionAPIView.as_view(), name='subscription'),
    path('payment/create/', PaymentCreateAPIView.as_view(), name='payment-create'),
    path('payment/status/<str:session_id>/', PaymentStatusAPIView.as_view(), name='payment-status'),
] + router.urls

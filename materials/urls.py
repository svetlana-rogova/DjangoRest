from materials.views import CourseViewSet
from rest_framework.routers import DefaultRouter


app_name = 'materials'

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [

] + router.urls
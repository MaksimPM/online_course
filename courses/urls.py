from django.urls import path
from rest_framework.routers import DefaultRouter
from courses.apps import CoursesConfig
from courses.views import LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, LessonDestroyAPIView, \
    CourseViewSet, \
    LessonUpdateAPIView, PaymentListAPIView

app_name = CoursesConfig.name

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lesson/', LessonListAPIView.as_view(), name='lesson_list'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson_get'),
    path('lesson/<int:pk>/update/', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lesson/<int:pk>/delete/', LessonDestroyAPIView.as_view(), name='lesson_delete'),
    path('course/payment/', PaymentListAPIView.as_view(), name='payments')
] + router.urls

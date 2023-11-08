from django.urls import path
from rest_framework.routers import DefaultRouter
from courses.apps import CoursesConfig
from courses.views import *

app_name = CoursesConfig.name

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lesson/', LessonListAPIView.as_view(), name='lesson_list'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson_get'),
    path('lesson/<int:pk>/update/', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lesson/<int:pk>/delete/', LessonDestroyAPIView.as_view(), name='lesson_delete'),
    path('course/payment/', PaymentListAPIView.as_view(), name='payments'),
    path('subscriptions/create/', SubscriptionCreateAPIView.as_view(), name='subscription_create'),
    path('subscriptions/', SubscriptionListAPIView.as_view(), name='subscriptions'),
    path('subscriptions/<int:pk>/', SubscriptionRetrieveAPIView.as_view(), name='subscription'),
    path('subscriptions/<int:pk>/update/', SubscriptionUpdateAPIView.as_view(), name='subscriptions_update'),
    path('subscriptions/<int:pk>/delete/', SubscriptionDestroyAPIView.as_view(), name='subscriptions_delete'),
] + router.urls

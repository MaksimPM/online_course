from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView
from courses.serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter


class LessonListAPIView(ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonCreateAPIView(CreateAPIView):
    serializer_class = LessonSerializer


class LessonRetrieveAPIView(RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['course', 'lesson', 'payment_method']
    ordering_fields = ['payment_date']

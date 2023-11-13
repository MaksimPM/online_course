from datetime import datetime, timedelta

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView

from courses.permissions import IsNotModeratorForAPIView, IsOwner, IsNotModeratorForViewSet
from courses.serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework_simplejwt.views import TokenObtainPairView

from courses.services import send_notification
from courses.stripe_api import create_intent, get_intent


class LessonListAPIView(ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated,)


class LessonCreateAPIView(CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsNotModeratorForAPIView,)

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()

    def create(self, request, *args, **kwargs):
        if 'course' in request.data:
            course = Course.objects.get(pk=request.data['course'])
            delta = datetime.now() - course.last_update.replace(tzinfo=None)
            if delta > timedelta(hours=4):
                send_notification(course)
            course.last_update = datetime.now()
            course.save()
        return super().create(request, *args, **kwargs)


class LessonRetrieveAPIView(RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsOwner,)


class LessonUpdateAPIView(UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsOwner,)

    def update(self, request, *args, **kwargs):
        lesson = Lesson.objects.get(pk=kwargs['pk'])
        if lesson.course:
            course = Course.objects.get(pk=lesson.course.pk)
            delta = datetime.now() - course.last_update.replace(tzinfo=None)
            if delta > timedelta(hours=4):
                send_notification(course)
            course.last_update = datetime.now()
            course.save()
        return super().update(request, *args, **kwargs)


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsOwner, IsNotModeratorForAPIView,)


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (IsAuthenticated, IsNotModeratorForViewSet,)

    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Course.objects.all()
        return Course.objects.filter(owner=user.pk)

    def update(self, request, *args, **kwargs):
        course = Course.objects.get(pk=kwargs['pk'])
        send_notification(course)
        return super().update(request, *args, **kwargs)


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['course', 'lesson', 'payment_method']
    ordering_fields = ['payment_date']
    permission_classes = (IsAuthenticated,)


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return create_intent(request)

    def perform_create(self, serializer):
        new_payment = serializer.save()
        new_payment.user = self.request.user
        new_payment.stripe_id = create_intent(self.request).data['intent']['id']
        new_payment.save()


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def get(self, request, *args, **kwargs):
        return get_intent(kwargs['pk'])


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class SubscriptionCreateAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SubscriptionSerializer

    def perform_create(self, serializer):
        new_subscription = serializer.save()
        new_subscription.user = self.request.user
        new_subscription.subscribed = True
        new_subscription.save()


class SubscriptionListAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, IsAdminUser,)
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()


class SubscriptionRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated, IsAdminUser,)
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()


class SubscriptionUpdateAPIView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated, IsAdminUser,)
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Subscription.objects.all()

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView

from courses.permissions import IsNotModeratorForAPIView, IsOwner, IsNotModeratorForViewSet
from courses.serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework_simplejwt.views import TokenObtainPairView


class LessonListAPIView(ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated,)


class LessonCreateAPIView(CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsNotModeratorForAPIView,)


class LessonRetrieveAPIView(RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsOwner,)


class LessonUpdateAPIView(UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsOwner,)


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsOwner, IsNotModeratorForAPIView,)


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (IsAuthenticated, IsNotModeratorForViewSet,)


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['course', 'lesson', 'payment_method']
    ordering_fields = ['payment_date']
    permission_classes = (IsAuthenticated,)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class SubscriptionCreateAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SubscriptionSerializer

    def perform_create(self, serializer):
        """Сохраняет авторизованного пользователя в объекте подписки"""

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

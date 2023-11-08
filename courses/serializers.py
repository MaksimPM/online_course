from rest_framework import serializers
from courses.models import Lesson, Course, Payment, Subscription
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from courses.validators import VideoUrlValidator, DescriptionValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [
            DescriptionValidator(fields='description'),
            VideoUrlValidator(fields='video_url')
        ]


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.IntegerField()
    lessons = LessonSerializer(source='lesson.all', many=True, read_only=True)
    subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'
        validators = [
            DescriptionValidator(fields='description'),
        ]

    def get_lessons_count(self, instance):
        return instance.lessons.count()

    def get_subscribed(self, obj):
        user = self.context['request'].user
        if Subscription.objects.filter(user=user).filter(course=obj).exists():
            return True
        return False


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email

        return token


class SubscriptionSerializer(serializers.ModelSerializer):
    subscribed = serializers.BooleanField(read_only=True)
    user = serializers.CharField(read_only=True)

    class Meta:
        model = Subscription
        fields = '__all__'

    def validate(self, atr):
        user = self.context['request'].user
        course = Course.objects.get(pk=atr['course'].pk)
        if Subscription.objects.filter(user=user, course=course).exists():
            raise serializers.ValidationError("Подписка уже существует")
        return atr

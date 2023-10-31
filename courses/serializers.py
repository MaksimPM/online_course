from rest_framework import serializers
from courses.models import Lesson, Course, Payment


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True)

    class Meta:
        model = Course
        fields = '__all__'

    def get_lessons_count(self, instance):
        return instance.lessons.count()


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

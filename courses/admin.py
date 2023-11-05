from django.contrib import admin

from courses.models import Course, Lesson, Payment


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'preview', 'description',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'preview', 'description', 'video_link',)


@admin.register(Payment)
class Payment(admin.ModelAdmin):
    list_display = ('id', 'payment_date', 'payment_amount', 'payment_method',)

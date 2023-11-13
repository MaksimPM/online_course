from django_celery_beat.models import PeriodicTask, IntervalSchedule

from courses.models import Subscription
from courses.tasks import send_notification_task


def set_schedule(*args, **kwargs):
    schedule, created = IntervalSchedule.objects.get_or_create(
            every=10,
            period=IntervalSchedule.SECONDS,
        )
    PeriodicTask.objects.create(
        interval=schedule,
        name='Check user last login',
        task='courses.tasks.check_user_last_login_task',
    )


def send_notification(course):
    if Subscription.objects.filter(course=course).exists():
        subscriptions = Subscription.objects.filter(course=course)
        recipient_list = []
        for sub in subscriptions:
            recipient_list.append(sub.user.email)
        send_notification_task.delay(
            course_title=course.title,
            recipient_list=recipient_list
        )

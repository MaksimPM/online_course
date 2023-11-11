from django.core.management import BaseCommand

from courses.models import Payment, Lesson, Course
from user.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):

        user = User.objects.get(pk=int(input("Пользователь: ")))

        lesson = None
        course = None
        choice = int(input("Урок - 1, курс - 2: "))
        if choice == 1:
            lesson = Lesson.objects.get(pk=int(input("Урок: ")))
        elif choice == 2:
            course = Course.objects.get(pk=int(input("Курс: ")))

        payment_method = int(input("Наличные - 1, перевод - 2: "))
        if payment_method == 1:
            payment_method = 'cash'
        elif payment_method == 2:
            payment_method = 'transfer'

        payment_amount = int(input("Сумма: "))

        Payment.objects.create(user=user, course=course, lesson=lesson, payment_amount=payment_amount,
                               payment_method=payment_method)

        print('Платеж создан')

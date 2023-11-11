from django.contrib.auth import get_user_model
from django.db import models

from config import settings

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    preview = models.ImageField(upload_to='courses/preview', verbose_name='Превью', **NULLABLE)
    description = models.TextField(verbose_name='Описание')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE, verbose_name='Владелец')
    price = models.PositiveIntegerField(default=0, verbose_name='Цена')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    preview = models.ImageField(upload_to='courses/preview', verbose_name='Превью', **NULLABLE)
    video_link = models.URLField(verbose_name='Ссылка на видео', **NULLABLE)

    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс', related_name='lessons')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE, verbose_name='Владелец')

    def __str__(self):
        return f'Урок - {self.title}, курса - {self.course.title}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Payment(models.Model):
    class PaymentMethod(models.TextChoices):
        CASH = 'cash', 'наличные'
        TRANSFER = 'transfer', 'перевод на счет'

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='Пользователь',
                             related_name='payments')
    payment_date = models.DateField(auto_now_add=True, verbose_name='Дата оплаты')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Оплаченный курс', **NULLABLE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Оплаченный урок', **NULLABLE)
    payment_amount = models.IntegerField(verbose_name='Сумма оплаты')
    payment_method = models.CharField(max_length=10, choices=PaymentMethod.choices, verbose_name='Способ оплаты')
    currency = models.CharField(max_length=50, verbose_name='Валюта', default='USD')
    stripe_id = models.CharField(max_length=150, **NULLABLE, verbose_name='Stripe ID')

    def __str__(self):
        return f'Оплата за: {self.course.title if self.course else self.lesson.title}, ' \
               f'пользователем - {self.user.email}'

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE, related_name='subscription'
                             , verbose_name='Пользователь')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subscription', verbose_name='Курс')
    subscribed = models.BooleanField(default=False, verbose_name='Признак подписки')

    def __str__(self):
        return f"{self.subscribed} - {self.course} - {self.user}"

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

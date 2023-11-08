from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from courses.models import Course, Lesson, Subscription
from user.models import User


class LessonTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(
            email='test@test.ru',
            is_staff=True,
            is_superuser=True,
            is_active=True
        )
        self.user.set_password('0000')
        self.user.save()
        self.access_token = str(AccessToken.for_user(self.user))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.course = Course.objects.create(
            title='test_course',
            description='course for test',
            owner=self.user
        )
        self.course.save()

        self.lesson = Lesson.objects.create(
            title='test_lesson',
            description='lesson for test',
            course=self.course,
            owner=self.user
        )

        self.lesson.save()

        self.subscription = Subscription.objects.create(
            course=self.course
        )
        self.subscription.save()

    def test_create_lesson(self):
        """Создание урока"""
        data = {'title': 'test', 'course': self.course.pk, 'description': 'lesson for test'}
        response = self.client.post('/lesson/create/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_lessons(self):
        """Тестирование получения списка уроков"""
        response = self.client.get('/lesson/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_lesson(self):
        """Получение урока"""
        response = self.client.get(f'/lesson/{self.lesson.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_lesson(self):
        """Изменение урока"""
        valid_data = {
            'title': 'new_test', 'description': 'Какое-то описание', 'video_link': 'https://www.youtube.com/test',
            'course': self.course.pk
        }
        invalid_video_url = {'title': 'new_test', 'description': 'Какое-то описание', 'video_link': 'https://www.test',
                             'course': self.course.pk}
        invalid_description = {'title': 'new_test', 'description': 'Какое-то описание https://www.test',
                               'video_link': 'https://www.youtube.com/test', 'course': self.course.pk}
        valid_description = {'title': 'new_test', 'description': 'Какое-то описание',
                             'video_link': 'https://www.youtube.com/test', 'course': self.course.pk}
        no_data = {'description': 'Какое-то описание', 'video_link': 'https://www.youtube.com/test',
                   'course': self.course.pk}

        response = self.client.put(f'/lesson/{self.lesson.pk}/update/', valid_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['title'], valid_data['title'])
        self.assertEqual(response.json()['description'], valid_data['description'])
        self.assertEqual(response.json()['video_link'], valid_data['video_link'])

        response = self.client.put(f'/lesson/{self.lesson.pk}/update/', invalid_video_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'non_field_errors': ['Неверный YouTube URL-адрес!']})

        response = self.client.put(f'/lesson/{self.lesson.pk}/update/', invalid_description)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'non_field_errors': ['В описании указан недопустимый URL!']})
        response = self.client.put(f'/lesson/{self.lesson.pk}/update/', valid_description)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.put(f'/lesson/{self.lesson.pk}/update/', no_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'title': ['Обязательное поле.']})

    def test_delete_lesson(self):
        """Удаление урока"""
        response = self.client.delete(f'/lesson/{self.lesson.pk}/delete/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.filter(pk=self.lesson.pk).exists(), False)

    def test_subscription_create(self):
        """Создание подписки"""
        data = {'course': self.course.pk}
        response = self.client.post('/subscriptions/create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['course'], self.course.pk)
        self.assertEqual(response.json()['user'], self.user.__str__())

        response = self.client.post('/subscriptions/create/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'non_field_errors': ['Подписка уже существует']})

    def test_subscription_delete(self):
        """Удаление подписки"""
        response = self.client.delete(f'/subscriptions/{self.subscription.pk}/delete/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

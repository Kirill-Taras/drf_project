from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from materials.models import Course, Lesson, Subscription
from users.models import User


class LessonCRUDTests(APITestCase):
    def setUp(self):
        # Создаем группу модераторов
        self.moder_group = Group.objects.create(name='moders')

        # Создаем тестовых пользователей
        self.admin = User.objects.create_superuser(
            email='admin@test.com',
            password='testpass'
        )
        self.moderator = User.objects.create_user(
            email='moder@test.com',
            password='testpass'
        )
        self.moderator.groups.add(self.moder_group)
        self.user = User.objects.create_user(
            email='user@test.com',
            password='testpass'
        )

        # Создаем тестовые данные
        self.course = Course.objects.create(
            title='Test Course',
            owner=self.admin
        )
        self.lesson = Lesson.objects.create(
            title='Test Lesson',
            course=self.course,
            owner=self.admin
        )

    def test_lesson_create_permissions(self):
        """Тест прав доступа при создании урока"""
        test_cases = [
            (self.admin, status.HTTP_201_CREATED),
            (self.moderator, status.HTTP_403_FORBIDDEN),
            (self.user, status.HTTP_201_CREATED),
            (None, status.HTTP_401_UNAUTHORIZED)
        ]

        url = reverse('materials:lesson_create')
        data = {
            'title': 'New Lesson',
            'course': self.course.id,
            'description': 'Test description',
            'video_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        }

        for user, expected_status in test_cases:
            if user:
                self.client.force_authenticate(user=user)
            else:
                self.client.logout()

            response = self.client.post(url, data)
            self.assertEqual(
                response.status_code,
                expected_status,
                f'Failed for {user}. Response: {response.data}'
            )


    def test_lesson_update_by_moderator(self):
        """Тест обновления урока модератором"""
        self.client.force_authenticate(user=self.moderator)
        url = reverse('materials:lesson_retrive', args=[self.lesson.id])
        data = {'title': 'Updated by Moderator'}

        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, 'Updated by Moderator')


class SubscriptionTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='user@test.com',
            password='testpass'
        )
        self.course = Course.objects.create(title='Test Course', owner=self.user)

    def test_subscription_flow(self):
        """Тест полного цикла подписки/отписки"""
        self.client.force_authenticate(user=self.user)
        url = reverse('materials:subscription')

        # Подписываемся
        response = self.client.post(url, {'course_id': self.course.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            Subscription.objects.filter(
                user=self.user,
                course=self.course
            ).exists()
        )

        # Отписываемся
        response = self.client.post(url, {'course_id': self.course.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(
            Subscription.objects.filter(
                user=self.user,
                course=self.course
            ).exists()
        )

    def test_subscription_status_in_course(self):
        self.client.force_authenticate(user=self.user)

        url = reverse('materials:course-detail', args=[self.course.id])

        response = self.client.get(url)
        self.assertIn('is_subscribed', response.data)
        self.assertFalse(response.data['is_subscribed'])

        sub_url = reverse('materials:subscription')
        self.client.post(sub_url, {'course_id': self.course.id})

        response = self.client.get(url)
        self.assertIn('is_subscribed', response.data)
        self.assertTrue(response.data['is_subscribed'])
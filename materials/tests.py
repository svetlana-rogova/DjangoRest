from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from django.urls import reverse
from users.models import CustomUser
from materials.models import Course, Lesson, Subscription
from django.contrib.auth.models import Group



class MaterialsTestCase(APITestCase):

    def setUp(self) -> None:

        self.group = Group.objects.create(name='moderator')

        self.client = APIClient()

        self.user = CustomUser.objects.create_user(username='test', email='user@test.com', password='1234')
        self.user.groups.add(self.group)

        self.other_user = CustomUser.objects.create_user(username='test2',email='other@test.com', password='1234')

        self.owner_user = CustomUser.objects.create_user(username='test3', email='owner@test.com', password='1234')

        self.course = Course.objects.create(title='Test course', description='Test description', owner=self.owner_user)

        self.lesson = Lesson.objects.create(title='Test lesson', description='Lesson desc', course=self.course,
                                            owner=self.owner_user)

    def test_lesson_create(self):
        self.client.force_authenticate(user=self.other_user)
        data = {
            "title": "New lesson",
            "description": "Text",
            "course": self.course.id,
            "video_url": "https://youtube.com/watch?v=123"
        }
        response = self.client.post(reverse('materials:lesson-create'), data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_lesson_create_for_moderator(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "title": "New lesson",
            "description": "Text",
            "course": self.course.id,
            "video_url": "https://youtube.com/watch?v=123"
        }
        response = self.client.post(reverse('materials:lesson-create'), data)
        self.assertEqual(response.status_code, 403)

    def test_lesson_list_for_moderator(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('materials:lesson-list'))
        self.assertEqual(response.status_code, 200)

    def test_lesson_list_not_moderator(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.get(reverse('materials:lesson-list'))
        self.assertEqual(response.status_code, 403)

    def test_course_list_moderator_only(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('materials:course-list'))
        self.assertEqual(response.status_code, 200)

    def test_course_list_not_moderator(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.get(reverse('materials:course-list'))
        self.assertEqual(response.status_code, 403)

    def test_course_create_not_moderator(self):
        self.client.force_authenticate(user=self.other_user)
        data = {
            "title": "Python 2",
            "image": "",
            "description": "Python — высокоуровневый язык программирования общего назначения."
        }
        response = self.client.post(reverse('materials:course-list'), data)
        self.assertEqual(response.status_code, 201)

    def test_course_create_for_moderator(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "title": "Python 2",
            "image": "",
            "description": "Python — высокоуровневый язык программирования общего назначения."
        }
        response = self.client.post(reverse('materials:course-list'), data)
        self.assertEqual(response.status_code, 403)

    def test_course_detail_for_moderator(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('materials:course-detail', args=[self.course.id]))
        self.assertEqual(response.status_code, 200)

    def test_course_detail_not_moderator(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.get(reverse('materials:course-detail', args=[self.course.id]))
        self.assertEqual(response.status_code, 403)

    def test_course_detail_for_owner(self):
        self.client.force_authenticate(user=self.owner_user)
        response = self.client.get(reverse('materials:course-detail', args=[self.course.id]))
        self.assertEqual(response.status_code, 200)

    def test_lesson_detail_for_moderator(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('materials:lesson-retrieve', args=[self.lesson.id]))
        self.assertEqual(response.status_code, 200)

    def test_lesson_detail_not_moderator(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.get(reverse('materials:lesson-retrieve', args=[self.lesson.id]))
        self.assertEqual(response.status_code, 403)

    def test_lesson_detail_for_owner(self):
        self.client.force_authenticate(user=self.owner_user)
        response = self.client.get(reverse('materials:lesson-retrieve', args=[self.lesson.id]))
        self.assertEqual(response.status_code, 200)

    def test_lesson_update_for_moderator(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "title": "New lesson2",
            "description": "Text2",
            "course": self.course.id,
            "video_url": "https://youtube.com/watch?v=123"
        }
        response = self.client.put(reverse('materials:lesson-update', args=[self.lesson.id]), data)
        self.assertEqual(response.status_code, 200)

    def test_lesson_update_not_moderator(self):
        self.client.force_authenticate(user=self.other_user)
        data = {
            "title": "New lesson2",
            "description": "Text2",
            "course": self.course.id,
            "video_url": "https://youtube.com/watch?v=123"
        }
        response = self.client.put(reverse('materials:lesson-update', args=[self.lesson.id]), data)
        self.assertEqual(response.status_code, 403)

    def test_lesson_update_for_owner(self):
        self.client.force_authenticate(user=self.owner_user)
        data = {
            "title": "New lesson2",
            "description": "Text2",
            "course": self.course.id,
            "video_url": "https://youtube.com/watch?v=123"
        }
        response = self.client.put(reverse('materials:lesson-update', args=[self.lesson.id]), data)
        self.assertEqual(response.status_code, 200)

    def test_course_update_for_moderator(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "title": "Python 3",
            "image": "",
            "description": "Python — высокоуровневый язык программирования общего назначения."
        }
        response = self.client.put(reverse('materials:course-detail', args=[self.course.id]), data)
        self.assertEqual(response.status_code, 200)

    def test_course_update_not_moderator(self):
        self.client.force_authenticate(user=self.other_user)
        data = {
            "title": "Python 3",
            "image": "",
            "description": "Python — высокоуровневый язык программирования общего назначения."
        }
        response = self.client.put(reverse('materials:course-detail', args=[self.course.id]), data)
        self.assertEqual(response.status_code, 403)

    def test_course_update_for_owner(self):
        self.client.force_authenticate(user=self.owner_user)
        data = {
            "title": "Python 3",
            "image": "",
            "description": "Python — высокоуровневый язык программирования общего назначения."
        }
        response = self.client.put(reverse('materials:course-detail', args=[self.course.id]), data)
        self.assertEqual(response.status_code, 200)

    def test_course_delete_for_moderator(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse('materials:course-detail', args=[self.course.id]))
        self.assertEqual(response.status_code, 403)

    def test_course_delete_not_moderator(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(reverse('materials:course-detail', args=[self.course.id]))
        self.assertEqual(response.status_code, 403)

    def test_course_delete_for_owner(self):
        self.client.force_authenticate(user=self.owner_user)
        response = self.client.delete(reverse('materials:course-detail', args=[self.course.id]))
        self.assertEqual(response.status_code, 204)

    def test_lesson_delete_for_moderator(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse('materials:lesson-delete', args=[self.lesson.id]))
        self.assertEqual(response.status_code, 403)

    def test_lesson_delete_not_moderator(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(reverse('materials:lesson-delete', args=[self.lesson.id]))
        self.assertEqual(response.status_code, 403)

    def test_lesson_delete_for_owner(self):
        self.client.force_authenticate(user=self.owner_user)
        response = self.client.delete(reverse('materials:lesson-delete', args=[self.lesson.id]))
        self.assertEqual(response.status_code, 204)

    def test_subscription_create(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.post(reverse('materials:subscription'), {"course_id": self.course.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "подписка добавлена")
        self.assertTrue(Subscription.objects.filter(owner=self.other_user, course=self.course).exists())

    def test_subscription_delete(self):
        self.subscription = Subscription.objects.create(owner=self.other_user, course=self.course)
        self.client.force_authenticate(user=self.other_user)
        response = self.client.post(reverse('materials:subscription'), {"course_id": self.course.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "подписка удалена")
        self.assertFalse(Subscription.objects.filter(owner=self.other_user, course=self.course).exists())